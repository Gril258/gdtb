from . import base
from . import router

global config
config = base.config().json
print("config -- %s" % config)