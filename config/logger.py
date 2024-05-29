import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s"
)

fh = RotatingFileHandler("logs/app.log", maxBytes=5000000, backupCount=5)
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)