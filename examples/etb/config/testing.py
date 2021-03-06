from config import settings
from salmon import view
from salmon.routing import Router
from salmon.server import Relay
import jinja2
import logging
import logging.config
import os

# configure logging to go to a log file
logging.config.fileConfig("config/test_logging.conf")

# the relay host to actually send the final message to (set debug=1 to see what
# the relay is saying to the log server).
settings.relay = Relay(host=settings.relay_config['host'], 
                       port=settings.relay_config['port'], debug=0)


settings.receiver = None


Router.defaults(**settings.router_defaults)
Router.load(settings.handlers + settings.queue_handlers)
Router.RELOAD=True

view.LOADER = jinja2.Environment(
    loader=jinja2.PackageLoader(settings.template_config['dir'], 
                                settings.template_config['module']))

# if you have pyenchant and enchant installed then the template tests will do
# spell checking for you, but you need to tell pyenchant where to find itself
if 'PYENCHANT_LIBRARY_PATH' not in os.environ:
    os.environ['PYENCHANT_LIBRARY_PATH'] = '/opt/local/lib/libenchant.dylib'

