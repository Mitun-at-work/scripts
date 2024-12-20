import os
from pathlib import Path
import coloredlogs


class DirLink :

    def __init__(self):
    
        dir_path = Path.cwd()
        coloredlogs.install(level="INFO", fmt="%(asctime)s - %(levelname)s - %(message)s")
        
        self.paths = {
                    "code": f"{dir_path}/code/",
                    "metadata": f"{dir_path}/meta/",
                    "data": f"{dir_path}/data/",
                    "vector": f"{dir_path}/vector/",
                    "additional": f"{dir_path}/additional/",
                    "png": f"{dir_path}/png/"
                }

        # List the files in each directory
        self.directories = {key: os.listdir(path) for key, path in self.paths.items()}

if __name__ == '__main__' :
    print(DirLink().directories)