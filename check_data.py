from get_dir import DirLink

class CheckData :

    def  __init__(self):

        self.dir = DirLink()
        self.data_path = self.dir.paths['data']
        self.data_folder = self.dir.directories['data']

    def check_data(self) :
        
        error = {}
        for file in self.data_folder : 
            file_link = f"{self.data_path}{file}"
            with open(file_link, 'r') as csv_file :
                cont = csv_file.read()
                if cont[0] == ',' : 
                    error[file.split('.')[0]] = 'The Index Column Included in the Data File'

        return error
    
if __name__ == '__main__' :
    cd = CheckData()
    cd.check_data()