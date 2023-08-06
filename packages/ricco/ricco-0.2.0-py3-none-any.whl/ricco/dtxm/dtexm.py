# encoding:GBK
import os

import pandas as pd
from ricco.dtxm.basic_tools import _Tools
from ricco.util import fn


class Dtexm(_Tools):

    def basic(self):
        '''���ݻ�����Ϣ����'''
        # ����
        self.add_bullet_list('������')
        self.add_normal_p('��'.join(self.df.columns))
        # �ļ�size
        self.add_bullet_list('�ļ��ߴ磺')
        self.add_normal_p(f'�У�{self.df.shape[0]}����{self.df.shape[1]}')
        # ������
        self.add_bullet_list('�������ͣ�')
        self.col_types = pd.DataFrame(self.df.dtypes, columns=['����']).reset_index().rename(columns={'index': '����'})
        self.add_df2table(self.col_types)

    def col_by_col(self):
        '''���м��'''
        for col in self.df.columns:
            self.add_bullet_list(col)
            self.add_normal_p(self.df[col].dtype)
            if (self.df[col].dtype == 'int64') | (self.df[col].dtype == 'float64'):
                self.serise_describe(col)
                self.hist_plot(col)
                self.add_normal_p('')
            elif (self.df[col].dtype == 'O'):
                self.object_describe(col)
                self.is_float(col)
                self.is_date(col)
                self.add_normal_p('')


    def save(self, savefilename: str = None):
        '''�����ļ���word�ĵ�'''
        if savefilename == None:
            if isinstance(self.filename, pd.DataFrame):
                raise FileNotFoundError('������Ҫ������ļ�·��')
            savefilename = fn(self.filename) + '-��ⱨ��.docx'
        self.doc.save(savefilename)
        print('�ļ�������', os.path.abspath(savefilename))

    def examine_all(self, savefilename: str = None):
        '''��������'''
        self.basic()
        self.col_by_col()
        self.save(savefilename=savefilename)


if __name__ == '__main__':
    doc = Dtexm('�ɽ�2.xlsx')
    doc.examine_all()
