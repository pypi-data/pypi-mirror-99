import requests
import json
import sys
import os

def get_my_ip():
    url = 'https://api.myip.com'
    r = requests.get(url)
    dato = json.loads(r.text)
    return dato['ip']

def set_base_path():
    token = "\\src\\"
    test_string = os.path.abspath(os.curdir)
    PATH_BASE = test_string.partition(token)[0]
    separator = test_string.partition(token)[1]
    if separator==token:
        sys.path.append(PATH_BASE)
        print("seteando PATH_BASE : ",PATH_BASE ) 


def get_base_path():
    token = "\\src\\"
    curdir_path = os.path.abspath(os.curdir)
    PATH_BASE = curdir_path.partition(token)[0]
    separator = curdir_path.partition(token)[1]
    if separator==token:
        return  PATH_BASE
    else:
        return curdir_path

def main():
    print(get_my_ip())


if __name__ == "__main__":
    main()