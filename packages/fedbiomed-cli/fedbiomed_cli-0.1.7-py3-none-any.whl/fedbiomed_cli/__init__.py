import os
import uuid

__version__ = "0.1.7"

ROOT = os.path.dirname(os.path.abspath(__file__))

# ============================================
# Init client default configurations
# ============================================
CONFIG_FILE = os.path.join(ROOT, 'config.ini')

from .utils.cli import init_client_config

cfg = init_client_config()

# ============================================
# Load client configurations
# ============================================
QUEUE_DIR = os.path.join(ROOT, f'queue_manager')
DB_DIR = os.path.join(ROOT, f'db.json')

MQTT_BROKER = os.getenv('MQTT_BROKER', cfg.get('mqtt', 'broker_url'))
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', cfg.get('mqtt', 'port')))

UPLOADS_URL = os.getenv('UPLOADS_URL', cfg.get('default', 'uploads_url'))
CLIENT_ID = os.getenv('CLIENT_ID', cfg.get('default', 'client_id'))

# ========= PATCH MNIST Bug torchvision 0.9.0 ===================
# https://github.com/pytorch/vision/issues/1938
from six.moves import urllib

opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-agent', 'Python-urllib/3.7'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
    ('Accept-Language', 'en-US,en;q=0.9'),
    ('Accept-Encoding', 'gzip, deflate, br')
]
urllib.request.install_opener(opener)
