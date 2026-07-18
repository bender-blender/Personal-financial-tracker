import pandas as pd
from weasyprint import HTML
from sqlalchemy import create_engine

from db.database import DataBase


class File:
    
    def __init__(self,db:DataBase):
        self.db = db
        self.engine = create_engine('sqlite:///finance.db')

    def to_excel(self):
        df = pd.read_sql_table('transactions', self.engine)
        df = pd.read_sql('SELECT * FROM transactions', self.engine)
        df.to_excel('my_table.xlsx', index=False, sheet_name='Data')
    
    def to_pdf(self):
        df = pd.read_sql_table('transactions', self.engine)
        df = pd.read_sql(f'SELECT * FROM transactions', self.engine)

        html = df.to_html(index=False)
        HTML(string=html).write_pdf('my_table.pdf')