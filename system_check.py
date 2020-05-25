import psutil as ps
import time
import os
from subprocess import Popen, PIPE, DEVNULL
import logging
import telegram_bot as tgbot


log_dir = os.path.join(os.getcwd(), "logs")
# logging.basicConfig(filename=log_dir, level=logging.INFO,
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] (%(threadName)-9s) %(message)s")


def check_status():

    wakeup_time = tgbot.config.WAKEUP_TIME
    trigger = tgbot.config.TRIGGER

    count = 0
    print("System checking started")

    while True:
        if count == trigger:
            time_elapsed = trigger * wakeup_time
            tgbot.send_message("{} is idle for {} minutes {} seconds\n".format(
                os.uname()[1], time_elapsed // 60, time_elapsed % 60))
            count = 0

        if mem_active() or cpu_active() or gpu_active():
            logging.info("Working")
            count = 0

        else:
            logging.info("Idle")
            count+=1

        time.sleep(wakeup_time)

    # '# os.system("sudo shutdown -h now"'

def mem_active():

    mem_vals = ps.virtual_memory().percent

    logging.info(mem_vals)

    if mem_vals < tgbot.config.MEM_THRES:
        return False

    return True


def cpu_active():

    cpu_vals = ps.cpu_percent(percpu=True)

    logging.info(cpu_vals)

    if any([cpu > tgbot.config.CPU_THRES for cpu in cpu_vals]):
        return True

    return False


def gpu_active():

    # print("r_val {}".format(r_val))
    # proc=Popen("nvidia-smi", stdout=PIPE, stderr=PIPE)
    proc=Popen("zibalos", shell=True, stdout=PIPE, stderr=DEVNULL)
    output=proc.communicate()[0]

    if proc.returncode != 0:
        return False

    return str(output).find("No running processes found") == -1


if __name__ == "__main__":
    tgbot.start_bot()
    check_status()

