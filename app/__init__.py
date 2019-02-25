from . import base
from . import router
from . import reactor

global config
config = base.config().json
print("config -- %s" % config)