import pandas as pd
import numpy as np

pd.set_option('mode.chained_assignment', None)


class InputOptimziation:
    '''Input Optimization Class'''

    def __init__(self):
        '''Constructor'''

    def load_files(self, csv_data):
        # 1. Load Diabetics Data
        missing_values = ['?', ' ']
        df_data = pd.read_csv(csv_data, na_values=missing_values, low_memory=False,
                              dtype={'payer_code': 'category'})

        # 2. Read ICD Data
        csv_icd = 'data/icd.csv'
        df_icd = pd.read_csv(csv_icd)

        return df_data, df_icd

    def make_revisit(self, df):
        """Add Revisit Count Column"""
        # df_revisit = df['patient_nbr'].value_counts()
        dfp = df.copy()
        # for index, val in df_revisit.iteritems():
        #     print(index, val)
        #     dfp = dfp.copy()
        #     patient_nbr = index
        #     filter_visit = dfp['patient_nbr'] == patient_nbr
        #     dfp['patient_nbr'][filter_visit] = val

        # self.data['RevisitCount'] = self.data.patient_nbr.groupby(self.data.patient_nbr).transform('count')
        dfp['RevisitCount'] = dfp.patient_nbr.groupby(df['patient_nbr']).transform('count')

        return dfp

    def drop_revisit(self, df):
        """Dropping revist more than 2"""
        df_revisit = df['patient_nbr'].value_counts()
        df_visit = df_revisit[df_revisit > 2]
        rows = df_visit.shape[0]
        filter_not_readmitted = df['readmitted'] != 'NO'

        dfp = df.copy()
        for num in range(0, rows):
            dfp = dfp.copy()
            patient_nbr = df_revisit[df_revisit > 2].index[num]
            filter_visit = dfp['patient_nbr'] == patient_nbr
            filter_not_readmitted = dfp['readmitted'] != 'NO'
            df_filter_visit = dfp[filter_visit & filter_not_readmitted][1:]
            dfp = dfp.drop(df_filter_visit.index)
            print(num, '/', rows)

        return dfp

    def fill_nan(self, data, column, value):
        """Fill Nan with 0"""
        data = data[column].fillna(value, inplace=True)
        return data

    def filter_rows(self, data, feature):
        """To filter numerical rows"""

        # 1. Filter Non-Numerical Rows
        filter_numeric = pd.to_numeric(data[feature], errors='coerce').notnull()
        df_num = data[filter_numeric]
        df_num[feature] = df_num[feature].astype(float)

        # 2. Filter Numerical Rows
        filter_non_numeric = pd.to_numeric(data[feature], errors='coerce').isnull()
        df_non_num = data[filter_non_numeric]

        return df_num, df_non_num

    def map_icd(self, icd, data, feature):
        """To map numerical rows"""

        # 1. Map Non-Numerical Rows
        df_num, df_non_num = self.filter_rows(data, feature)
        df_non_num[feature] = 'External Injury'

        frames = [df_num, df_non_num]
        data = pd.concat(frames)

        # 2. Map Numerical Rows
        for index, row in icd.iterrows():
            data_process = data.copy()
            # Read ICD inputs
            disease = row['disease']
            low = row['start']
            high = row['end']

            additional = str(row['additional']).split(',')
            additional = [float(i) for i in additional]

            # Filter Numerical
            df_num, df_non_num = self.filter_rows(data_process, feature)
            filter_low = df_num[feature] >= low
            filter_high = df_num[feature] <= high
            filter_additional = df_num[feature].isin(additional)
            df_num[feature][(filter_low & filter_high) | filter_additional] = disease

            frames = [df_num, df_non_num]
            data = pd.concat(frames)

        return data

    def remove_expired(self, data):
        # 7. Drop Expired Rows
        expired_list = [11, 19, 20, 21]
        filter_expired = ~data['discharge_disposition_id'].isin(expired_list)
        df_expired = data[filter_expired]

        return df_expired


def main():
    """Main Function"""

    # df_data, df_icd = load_files()
    # fill_nan(df_data)

    # df_data = map_icd(df_icd, df_data, 'diag_1')
    # df_data = map_icd(df_icd, df_data, 'diag_2')
    # df_data = map_icd(df_icd, df_data, 'diag_3')
    # df_data = make_revisit(df_data)
    # df_data = drop_revisit(df_data)
    # df_data = remove_expired(df_data)
    # df_data.to_csv('data/input_optimized.csv', index=False)
    # df_data.to_csv('data/train_input.csv', index=False)

    debug = 0


if __name__ == '__main__':
    main()
