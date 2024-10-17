import tarfile
import random
import atexit
import shutil
import json
import os

class AppBuilder:
    def __init__(self):
        """Class for building pypkg apps.
        """

        # Setup Temporary build folder
        self.tempfolder = os.path.expanduser("~/.pypkg/pypkgbuildtmp"+str(random.randint(11111,99999))) 
        os.mkdir(self.tempfolder)

        self.build = tarfile.open(f"build.pypkg","w:")

        self.config = {"dotdesktop":{}}

        atexit.register(self.rmtemp) # make sure to get rid of those
        atexit.register(self.build.close)

    def __setitem__(self,key,value):
        self.config[key] = value
    def __getitem__(self,key):
        return self.config[key]

    def rmtemp(self):
        shutil.rmtree(self.tempfolder)
    
    def set_exec(self,executablepath):
        """Set python file that represents the app.

        To help precisely set the executable, %APPROOT represents the app directory. (e.g. $APPROOT/main.py)

        Args:
            executablepath (str): Path of the python file that should be launched when app is launched.
        """
        self.config["executable"] = executablepath
    def set_icon(self,icon: str):
        """Set application icon.

        Args:
            icon (str): Icon path.
        """
        self.build.add(
            icon,arcname="icon."+icon.split(".")[-1] # rename icon to just "icon" in build archive to keep things simple
        )
    def add(self,path):
        """Add file or folder to the $APPROOT directory.

        Args:
            path (str): Location of the file or folder.
        """

        self.build.add(path,f"approot/{path.split("/")[-1]}")
    def build_app(self):
        with open(f"{self.tempfolder}/config.json","w") as file:
            json.dump(self.config,file)
        self.build.add(f"{self.tempfolder}/config.json","config.json")
        self.build.close()