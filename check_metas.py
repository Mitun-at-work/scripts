from get_dir import DirLink
import pandas as pd

class CheckMeta:

    def __init__(self):

        dir_link = DirLink()
        self.path = dir_link.paths
        self.dir = dir_link.directories

        # Define the expected columns for metadata
        self.column_names = [
            "title", "language", "png", "code", "vector", "additional_files", "data"
        ]

        # Define prefix checks in a structured way
        self.prefix_checks = {
            'code': 'CodeDirectory/',
            'png': 'PNGDirectory/',
            'data': 'DataDirectory/'
        }

        self.title_used = {}
        self.additional_file_mentions = {}


    def check_meta(self):

        error_messages = {}
        for index, metadata in enumerate(self.dir["metadata"]):
            try : 
                msg = []
                df = pd.read_csv(f"{self.path['metadata']}/{metadata}")

                # Extract file name from the metadata
                file_name = metadata.split('.')[0]
                features, values = df["id"], df[file_name]

                # Unpack the values from the DataFrame row
                title, language_used, png_file, code_file, vector_file, additional_file, data_file = values

                # Strip
                title = title.strip()
                language_used = language_used.strip()
                png_file = png_file.strip()
                code_file = code_file.strip()
                data_file = data_file.strip()

                # Storing the ttle
                self.title_used[file_name] = title

                """
                    Checking for vector & Additional Files
                """
                if type(vector_file) != float and vector_file.strip().lower() != 'na' :
                    vector_file = vector_file.strip()
                else : vector_file = None

                if type(additional_file) != float and additional_file.strip().lower() != 'na' :
                    additional_file = additional_file.strip()
                else : additional_file = None

                """
                    Checking for Meta Data & Fields
                """
                if not all(features[idx] == col for idx, col in enumerate(self.column_names)):
                    msg.append("Metadata Fields Wrongly Specified \n")

                # Check for Python language
                if not language_used.lower().startswith('p'):
                    msg.append('Wrong language is specified \n')

                flag = False
                """
                    Checking for Prefixes
                """
                for key, prefix in self.prefix_checks.items():
                    
                    file_value = locals().get(f"{key}_file")
                    
                    if isinstance(file_value, str):
                        if not file_value.startswith(prefix):
                            flag = True
                            msg.append(f'{prefix} Prefix is not used \n')
                    
                    elif key == 'data':  
                        data_files = [x.strip() for x in data_file.split(',')]
                        for data_file_ in data_files:
                            if not data_file_.startswith(prefix):
                                flag = True
                                msg.append(f'{prefix} Prefix is not used for Data \n')

                # Check for Vector File Prefix
                if vector_file :
                    if not (vector_file.startswith('VectorDirectory/')) :
                            msg.append(f'VectorDirectory/ Prefix is not used for vector path \n')

                # Flag
                if flag : 
                    error_messages[file_name] = ','.join(msg)
                    continue

                """Check for Files bieng configured properly"""

                code_file_configuration = (code_file[14 : ] == f'{file_name}.ipynb')
                if not code_file_configuration:
                    msg.append(f"{code_file[14 : ]} is mentioned instead of {file_name}.ipynb \n")
                else :
                    if not f'{file_name}.ipynb' in self.dir['code'] : 
                        msg.append(f'The {file_name}.ipynb is missing from the directory \n')

                # Check for PNG File Specified
                code_file_configuration = (png_file[13 : ] == f'{file_name}.png')
                if not code_file_configuration :
                    msg.append(f"{png_file[13 : ]} is mentioned instead of {file_name}.png \n")
                else : 
                    if not f'{file_name}.png' in self.dir['png'] :
                        msg.append(f'{file_name}.png is missing from directory \n')

                # Check for Data File Specified
                if ',' in data_file :

                    data_split_files = data_file.split(',')
                    for idx, data_split_file_name in enumerate(data_split_files) :
                        data_split_file_name = data_split_file_name.strip()
                        data_file_configuration = data_split_file_name[14 : ] == f'{file_name}_{idx + 1}.csv'

                        if not data_file_configuration:
                            msg.append(f"{data_split_file_name[14: ]} is mentioned instead of {file_name}_{idx + 1}.csv \n")

                        else : 
                            if not f'{file_name}_{idx + 1}.csv' in self.dir['data'] :
                                msg.append(f'{file_name}_{idx + 1} data file is missing from the directory \n')


                else :
                    data_file_configuration = (data_file[14 : ] == f'{file_name}.csv')
                    if not data_file_configuration:
                        msg.append(f"{data_file[14 : ]} is mentioned instead of {file_name}.csv \n")
                    else : 
                        if not f'{file_name}.csv' in self.dir['data'] :
                          msg.append(f'{file_name}.csv data file is missing from directory \n')


                # Check for Vector File
                if vector_file :
                    vector_configuration = (vector_file[16 :] == f'{file_name}.html')
                    if not vector_configuration:
                        msg.append(f"{vector_file[16 : ]} is mentioned instead of {file_name}.html \n")
                    else : 
                        if not f'{file_name}.html' in self.dir['vector'] :
                            msg.append(f'{file_name}.html is missing from directory \n')

                # Check for Additional File
                if additional_file : 
                    """
                    Accessing Additional Files
                    """
                    if ',' in additional_file :
                        additional_file_striped = additional_file.split(',')
                    else : 
                        additional_file_striped = [additional_file]

                    for individual_additional_file in additional_file_striped :
                        
                        # Removing Unwanted Spaces
                        individual_additional_file = individual_additional_file.strip()

                        # Prefix Check
                        if not individual_additional_file.startswith("AdditionalFilesDirectory/")  :
                            msg.append('AdditionalFilesDirectory/ prefix is not used \n')
                        else :
                            if not individual_additional_file[25:] in self.dir['additional'] :
                                msg.append(f'{individual_additional_file[25:]} is missing from the directory \n')
                            
                            # Storing Results
                            target_additional_file = individual_additional_file[25 : ]
                            if file_name in self.additional_file_mentions : 
                                self.additional_file_mentions[file_name].append(target_additional_file) 
                            else : self.additional_file_mentions[file_name] = [target_additional_file]

                if msg :
                    error_messages[file_name] = ''.join(msg)
        
            except Exception as error : 
                error_messages[file_name] = f'The task Id mentioned in the Meta Data is wrong \n'
      

        return error_messages

if __name__ == '__main__':
    print(len(CheckMeta().check_meta()))
