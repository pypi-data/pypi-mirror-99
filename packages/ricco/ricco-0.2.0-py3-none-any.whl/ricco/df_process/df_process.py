# encoding:GBK
import geopandas as gpd
import pandas as pd
from ricco import rdf


from . import Base


class Geo_data_process(Base):
    '''������'''

    def to_geo_df(self):
        self.df = gpd.GeoDataFrame(self.df)
        return self.df


class Data_process(Base, Geo_data_process):
    '''Dataframe��������'''

    # ��������


# if __name__ == '__main__':
# df = rdf('�Ϻ����ص�λ.csv')
# df = '�Ϻ����ص�λ.csv'
#
# a = Data_process(df)
# a.reset2name()
# a.to_gbk('tes2.csv')
# a.rename({})
# a.to_geo_df()
# print(a.df)
