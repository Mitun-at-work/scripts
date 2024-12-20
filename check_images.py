from pathlib import Path
from PIL import Image
from get_dir import DirLink


class ImageCheck:
    def __init__(self):
        # Define the path to the images
        self.dir = DirLink()

    def image_check(self):
        
        error = {}
        for img_path in self.dir.directories['png']:
            try  :

                image_file = img_path.split('.')[0]
                message = ''
                link  = f"{self.dir.paths['png']}/{img_path}"
                file_path = Path(link)

                cur_image = Image.open(file_path)
                width, height = cur_image.size
                
                if width < 1023 or height < 1023:
                    message += f"Image dimensions should be 1024 x 1024 px"

                file_size_mb = file_path.stat().st_size / (1024 * 1024)  

                if file_size_mb > 2:

                    message += f"Image size shouldn't be more than 2MB \n"

                if message : error[image_file] = message
            
            except Exception as e:
                error[image_file] = "Something went wrong. Please go through this image"        
        return error

if __name__ == '__main__' :
    ic = ImageCheck()
    ic.image_check()