import re
from get_dir import DirLink


class CheckTitle :


    def scrape_title(self, input_string) -> str:

        if 'update_layout' in input_string : 

            target_idx = input_string.index('update_layout')
            input_string = input_string[target_idx : ]
            title_idx = input_string.index('title')

        else :
            try : 
                title_idx = input_string.index('title')
            except : 
                return "No Title"
        
        flag = False

        start_idx = - 1
        qutotation_used = ''
        end_idx = -1

        # Find the Qutotation
        cur_idx = title_idx
        while cur_idx :
            if input_string[cur_idx] in ['"', "'"] :
                qutotation_used  = input_string[cur_idx]
                start_idx = cur_idx + 1
                break
            cur_idx += 1

        cur_idx += 1

        # Determing 
        while input_string[cur_idx] != qutotation_used  :
            cur_idx += 1
        end_idx = cur_idx 

        return input_string[start_idx : end_idx]



if __name__ == '__main__' :

    code = """
    import matplotlib.pyplot as plt

    # Data
    data = [1, 2, 3, 4, 5, 56]

    # Create a simple plot
    plt.plot(data)
    plt.title('Plot of the List Data')  # Title of the plot
    plt.xlabel('Index')  # Label for the x-axis
    plt.ylabel('Value')  # Label for the y-axis

    # Show the plot
    plt.show()
    """

    ct = CheckTitle()
    title = ct.scrape_title(code)

    print(title)