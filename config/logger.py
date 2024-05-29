import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "app.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s"
)

fh = RotatingFileHandler(log_dir, maxBytes=5000000, backupCount=5)
fh.setFormatter(formatter)
logger.addHandler(fh)