import pandas as pd


class ExploreData:
    """Data Exploration"""

    def __init__(self, data, id_data):

        self.data = data
        self.id_data = id_data

        self.df = self.import_data()
        self.id_dfs = self.get_id_dfs()

    def import_data(self):
        """Import CSV Data"""
        try:
            df = pd.read_csv(self.data)
            return df
        except Exception as exp:
            err = self.errObj.handle_error(str(exp))
            print(str(err))

    def get_id_dfs(self):
        """Get list of id mappings in dataframe"""
        try:
            df = pd.read_csv(self.id_data, header=None)
            rows = df.to_numpy().tolist()

            ids = []
            id = []
            for row in rows:
                if not pd.isnull(row[0]):
                    id.append(row)
                else:
                    df = pd.DataFrame(id)
                    df.columns = df.iloc[0]
                    df = df[1:]
                    id = []
                    ids.append(df)

            df = pd.DataFrame(id)
            df.columns = df.iloc[0]
            df = df[1:]
            ids.append(df)
            return ids

        except Exception as exp:
            err = self.errObj.handle_error(str(exp))
            print(str(err))

    def get_mapped_ids(self, feature, list):
        """Get Ids of the list of Features"""
        ids = []
        for df in self.id_dfs:
            if df.columns[0] == feature:
                for item in list:
                    list_items = df[df[df.columns[1]] == item]
                    ids.append(int(list_items[feature].iloc[0]))
        return ids

    def drop_samples(self, df, feature, items_list):
        """Drop Samples"""
        drop_index_list = []
        for num in items_list:
            list_items = df[df[feature] == num].index.tolist()
            for item in list_items:
                if not item in drop_index_list:
                    drop_index_list.append(item)

        df.drop(drop_index_list, inplace=True)
        return df

    def calc_prevalence(self, y_actual):
        return round(sum(y_actual) / len(y_actual), 2)

