from typing import List
from typing import Dict
from prettytable import PrettyTable
from functools import cmp_to_key
from typing import Optional


class Database:
    def __init__(self) -> None:
        self.tables = {}

    def execute(self, command: str, tableName, params: List):
        if command.lower() == "create":
            self.createTable(tableName, params)
        elif command.lower() == "insert":
            self.insertInto(tableName, params)
        elif command.lower() == "select":
            self.select(tableName, params)
        else:
            print("ERROR! Command is not supported")

    def createTable(self, tableName: str, params):
        if tableName not in self.tables.keys():
            self.tables[tableName] = Table(tableName, params)
        else:
            print("ERROR! Table {tableName} exists")
            return
        print("Table {tableName} has been created")

    def insertInto(self, tableName: str, params):
        if tableName not in self.tables:
            print("Table {tableName} not found...")
            return
        self.tables[tableName].insert_into(params)
        print("1 row has been inserted into {tableName}")

    def select(self, tableName, params):
        if tableName not in self.tables:
            print("Table {tableName} not found...")
            return
    
        data = self.tables[tableName].select_from(
            params[0], params[1], params[2], params[3]
        )
        self.printResult(data)
        

    def printResult(self, data:Dict):
        table = PrettyTable()
        if len(data)>0:
            table.field_names = data[0].keys()

            for row in data:
                table.add_row(row.values())

            print(table)
        else:
            print('Rows not found...')


class Table:
    def __init__(self, tableName: str, params: Dict) -> None:
        self.tableName = tableName
        self.data = []
        self.columns = []
        self.indexes = {}
        for column in params:
            if column[1]:
                self.indexes[column[0]] = BinarySearchTree()
            self.columns.append(column[0])

    def insert_into(self, values):
        if len(values) == len(self.columns):
            row = dict(zip(self.columns, values))
            self.data.append(row)

            for index_column in self.indexes.keys():
                row_id = len(self.data) - 1
                index_value = row[index_column]
                if index_column in self.indexes:
                    self.indexes[index_column].insert(index_value, row_id)
                else:
                    index_tree = BinarySearchTree()
                    index_tree.insert(index_value, row_id)
                    self.indexes[index_column] = index_tree
        else:
            print("Number of values does not match the number of columns.")

    # Function to select rows from a table with an index
    def select_from(
        self, where_column:  Optional[str] = None, where_value: Optional[str] = None, sign: Optional[int] = None, order_by_column: Optional[List] = None
    ):
        if where_column is None:
            if order_by_column is not None:
                return self.sort_only(order_by_column)
            else:
                return self.data

        if where_value[0] != '"':
            if where_column not in self.columns or where_value not in self.columns:
                print(
                    "ERROR! Column {where_column} or {where_value} doesn't exist in table '{self.tableName}"
                )
                return None

            results = self.compare_with_column(where_column, where_value, sign)
            if len(order_by_column):
                results = self.custom_sort(results, order_by_column)
            return results

        else:
            where_value = where_value.strip('"')
            needs_ordering = True

            if where_column in self.columns:
                if where_column in self.indexes:
                    if (
                        len(order_by_column) == 1
                        and where_column == order_by_column[0][0] == -1
                    ):
                        needs_ordering = False

                    if len(order_by_column) and order_by_column[0][1]:
                        results = self.compare_by_index_desc(where_column,where_value,sign)
                    else:
                        results = self.compare_by_index_asc(where_column,where_value,sign)

                else:
                    results = self.compare_with_value(where_column, where_value, sign)
            else:
                print(
                    f"Column '{where_column}' does not exist in table '{self.tableName}'."
                )

            print(order_by_column)
            if needs_ordering and len(order_by_column):
                results = self.custom_sort(results, order_by_column)

            return results

    def custom_sort(self,data, sort_columns):
        def custom_compare(item1, item2):
            for column, order in sort_columns:
                if item1[column] < item2[column]:
                    return -1 * order  # Multiply by -1 for descending order
                elif item1[column] > item2[column]:
                    return 1 * order
            return 0

        return sorted(data, key=cmp_to_key(custom_compare))

    def sort_only(self, order_by_column: List):
        return self.custom_sort(self.data,order_by_column)

    def compare_with_column(self, where_column1, where_column2, sign):
        if sign == 0:
            results = [
                row for row in self.data if row[where_column1] == row[where_column2]
            ]
        elif sign == 1:
            results = [
                row for row in self.data if row[where_column1] > row[where_column2]
            ]
        else:
            results = [
                row for row in self.data if row[where_column1] < row[where_column2]
            ]

        return results

    def compare_with_value(self, where_column: str, where_value: str, sign: int):
        if sign == 0:
            results = [row for row in self.data if row[where_column] == where_value]
        elif sign == 1:
            results = [row for row in self.data if row[where_column] > where_value]
        else:
            results = [row for row in self.data if row[where_column] < where_value]

        return results

    def compare_by_index_asc(self, where_column, where_value, sign):
        index_tree = self.indexes[where_column]
        if sign == 0:
            row_ids = index_tree.search(where_value)
        elif sign == 1:
            row_ids = index_tree.search_values_greater_than_asc(where_value)
        else:
            row_ids = index_tree.search_values_less_than_asc(where_value)
        return self.get_values_at_indexes(row_ids)

    def compare_by_index_desc(self, where_column, where_value, sign):
        index_tree = self.indexes[where_column]
        if sign == 0:
            row_ids = index_tree.search(where_value)
        elif sign == 1:
            row_ids = index_tree.search_values_greater_than_desc(where_value)
        else:
            row_ids = index_tree.search_values_less_than_desc(where_value)
        return self.get_values_at_indexes(row_ids)

    def get_values_at_indexes(self, indixes):
        values = []
        for index in indixes:
            if 0 <= index < len(self.data):
                values.append(self.data[index])
            else:
                values.append(None)
        return values


