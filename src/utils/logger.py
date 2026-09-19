import logging

def get_logger(name: str):
  logger=logging.getLogger(name)
  if logger.handlers:
    return logger
  logger.setLevel(logging.INFO)
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s',datefmt="%Y-%m-%d %H:%M:%S")
  ch.setFormatter(formatter)
  logger.addHandler(ch)
  return logger

  