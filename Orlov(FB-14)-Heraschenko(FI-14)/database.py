from typing import List
from typing import Dict
from prettytable import PrettyTable
from functools import cmp_to_key
from typing import Optional
from colorama import Back
from PrettyPrint import PrettyPrintTree

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
            print("ERROR! Table {tableName} already exists")
            return
        print(f"Table {tableName} has been created")

    def insertInto(self, tableName: str, params):
        if tableName not in self.tables:
            print(f"Table {tableName} not found...")
            return
        if(self.tables[tableName].insert_into(params)):
            print(f"1 row has been inserted into {tableName}")

    def select(self, tableName, params):
        if tableName not in self.tables:
            print(f"Table {tableName} not found...")
            return
    
        if self.validateSelectInput(self.tables[tableName],params):
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

    def validateSelectInput(self, table, params:List)->bool:
        if params[0] is not None and params[0] not in table.columns:
            print( f"Column '{params[0]}' does not exist in table '{table.tableName}'.")
            return False

        if params[1] is not None and params[1][0]!='"' and params[1] not in table.columns:
            print ( f"Column '{params[1]}' does not exist in table '{table.tableName}'.")
            return False

        if params[2] is not None and params[2] not in [0,-1,1]:
            print(f'Where wit code {params[2]} operation is not allowed.')
            return False

        if params[3] is not None:
            for column,order in params[3]:
                if column not in table.columns:
                     print ( f"Column '{column}' does not exist in table '{table.tableName}'.")
                     return False
                
        return True




class Table:
    def __init__(self, tableName: str, params: Dict) -> None:
        self.tableName = tableName
        self.data = []
        self.columns = []
        self.indexes = {}
        for column in params:
            if column[1]:
                self.indexes[column[0]] = BlackRedTree()
            self.columns.append(column[0])

    def insert_into(self, values)->bool:
        if len(values) == len(self.columns):
            row = dict(zip(self.columns, values))
            self.data.append(row)

            for index_column in self.indexes.keys():
                row_id = len(self.data) - 1
                index_value = row[index_column]
                if index_column in self.indexes:
                    self.indexes[index_column].insert(index_value, row_id)
                else:
                    index_tree = BlackRedTree()
                    index_tree.insert(index_value, row_id)
                    self.indexes[index_column] = index_tree
            return True
        else:
            print("Number of values does not match the number of columns.")
            return False

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
                    f"ERROR! Column {where_column} or {where_value} doesn't exist in table '{self.tableName}"
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
            row_ids = index_tree.root.search(where_value)
        elif sign == 1:
            row_ids = index_tree.root.search_values_greater_than_asc(where_value)
        else:
            row_ids = index_tree.root.search_values_less_than_asc(where_value)
        return self.get_values_at_indexes(row_ids)

    def compare_by_index_desc(self, where_column, where_value, sign):
        index_tree = self.indexes[where_column]
        if sign == 0:
            row_ids = index_tree.root.search(where_value)
        elif sign == 1:
            row_ids = index_tree.root.search_values_greater_than_desc(where_value)
        else:
            row_ids = index_tree.root.search_values_less_than_desc(where_value)
        return self.get_values_at_indexes(row_ids)

    def get_values_at_indexes(self, indixes):
        values = []
        for index in indixes:
            if 0 <= index < len(self.data):
                values.append(self.data[index])
            else:
                values.append(None)
        return values


class Node:
    def __init__(self, value=None, parent = None, color = 'R'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = parent
        self.data = []

    #def insert(self, value, data):
    #    if self.value is None:
    #        self.value = value
    #        self.data.append(data)
    #    elif value < self.value:
    #        if self.left is None:
    #            self.left = Node(value, parent = self, root = self.root)
    #        self.left.insert(value, data)
    #    elif value > self.value:
    #        if self.right is None:
    #            self.right = Node(value, parent = self, root = self.root)
    #        self.right.insert(value, data)
    #    else:
    #        self.data.append(data)

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

class BlackRedTree:
    def __init__(self):
        self.NIL = Node('O_O') #leafs of blackredtree
        self.NIL.color = 'B'
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL

    def rotateLeft(self,x):
        y = x.right
        x.right = y.left

        if(y.left != self.NIL):
            y.left.parent = x
        y.parent = x.parent
        if(x.parent == None):
            self.root = y
        elif(x == x.parent.left):
            x.parent.left = y
        else: 
            x.parent.right = y
        y.left = x
        x.parent = y
       
    
    def rotateRight(self,x):
        y = x.left
        x.left = y.right
        
        if(y.right != self.NIL):
            y.right.parent = x
        y.parent = x.parent
        if(x.parent == None):
            self.root = y
        elif(x == x.parent.right):
            x.parent.right = y
        else: 
            x.parent.left = y
        y.right = x
        x.parent = y
    

    def fix(self, node):
        while(node.parent and node.parent.color == 'R'):
            if(node.parent == node.parent.parent.left):
                uncle = node.parent.parent.right
                if(uncle.color == 'R'):
                    node.parent.color = 'B'
                    uncle.color = 'B'
                    node.parent.parent.color = 'R'
                    node = node.parent.parent
                else:
                    if(node == node.parent.right):
                        node = node.parent
                        self.rotateLeft(node)
                    node.parent.color = 'B'
                    node.parent.parent.color = 'R'
                    self.rotateRight(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if(uncle.color == 'R'):
                    node.parent.color = 'B'
                    uncle.color = 'B'
                    node.parent.parent.color = 'R'
                    node = node.parent.parent
                else:
                    if(node == node.parent.left):
                        node = node.parent
                        self.rotateRight(node)
                    node.parent.color = 'B'
                    node.parent.parent.color = 'R'
                    self.rotateLeft(node.parent.parent)
            if(node == self.root):
                break
        self.root.color = 'B'
                


    def insert(self,value, data):
        node = Node(value)
        node.right = self.NIL
        node.left = self.NIL
        node.data.append(data)
        y = None
        x = self.root
        while(x != self.NIL):
            y = x
            if(node.value < x.value):
                x = x.left
            elif(node.value > x.value):
                x = x.right
            else:
                x.data.append(data)
                return
        node.parent = y
        if(y == None):
            self.root = node
        elif(node.value < y.value):
            y.left = node
        else:
            y.right = node
        self.fix(node)

        
            
    