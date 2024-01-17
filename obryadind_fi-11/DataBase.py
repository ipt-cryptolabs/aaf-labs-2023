from prettytable import PrettyTable
from sortedcontainers import SortedDict

class Database:
    def __init__(self):
        self.tables = {}
        self.indexes = {}
    
    def create_table(self, create_command):
        table_name = create_command.table_name

        if table_name in self.tables:
            return f"Table {table_name} already exists."
        
        self.tables[table_name] = {
            "columns": [],
            "rows": []
        }
        self.indexes[table_name] = {}

        for col_name, col_info in create_command.columns:
            self.tables[table_name]["columns"].append(col_name)           
            if col_info:
                self.indexes[table_name][col_name] = SortedDict()

        return f"Table {table_name} has been created."

    def insert_into_table(self, insert_command):
        table_name = insert_command.table_name

        if table_name not in self.tables:
            return f"Table {table_name} does not exist."
        
        if len(insert_command.values) != len(self.tables[table_name]["columns"]):
            return "The number of values does not match the number of columns."

        row_index = len(self.tables[table_name]["rows"])
        self.tables[table_name]["rows"].append(insert_command.values) 

        for i, value in enumerate(insert_command.values):
            column_name = self.tables[table_name]["columns"][i]
            if column_name in self.indexes[table_name]:
                self.indexes[table_name][column_name].setdefault(value, []).append(row_index)
        
        return f"1 row has been inserted into {table_name}."        


    def select_from_table(self, select_command):
        table_name = select_command.table_name

        if table_name not in self.tables:
            return f"Table {table_name} does not exist."
    
        rows = self.tables[table_name]["rows"]
        columns = self.tables[table_name]['columns']

        # Apply WHERE condition
        if select_command.where_condition:
            column_name, operator, value = select_command.where_condition
            column_index = columns.index(column_name)

            # Strip quotation marks if value is a string literal
            if value.startswith('"') and value.endswith('"'):
                value = value.strip('"')
            else:
                # Convert to number if it's numeric
                value = float(value) if '.' in value else int(value)
                
            # Check if column data is numeric or string
            is_numeric = all(row[column_index].replace('.', '', 1).isdigit() for row in rows if row[column_index])
    
            # Convert value to the appropriate type
            if is_numeric:
                value = float(value) if '.' in value else int(value)
    
            # Apply the condition
            if operator == '>':
                if is_numeric:
                    rows = [row for row in rows if float(row[column_index]) > value]
                else:
                    rows = [row for row in rows if row[column_index] > value]
    
        # Apply ORDER_BY clause
        if select_command.order_by_clause:
            for col_name, order in reversed(select_command.order_by_clause):
                column_index = columns.index(col_name)
                # Determine sort key type (numeric or string)
                is_numeric = all(row[column_index].replace('.', '', 1).isdigit() for row in rows if row[column_index])
                key_func = lambda row: float(row[column_index]) if is_numeric else row[column_index]
                rows.sort(key=key_func, reverse=(order == 'DESC'))
    
        # Generate table output
        table = PrettyTable()
        table.field_names = columns
        for row in rows:
            table.add_row(row)
    
        return table.get_string()


    def _apply_where_condition(self, rows, columns, where_condition, table_name):
        if where_condition:
            col1, operator, col2_or_value = where_condition
            col1_idx = columns.index(col1)
        
            # Assuming only string literals and direct column comparisons
            if col2_or_value.startswith('"') and col2_or_value.endswith('"'):
                value = col2_or_value.strip('"')
                if operator == '>':
                    if col1 in self.indexes[table_name]:
                        index = self.indexes[table_name][col1]
                        row_indices = []
                        for key in index.irange(minimum=value, inclusive=(False, False)):
                            row_indices.extend(index[key])
                        rows = [self.tables[table_name]['rows'][i] for i in row_indices]
                    else:
                            rows = [row for row in rows if row[col1_idx] > value]
            # Add more conditions for different operators if needed

            elif col2_or_value in columns:
                col2_idx = columns.index(col2_or_value)
                if operator == '>':
                    rows = [row for row in rows if row[col1_idx] > row[col2_idx]]
            # Add more conditions for different operators if needed

        return rows
        

    def _apply_order_by(rows, columns, order_by_columns):
        if order_by_columns:
            def sorting_key(row):
                key = []
                for col, order in order_by_columns:
                    col_index = columns.index(col)
                    value = row[col_index]
                    # Reverse the value for descending order
                    if order == 'DESC':
                        value = -value if isinstance(value, (int, float)) else value[::-1]
                        key.append(value)
                    return tuple(key)

            rows.sort(key=sorting_key)

        return rows
    
    
