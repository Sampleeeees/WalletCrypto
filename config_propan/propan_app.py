import sys
import os

from config_propan.propan_broker import broker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from propan import RabbitBroker, PropanApp

app = PropanApp(broker)



