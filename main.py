from check_files import CheckFile
from check_images import ImageCheck
from check_metas import CheckMeta
from check_code import CodeCheck
from check_data import CheckData
from make_report import MakeReport
from get_dir import DirLink
from check_image_simmilarities import ImageSimilarityChecker
from img_plotter import ImagePlotter

class TuringMultiModality :

    def __init__(self):
        
        self.dir = DirLink()

        self.data_checker = CheckData()
        self.code_checker = CodeCheck()
        self.metadata_checker = CheckMeta()
        self.image_checker = ImageCheck()
        self.make_report = MakeReport()
        self.image_simmilarity = ImageSimilarityChecker()
        self.image_plotter = ImagePlotter()


    def run(self) :
        
        final_summary = {}

        data_summary = self.data_checker.check_data()
        meta_summary = self.metadata_checker.check_meta()
        code_summary = self.code_checker.code_check(self.metadata_checker.title_used, self.metadata_checker.additional_file_mentions)
        image_summary = self.image_checker.image_check()
        image_simmilarity_summary = self.image_simmilarity.get_similar_images()

        self.image_plotter.plot_and_save(image_simmilarity_summary.keys())


        # Summaries
        summaries = [meta_summary, image_summary, code_summary, data_summary, image_simmilarity_summary]

        # Iterate through each dictionary
        for summary in summaries:
            for key, value in summary.items():
                if key in final_summary:
                    final_summary[key].append(value)
                else:
                    final_summary[key] = [value]

        for key, items in final_summary.items() :
            
            row = [key, f'https://labeling-g.turing.com/conversations/{key}/view']
            msg = ''
            for item in items :
                msg += f'{item} \n'
            row.append(msg)
            self.make_report.add_log(row)
        self.make_report.save_report()


if __name__ == '__main__' :
    TuringMultiModality().run()
