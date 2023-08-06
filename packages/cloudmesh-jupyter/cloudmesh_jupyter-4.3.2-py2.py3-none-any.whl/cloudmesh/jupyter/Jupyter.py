import os
from cloudmesh.common.Shell import Shell
# from yamldb import YamlDB
from subprocess import Popen
from cloudmesh.common.util import path_expand
from subprocess import PIPE
from subprocess import STDOUT
import shlex

class Jupyter:


    def __init__(self, user:str, host:str, port:int, directory:str):
        self.user = user
        self.port = port
        self.host = host
        self.directory = directory or ""

        # self.db = YamlDB("~/.cloudmesh/jupyter.yml")

    def start(self):
        command = f"source .bash_profile; jupyter-lab {self.directory} --no-browser --port={self.port} 2>&1"
        print (command)
        p = Popen(['ssh', '-T', f'{self.user}@{self.host}', command],
                   stdin=PIPE, stdout=PIPE, stderr=PIPE,
                   universal_newlines=True)
        p.stdin.flush()
        while True:
            l = p.stdout.readline().strip()
            if l != None and l != "" and l.startswith("or http://127.0.0.1"):
                # print (f"{l}")
                url = l.split(" ")[1]
                self.tunnel()
                Shell.browser(url)

    def stop(self):
        os.system(f"ssh {self.user}@{self.host} killall jupyter-lab")

    def tunnel(self):
        command = f"ssh -N -f -L localhost:{self.port}:localhost:{self.port} {self.user}@{self.host}"
        print (command)
        os.system(command)

    def open(self):
        location = f"https://localhost:{self.port}/lab?"
        print ("Open", location)
        Shell.browser(location)


    #  > /dev/null 2>&1 & echo $! > "dmr.pid"