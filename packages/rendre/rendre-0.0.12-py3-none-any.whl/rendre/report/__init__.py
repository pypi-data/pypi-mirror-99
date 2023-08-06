
def init_report(args, config)->tuple:
    if args.template=="tmpl-0001":
        from .tmpl_0001 import init, item, close
    if args.template=="tmpl-0002":
        from .tmpl_0002 import init, item, close
    if args.template=="tmpl-0003":
        from .tmpl_0003 import init, item, close
    if args.template=="tmpl-0004":
        from .tmpl_0004 import init, item, close
    if args.template=="tmpl-0007":
        try:
            from tmpl_0007 import init, item, close
        except:
            from .tmpl_0007 import init,item,close

    if args.template=="tmpl-0008":
        from .tmpl_0008 import init, item, close
    return init, item, close
