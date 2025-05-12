from Utils import init_logging
import logging
init_logging("TextClient", exception_logger="Client")
logger = logging.getLogger("FileLog")
logger.warning("\u2211")