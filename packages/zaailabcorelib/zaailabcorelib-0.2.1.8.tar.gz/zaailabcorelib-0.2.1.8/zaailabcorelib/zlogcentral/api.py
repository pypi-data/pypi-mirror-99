import socket
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import os
import json


def send_request_async(param):
    try:
        requests.post(param[0], data=param[1], timeout=1)
    except:
        pass
request_pool = ThreadPoolExecutor(max_workers=20)
def get_local_ip():
    local_ip = socket.gethostname()
    local_ip="10.40.34."+local_ip[-2:]
    return local_ip
def get_name_of_folder():
    env_name = os.getenv('NAME')
    if(env_name is None):
        path = os.getcwd()
        folder = os.path.basename(path)
    else:
        folder = env_name
    return folder

class LogJob():
    def __init__(self, uid=0, cmd=0):
        self.uid = uid
        self.cmd = cmd
        self.start_time = int(time.time()*1000)
        self.param = {}

    def set_dict_param(self, param):
        self.param.update(param)
    def set_param(self, key, value):
        self.param[key]=value
    def get_start_time(self):
        return self.start_time
    def get_uid(self):
        return self.uid
    def get_cmd(self):
        return self.cmd
    def get_json_string(self):
        return json.dumps(self.param)

class LogClient:

    def __init__(self, host, port):
        self.host = host
        self.port = str(port)


    def __general_log(self, category, log, path, sync, type_log):
        project = get_name_of_folder()
        local_ip = get_local_ip()
        created_time = int(time.time()*1000)
        log_json={
            "project":project,
            "ip":local_ip,
            "created_time":created_time,
            "log":log

        }

        log = json.dumps(log_json)
        data = {
            'category': category,
            'log': log,
            'type': type_log
        }

        if(sync):
            try:

                return requests.post("http://" + self.host + ":" + self.port + path, data=data, timeout=1)
            except:
                return None

        else:
            param = []
            param.append("http://" + self.host + ":" + self.port + path)
            param.append(data)
            request_pool.submit(send_request_async,(param))
            return None
    def log(self, category, log, sync=False, type_log="result"):
        """
            log function

            :param category: category for the project (Ex : ZALO_FACE)
            :param log has 2 type:
                string: old flow. Just send user's json string
                LogJob: new flow. Send LogJob object with cmd, uid, execute_time are added to data
        """
        if (type(log) == LogJob):
            log.set_param("uid", log.get_uid())
            log.set_param("cmd", log.get_cmd())
            log.set_param("execute_time", int(time.time()*1000)-log.get_start_time())
            return self.__general_log(category, log.get_json_string(), "/log", sync, type_log)
        else:
            return self.__general_log(category, log, "/log", sync, type_log)