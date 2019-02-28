from . import base
from . import router
from . import reactor
from . import core

global config
config = base.config().json
print("config -- %s" % config)