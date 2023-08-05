import os
import uuid

ROOT = os.path.dirname(os.path.abspath(__file__))
QUEUE_DIR = os.path.join(ROOT, f'queue_manager')
DB_DIR = os.path.join(ROOT, f'db.json')

MQTT_BROKER = os.getenv('MQTT_BROKER', 'epione-demo.inria.fr')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', 80))

UPLOADS_URL = os.getenv('UPLOADS_URL', 'https://epione-demo.inria.fr/fedbiomed/upload/')
CLIENT_ID = os.getenv('CLIENT_ID', str(uuid.UUID(int=uuid.getnode())))

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

from torchvision import datasets