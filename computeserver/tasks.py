from celery import shared_task
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from celery import Task
from .celery import app
import time
import subprocess
from celery.result import AsyncResult
import requests


# https://github.com/cellgeni/nf-server/blob/master/src/nf_server/execution.py
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True, cwd='/home/fedorov_de/RUN_DIR_NF')
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

logger = get_task_logger(__name__)
class ComputeTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        result = AsyncResult(task_id)
        # Send info about successful completition to head server
        logger.info("SUUC CALLBACK")
        response = requests.post('http://192.168.0.114:8000/compute/talkback/', 
            data={'task_id': task_id, 'state': result.state})
        print(response)

@app.task(base=ComputeTask)
def execute_nf():
    logger.info("STARTING EXECUTION")

    dir_with_fastq = ''


    # ============================================
    # === RUN NEXTFLOW
    # c = "nextflow run ~/OpenGit/wf-artic/main.nf -profile conda --scheme_name SARS-CoV-2 --scheme_version V3 --fastq ~/test/"
    # for path in execute(c):
    #     logger.info(f"Stdout: {path}")
    # ============================================
    time.sleep(4) 
    logger.info("DONE")
    return 'done'



logger = get_task_logger(__name__)
class CopyTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        result = AsyncResult(task_id)
        # Send info about successful completition to head server
        logger.info("SUUC CALLBACK")
        response = requests.post('http://192.168.0.114:8000/compute/talkback/', 
            data={'task_id': task_id, 'state': result.state})
        print(response)