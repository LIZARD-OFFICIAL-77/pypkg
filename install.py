from appenvironment import AppEnvironment

import hashlib
import tarfile
import random
import shutil
import atexit
import json
import os



class JsonDotDesktopBuilder:
    def __init__(self,json: dict):
        self.build = "[Desktop Entry]\n"
        for k,v in json.items():
            self.build = f"{k}={v}\n"
    def install(self,dotdesktopname):
        with open(os.path.expanduser(f"~/.local/share/applications/{dotdesktopname}.desktop"),"w") as file:
            file.write(self.build)

class Installer:
    def __init__(self,pypkgfile):
        self.pypkgfile = pypkgfile
        self.config = {}
        
        # Create temporary folder to extract the build files to
        
        self.tempfolder = os.path.expanduser("~/.pypkg/pypkginstalltmp"+str(random.randint(11111,99999))) 
        os.mkdir(self.tempfolder)
        atexit.register(self.rmtemp)
        
        # Setup files required to install app
        
        with tarfile.open(self.pypkgfile,"r:") as file:
            file.extraction_filter = (lambda x,y: x)
            file.extractall(self.tempfolder)
        with open(f"{self.tempfolder}/config.json") as file:
            self.config: dict = json.load(file)
        
    def install(self):
        self.appenv = AppEnvironment(self.config["pkgname"])
        shutil.copytree(f"{self.tempfolder}/approot",self.appenv.getpath("/")) # copy files from approot to app environment
        
        self.appenv.pip(f"install {self.config["pip"].join(" ")}")
        
        self.dotdesktop = JsonDotDesktopBuilder(self.config["dotdesktop"])
        self.dotdesktop.install(self.config["pkgname"])
        
        
        
    def rmtemp(self):
        shutil.rmtree(self.tempfolder)

installer = Installer("build.pypkg")

#installer.install()