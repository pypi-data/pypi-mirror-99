import re, os, sys, shutil
from pathlib import Path
import logging
from typing import List, Set
import coloredlogs

import yaml


logger = logging.getLogger(__name__)
coloredlogs.install()

class Error(OSError):
    pass


def isrepository(url_string):
    url_object = urllib.parse.urlparse(url_string)
    url_path = Path(url_object.path)
    if len(url_path.parts)==3:
        return True
    else:
        return False

def get_resource_location(rsrc,config):
    if "archive_location" in rsrc and "archive" in rsrc:
        pass
    else:
        logger.error(f"{rsrc['id']}: insufficient archive info")
        return
    try:
        if rsrc["archive"] in config.environ:
            projdir = config.environ[rsrc["archive"]]
        else:
            projdir = os.environ.get(rsrc['archive'].replace('$',''))
    except Exception as e:
        logger.error(f"[{rsrc['id']}]: {e}")
        return
    
    return os.path.join(projdir,rsrc['archive_location'])

def copy_file(src,dst,dst_root=None,rules:Set[str]=None,*,follow_symlinks=True):
    """Based on shutil.copy2"""
    
    if rules:
        relpath = os.path.relpath(dst,dst_root)
        logger.debug("relpath={}".format(relpath))
        for rule in rules:
            relpath = sed(rule,relpath)
        logger.debug("new relpath={}".format(relpath))
        
        if relpath:
            dst = os.path.join(dst_root,relpath)
        else:
            return

    if dst and os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))

    shutil.copyfile(src,dst,follow_symlinks=follow_symlinks)
    shutil.copystat(src, dst, follow_symlinks=follow_symlinks)
    return dst


def _copytree(entries, src, dst, dst_root, rules, symlinks, ignore, copy_function,
              ignore_dangling_symlinks, dirs_exist_ok=False):
    if ignore is not None:
        ignored_names = ignore(os.fspath(src), [x.name for x in entries])
    else:
        ignored_names = set()

    if rules:
        relpath = os.path.relpath(dst,dst_root)
        logger.debug("relpath={}".format(relpath))
        for rule in rules:
            relpath = sed(rule,relpath)
        logger.debug("new relpath={}".format(relpath))
        
        if relpath:
            dst = os.path.join(dst_root,relpath)
        else:
            return

    os.makedirs(dst, exist_ok=dirs_exist_ok)
    errors = []
    use_srcentry = copy_function is copy_file or copy_function is shutil.copy

    for srcentry in entries:
        if srcentry.name in ignored_names:
            continue
        srcname = os.path.join(src, srcentry.name)
        dstname = os.path.join(dst, srcentry.name)

        ##########################################################################
        if rules:
            relpath = os.path.relpath(dst,dst_root)
            logger.debug("relpath={}".format(relpath))
            for rule in rules:
                relpath = sed(rule,relpath)
            logger.debug("new relpath={}".format(relpath))
            
            if relpath:
                dst = os.path.join(dst_root,relpath)
            else:
                return
        ##########################################################################



        srcobj = srcentry if use_srcentry else srcname
        try:
            is_symlink = srcentry.is_symlink()
            if is_symlink and os.name == 'nt':
                # Special check for directory junctions, which appear as
                # symlinks but we want to recurse.
                lstat = srcentry.stat(follow_symlinks=False)
                if lstat.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT:
                    is_symlink = False
            if is_symlink:
                linkto = os.readlink(srcname)
                if symlinks:
                    # We can't just leave it to `copy_function` because legacy
                    # code with a custom `copy_function` may rely on copytree
                    # doing the right thing.
                    os.symlink(linkto, dstname)
                    shutil.copystat(srcobj, dstname, follow_symlinks=not symlinks)
                else:
                    # ignore dangling symlink if the flag is on
                    if not os.path.exists(linkto) and ignore_dangling_symlinks:
                        continue
                    # otherwise let the copy occur. copy2 will raise an error
                    if srcentry.is_dir():
                        copy_tree(srcobj, dstname, dst_root, rules, symlinks, ignore,
                                 copy_function, dirs_exist_ok=dirs_exist_ok)
                    else:
                        copy_function(srcobj, dstname, dst_root, rules)
            elif srcentry.is_dir():
                copy_tree(srcobj, dstname, dst_root, rules, symlinks, ignore, copy_function,
                         dirs_exist_ok=dirs_exist_ok)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy_function(srcobj, dstname, dst_root, rules)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        # Copying file access times may fail on Windows
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))
    if errors:
        raise Error(errors)
    return dst

def copy_tree(src, dst, dst_root=None, rules:Set[str]=None,symlinks=False, ignore=None, copy_function=copy_file,
             ignore_dangling_symlinks=False, dirs_exist_ok=True):
    """Recursively copy a directory tree and return the destination directory.
    dirs_exist_ok dictates whether to raise an exception in case dst or any
    missing parent directory already exists.
    If exception(s) occur, an Error is raised with a list of reasons.
    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied. If the file pointed by the symlink doesn't
    exist, an exception will be added in the list of errors raised in
    an Error exception at the end of the copy process.
    You can set the optional ignore_dangling_symlinks flag to true if you
    want to silence this exception. Notice that this has no effect on
    platforms that don't support os.symlink.
    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copy_tree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():
        callable(src, names) -> ignored_names
    Since copy_tree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.
    The optional copy_function argument is a callable that will be used
    to copy each file. It will be called with the source path and the
    destination path as arguments. By default, copy2() is used, but any
    function that supports the same signature (like copy()) can be used.
    """
    sys.audit("shutil.copytree", src, dst)
    with os.scandir(src) as itr:
        entries = list(itr)
    
    if dst:
        return _copytree(entries=entries, src=src, dst=dst, dst_root=dst_root, rules=rules, symlinks=symlinks,
                     ignore=ignore, copy_function=copy_function,
                     ignore_dangling_symlinks=ignore_dangling_symlinks,
                     dirs_exist_ok=dirs_exist_ok)


