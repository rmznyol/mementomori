import pandas as pd


class DataCollection():
    def __init__(self):
        self.df_dict = dict()
        self.years = set()
        self.dataframe = self.get_dataframe()

    def get_years(self):
        print(
            'Please enter the sequence of years (between 2005 and 2015) e.g. 2015 . Enter blank to end the sequence or enter all to get all data sets:')
        while True:
            year = input(
                'Please enter the sequence of years (between 2005 and 2015), enter blank to end the sequence or enter all to get all data sets:')
            if year == 'all':
                self.years = set([i for i in range(2005, 2016)])
                break
            if len(year) == 0:
                print("You entered blank, sequence is ended. The data from the following years will be loaded into memory:")
                break
            try:
                year = int(year)
            except ValueError:
                print('Please enter valid integer value')
                continue
            if 2005 <= year <= 2015:
                self.years.add(str(year))
            else:
                print('Valid range is: 2005-2015')
            if len(self.years) > 10:
                print('All data sets will be installed')
                break
            print('Current set of years :' ,self.years)
        print(self.years)

    def get_dataframe(self):

        self.get_years()

        for year in self.years:
            self.df_dict[f'df_{year}'] = pd.read_csv(f'data/{year}_data.csv')
        df = pd.concat(self.df_dict.values())

        df_json = pd.read_json(f'data/2015_codes.json')
        causes_113 = df_json[df_json['113_cause_recode'].isnull() == False]['113_cause_recode']
        causes_113.index = list(map(int, causes_113.index))
        causes_113.name = '113_cause_recode_json'
        # extract unnatural causes labels
        unnatural_causes = causes_113.index[111:]

        return (df,causes_113[unnatural_causes])
