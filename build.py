import tarfile
import random
import atexit
import shutil
import os

class JsonDotDesktopBuilder:
    def __init__(self,json: dict):
        self.build = "[Desktop Entry]\n"
        for k,v in json.items():
            self.build = f"{k}={v}\n"

class AppBuilder:
    def __init__(self,name):
        """Class for building pypkg apps.

        Args:
            name (str): App name
        """
        self.name = name

        
        self.tempfolder = "pypkgbuild"+str(random.randint(11111,99999)) # Create temp folder because tarfile needs it.
        os.mkdir(self.tempfile)
        atexit.register(self.deltemp)

        self.approot = tarfile.open(f"{self.tempfolder}/approot.tar.gz","w:")
        self.build = tarfile.open(f"{self.tempfolder}/build.tar.gz","w:")

        self.dotdesktop = {}
    
    def __setitem__(self,key,value):
        self.dotdesktop[key] = value

    def deltemp(self):
        shutil.rmtree(self.tempfile)
    
    def add(self,path):
        """Add file or folder to the app directory.

        Args:
            path (str): Location of the file or folder.
        """
        self.approot.add(path)
    
