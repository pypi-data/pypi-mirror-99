from corelibs import _corelibs as _c

log = _c.log
cl = _c.cl
log.info("Hello")

cl.install(level=30)
log.info("Hello ne doit pas s'afficher...")
