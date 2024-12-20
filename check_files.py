import os

from get_dir import DirLink


import pandas as pd
import logging
import coloredlogs



class CheckFile :
        
    coloredlogs.install(level="INFO", fmt="%(asctime)s - %(levelname)s - %(message)s")

    def __init__(self):

        self.dir = DirLink()

        self.code = sorted(self.dir.directories['code'])
        self.png = sorted(self.dir.directories['png'])
        self.meta = sorted(self.dir.directories['metadata'])
        self.data = sorted(self.dir.directories['data'])

    def file_check(self) :

        error = {}

        code_file_name = set([code_file.split('.')[0] for code_file in self.code])
        png_file_name = set([png_file.split('.')[0] for png_file in self.png])
        meta_file_name = set([meta_file.split('.')[0] for meta_file in self.meta])
        data_file_name = set([data_file.split('.')[0] for data_file in self.data])

        diff = [code_file_name, png_file_name, meta_file_name, data_file_name]
        cell = ['Code', 'PNG', 'Meta', 'Data']

        n = len(diff)

        for i in range(n) :

            message = ''

            for j in range(i + 1, n): 

                missing_files = diff[i] - diff[j]

                if missing_files : 

                    missing_parameter = cell[j] if len(diff[i]) >  len(diff[j]) else cell[i]

                    for missed_file in missing_files : 

                        if missed_file in error :
                            error[missed_file].append(f"{missing_parameter} File Missing")

                        else :
                            error[missed_file] = [f"{missing_parameter} File Missing"]

                print(missing_files)

        return error


if __name__ == '__main__' :
    CheckFile().file_check()