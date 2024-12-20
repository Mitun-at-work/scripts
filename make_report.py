import pandas as pd

class MakeReport:

    def __init__(self):
        self.count = 0
        self.columns = ['Task Id', 'Task Link', 'Issue']
        self.dataframe = pd.DataFrame(columns=self.columns)

    def add_log(self, details_row):
        # Convert the list to a DataFrame and concatenate
        new_row = pd.DataFrame([details_row], columns=self.columns)
        self.dataframe = pd.concat([self.dataframe, new_row], ignore_index=True)
        self.count += 1

    def save_report(self):
        self.dataframe.to_excel('report.xlsx', index=False)

if __name__ == '__main__':
    report = MakeReport()
    report.add_log([1, 'http://tasklink.com', 'Some issue description'])
    report.save_report()