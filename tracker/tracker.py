import pandas

from datetime import datetime

from db import DataBase
from collections import defaultdict

class Tracker:

    def __init__(self):
        self.db = DataBase()
    

    def __filter_pattern(self, field, operator, value):
        """Универсальный метод фильтрации."""
        allowed_operators = {"=", ">", "<", ">=", "<=", "!="}

        if operator not in allowed_operators:
            raise ValueError("Недопустимый оператор")

        self.db.cursor.execute(
            f"SELECT * FROM transactions WHERE {field} {operator} ?",
            (value,)
        )
        return self.db.cursor.fetchall()


    def add_transaction(self,name:str, value:float, type_transaction="Доход", time=f"{datetime.now().strftime("%Y-%m-%d")}"):
        """Добавить транзакцию
        """
        if type_transaction == "Расход":
            value = -value
        
        self.db.add_transaction(name, value, type_transaction, time)
    
    def remove_transaction(self,value:int):
        """Удалить транзакцию
        """
        self.db.remove_transaction(value)
    
    def get_transaction(self):
        """Получить все транзакции
        """
        return self.db.get_everything()
    

    def current_balance(self):
        """Текущий баланс
        """
        total = 0
        data = self.get_transaction()
        for value in data.values():
            total += value[1]
        return total
    
    def filter_by_name(self, name):
        """Фильтр по названию."""
        return self.__filter_pattern("name","=",name)


    def filter_by_type(self, transaction_type):
        """Фильтр по типу транзакции."""
        return self.__filter_pattern("type","=",transaction_type)


    def filter_by_time(self, time, sign="="):
        """Фильтр по времени."""
        return self.__filter_pattern("time",sign,time)


    def filter_value(self, value, sign="="):
        """Фильтер по сумме
        """
        return self.__filter_pattern("value", sign, value)
    
    def all_time_statistics(self):
        """Статистика за все время
        """
        names = ["Доходы","Расходы"]
        income_expenses = [0,0]
        data = self.get_transaction()
        for value in data.values():
            if value[2] == "Доход":
                income_expenses[0] += value[1]
            else:
                income_expenses[1] += abs(value[1])
        return names,income_expenses
    
    def advanced_statistics(self,transaction_type="Доход"):
        """Общая стастика
        """
        filter_type = self.filter_by_type(transaction_type)
        for_pie = defaultdict(int)
        for_line = defaultdict(list)
        
        for row in filter_type:
            for_pie[row[1]] += abs(row[2])
            for_line[row[1]].append(abs(row[2]))
        
        return for_line,for_pie
    
    # def forecast(self):
    #     pass