import logging
def get_logger():
 logging.basicConfig(filename="logs/etl.log",level=logging.INFO)
 return logging.getLogger("etl")
