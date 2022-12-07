from sklearn.preprocessing import FunctionTransformer
import pandas as pd
import numpy as np




class DataPreprocesor:
    """
    This is a class for data cleaning and transforming data sets

    Attributes:
        categorical (List(str)): The list of categorical variables.
        continuous (List(str)): The list of categorical variables.
        education_dict : Convetion dictionary for education

    Returns One Hot Encoded features with Converted Education Column
    """

    def __init__(self, categorical=None, continuous= None, target_column='unnatural'):
        if categorical == None:
            categorical =['marital_status','sex']
        if continuous == None:
            continuous =['education_2003_revision','detail_age']

        self.categorical = list(categorical)
        self.continuous = list(continuous)
        self.features = self.categorical + self.continuous + [target_column]
        self.education_dict = {99: 9}
        for education_1989_revision in range(18):
            if education_1989_revision <= 8:
                education_2003_revision = 1
            elif education_1989_revision <= 11:
                education_2003_revision = 2
            elif education_1989_revision <= 12:
                education_2003_revision = 3
            elif education_1989_revision <= 13:
                education_2003_revision = 4
            elif education_1989_revision <= 15:
                education_2003_revision = 5
            elif education_1989_revision <= 16:
                education_2003_revision = 6
            elif education_1989_revision <= 17:
                education_2003_revision = 7
            self.education_dict[education_1989_revision] = education_2003_revision

    def one_hot_encoder(self, df):
        list_of_features = self.categorical
        df_copy = df.copy()

        for feature in list_of_features:
            temp = pd.get_dummies(
                df_copy[[feature]])  # There is a difference between df_copy[[feature]] and df_copy[feature],
            returned_features = list(
                temp.columns)  # the former gives , e.g, 'marital_status_M' instead of M. This is to avoid overlapping names and get strings instead of value M
            returned_features.pop()
            df_copy[returned_features] = temp[returned_features]
        return df_copy.drop(columns=list_of_features)

    def get_one_hot_coded_data(self, df):
        one_hot_transformer = FunctionTransformer(lambda df: self.one_hot_encoder(df))
        return one_hot_transformer.transform(df)

    def education_convertor(self, df):
        df_copy = df.copy()
        df_copy['education'] = df_copy['education_2003_revision'].fillna(df_copy['education_1989_revision'].map(self.education_dict))
        return df_copy

    def drop_actual_nans(self,df):
        df_copy = df.copy()
        df_copy.loc[df_copy['detail_age'] == 999, 'detail_age'] = np.nan  # Identify the missing values
        df_copy.loc[df['education'] == 9, 'education'] = np.nan
        print('\t Number of dropped datapoints for detail_age column:', (df_copy['detail_age'].isna()).sum(), '\n\n',
              '\t Number of dropped datapoints for education column: ', (df_copy['education'].isna()).sum(), '\n\n')
        df_copy.dropna(subset=['detail_age', 'education'], inplace=True)

        return df_copy

    def get_clean_data_and_features(self,df):
        features_of_interes = self.features + ['education_1989_revision']
        df = df[features_of_interes]
        converted_data = self.education_convertor(df)
        features_of_interes.remove('education_1989_revision')
        features_of_interes.remove('education_2003_revision')
        features_of_interes.append('education')
        clean_data = self.drop_actual_nans(converted_data[features_of_interes])
        one_hot_coded_data = self.get_one_hot_coded_data(clean_data)
        features = list(one_hot_coded_data.columns)
        features.remove('unnatural')
        return (one_hot_coded_data,features)


