from config import settings
from salmon.routing import Router
from salmon.server import Relay, SMTPReceiver
from salmon import view
import logging
import logging.config
import jinja2

logging.config.fileConfig("config/logging.conf")

# the relay host to actually send the final message to
settings.relay = Relay(host=settings.relay_config['host'], 
                       port=settings.relay_config['port'], debug=1)

# where to listen for incoming messages
settings.receiver = SMTPReceiver(settings.receiver_config['host'],
                                 settings.receiver_config['port'])

Router.defaults(**settings.router_defaults)
Router.load(settings.handlers)
Router.RELOAD=True
Router.LOG_EXCEPTIONS=True
Router.UNDELIVERABLE_QUEUE=queue.Queue(settings.UNDELIVERABLES)

view.LOADER = jinja2.Environment(
    loader=jinja2.PackageLoader(settings.template_config['dir'], 
                                settings.template_config['module']))

