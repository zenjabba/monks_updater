import subprocess

import psutil

from . import logger

log = logger.get_logger(__name__)


def find(process_name, username=None):
    processes = []
    log.debug("Retrieving processes matching %s", process_name)

    try:
        for process in psutil.process_iter():
            if process_name.lower() in process.name().lower():
                if username:
                    if username.lower() not in process.username().lower():
                        continue
                processes.append(process.pid)

    except:
        log.exception("Exception finding process %s by user %s: ", process_name, username if username else 'Any')
        return None
    return processes


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = str(process.stdout.readline()).lstrip('b').replace('\\n', '').strip()
        if process.poll() is not None:
            break
        if output and len(output) >= 4:
            log.info(output)

    rc = process.poll()
    return rc
