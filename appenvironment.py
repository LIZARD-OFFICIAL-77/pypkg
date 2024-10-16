import pathlib
import venv
import os



def delenv(name="throwerrror"):
    os.system(f"rm -rf ~/.pypkg/appenvs/{name}")

class AppEnvironment:
    def __init__(self,name):
        self.name = name
        self.path = f"{os.path.expanduser("~")}/.pypkg/appenvs/{self.name}"
        self.existing = True
        if not pathlib.Path(self.path).is_dir():
            self.existing = False
            venv.create(f"{self.path}/venv")
            os.system(f"{self.path}/venv/bin/python ensurepip --defualt-pip")
            os.mkdir(self.path)
    
    def getpath(self,path):
        return self.path + path
    
    def python(self,command):
        os.system(f"{self.path}/venv/bin/python {command}")

    def pip(self,command):
        os.system(f"{self.path}/venv/bin/pip {command}")