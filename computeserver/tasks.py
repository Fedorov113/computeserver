from celery import shared_task
from celery.utils.log import get_task_logger
import time
logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    logger.info("ADDING")
    time.sleep(30) 
    logger.info("DONE")
    return x + y