class BinarySearchTree:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None
        self.data = []

    def insert(self, value, data):
        if self.value is None:
            self.value = value
            self.data.append(data)
        elif value < self.value:
            if self.left is None:
                self.left = BinarySearchTree(value)
            self.left.insert(value, data)
        elif value > self.value:
            if self.right is None:
                self.right = BinarySearchTree(value)
            self.right.insert(value, data)
        else:
            self.data.append(data)

    def search(self, value):
        if self.value == value:
            return self.data
        elif value < self.value and self.left is not None:
            return self.left.search(value)
        elif value > self.value and self.right is not None:
            return self.right.search(value)
        else:
            return []

    def search_values_less_than_asc(self, value):
        result = []
        print(value, self.value)
        if self.value is not None:
            if self.value < value:
                if self.left:
                    result.extend(self.left.search_values_less_than_asc(value))
                result.extend(self.data)
                if self.right:
                    result.extend(self.right.search_values_less_than_asc(value))
        return result

    def search_values_greater_than_asc(self, value):
        result = []
        if self.value is not None:
            if self.left:
                result.extend(self.left.search_values_greater_than_asc(value))
            if self.value > value:
                result.extend(self.data)
            if self.right:
                result.extend(self.right.search_values_greater_than_asc(value))
        return result
    
    def search_values_greater_than_desc(self, value):
        result = []
        if self.value is not None:
            if self.right:
                result.extend(self.right.search_values_greater_than_desc(value))
            if self.value > value:
                result.extend(self.data)
            if self.left:
                result.extend(self.left.search_values_greater_than_desc(value))
        return result
    
    def search_values_less_than_desc(self, value):
        result = []
        if self.value is not None:
            if self.right:
                result.extend(self.right.search_values_less_than_desc(value))
            if self.value < value:
                result.extend(self.data)
            if self.left:
                result.extend(self.left.search_values_less_than_desc(value))
        return result
