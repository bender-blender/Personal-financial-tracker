import sqlite3



class DataBase:
    
    def __init__(self):
        self.bd = sqlite3.connect("finance.db")
        self.cursor = self.bd.cursor()
        self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value REAL,
        type TEXT NOT NULL,
        time TEXT
        )
        """)
        self.bd.commit()
    
    def add_transaction(self, name:str, value:float, type_transaction:str, time:str):
        """
        Добавить транзакцию
        """
        
        self.cursor.execute(
        """
        INSERT INTO transactions (name, value, type, time)
        VALUES (?, ?, ?, ?)
        """,(name,value,type_transaction,time))
        self.bd.commit()

    def remove_transaction(self, value:int):
        """Удалить транзакцию
        Можно по имени или индексу       
        """
        
        if not isinstance(value,int):
            raise Exception("value must be str or int")
        

        
        self.cursor.execute(
            """
            DELETE FROM transactions WHERE id = ?
            """,(value,)
        )
        self.bd.commit()
        
    
    def get_everything(self):
        """
        Посмотреть все транзакции
        """
        data = {}
        self.cursor.execute("SELECT * FROM transactions")

        rows = self.cursor.fetchall()
        for row in rows:
            data[row[0]] = row[1:]  
        return data