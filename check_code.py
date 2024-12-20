from fetch_imports import FetchImports
from check_imports import ImportChecker
from get_dir import DirLink
from pathlib import Path

import os
import logging
import coloredlogs
import nbformat

class CodeCheck:
    def __init__(self):

        # Initialize the logging configuration
        self.dir = DirLink()
        self.import_checker = ImportChecker()
        self.fetch_imports = FetchImports()
        self.code_dir = self.dir.directories['code']
        self.code_file_path = self.dir.paths['code']


    def load_notebook(self, file_path):
        """Loads the notebook from the specified file path."""

        try : 
            with open(file_path, "r", encoding="utf-8") as f:
                notebook = nbformat.read(f, as_version=4)
            return notebook
        
        except : 
            print(f"{file_path} couldn't open notebook")

    def extract_code_cells(self, notebook):
        """Extracts code cells from a Jupyter notebook."""
        return [cell.source for cell in notebook.cells if cell.cell_type == "code"]

    def code_check(self, titles_used : dict, additional_files : dict):
        """Checks the code files in the 'code' directory for issues."""

        error = {}

        for code_file in self.code_dir:

            error_msg = []
            
            file_path = f"{self.code_file_path}{code_file}"
            notebook = self.load_notebook(file_path) 
            # Extract code cells from the notebook
            code_cells = self.extract_code_cells(notebook)

            # Task Id
            key = code_file.split('.')[0]

            # Check if there are more than one code cell
            flag = False
            len_code_cells = len(code_cells)

            if len_code_cells != 1 and  not key in additional_files :
                error_msg.append('Additional File is used but not configured in metadata\n')

            code_to_check = code_cells[1] if len(code_cells) > 1 else code_cells[0]
            imports_used = self.fetch_imports.fetch_imports(code_to_check)
            unused_imports = self.import_checker.check_unused_imports(imports_used, code_to_check)

            
            try : 
                metadata_title = titles_used[key] 
            except : 
                metadata_title = ""

            if unused_imports :
                false_imports = ', '.join(unused_imports)
                error_msg.append(f'Unused Imports included : {false_imports} \n') 

            if metadata_title not in code_to_check :
                error_msg.append (f"The title in the metadata is {metadata_title} and the title in the code is different\n")


            if error_msg : 
                msg =  '\n '.join(error_msg) 
                error[key] = msg

        return error


if __name__ == '__main__' :
    cc = CodeCheck()
    cc.code_check()
