import os,requests,time
from colabrun.common import config, utils, Requests
from colabrun.Client import Client
arr_threads=[]
def start():
    try:
        mf_server = os.getenv("MF_SERVER", config.ServerAdress.MF_SERVER)
        lst_objs = requests.get(f"{mf_server}/client/get").json()
        lst_clients = []
        for obj in lst_objs:
            client = Client(obj['id'], obj['email'])
            client.start()
            lst_clients.append(client)
            time.sleep(30)
        for client in lst_clients:
            client.wait()
        print('done')
    except Exception as e:
        print(e)
        pass
    os.system("reboot")
