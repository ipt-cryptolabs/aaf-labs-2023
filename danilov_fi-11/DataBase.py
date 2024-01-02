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

        if select_command.where_condition:
            rows = self._apply_where_condition(rows, columns, select_command.where_condition, table_name)


        if select_command.group_by_columns:
            rows, columns = self._apply_group_by(rows, columns, select_command, table_name)

        table = PrettyTable()
        table.field_names = columns
        for row in rows:
            table.add_row(row)

        return table.get_string()  


    def _apply_where_condition(self, rows, columns, where_condition, table_name):
        col1 = where_condition.left_column
        col2_or_value = where_condition.right_operand
        col1_idx = columns.index(col1)
        
        if col2_or_value.startswith('"') and col2_or_value.endswith('"'):
            value = col2_or_value.strip('"')
            if col1 in self.indexes[table_name]:
                index = self.indexes[table_name][col1]
                row_indices = []
                for key in index.irange(maximum=value, inclusive=(False, False)):
                    row_indices.extend(index[key])              
                rows = [self.tables[table_name]['rows'][i] for i in row_indices]
                
            else:
                rows = [row for row in rows if row[col1_idx] < value]
                
        elif col2_or_value in columns:
            col2_idx = columns.index(col2_or_value)
            rows = [row for row in rows if row[col1_idx] < row[col2_idx]]

        return rows
    

    def _apply_group_by(self, rows, columns, select_command, table_name):

        group_by_indices = [columns.index(col) for col in select_command.group_by_columns]
        grouped_rows = {}
        indexed_group_by = all(col in self.indexes[table_name] for col in select_command.group_by_columns)

        if indexed_group_by:
            for col in select_command.group_by_columns:
                index = self.indexes[table_name][col]
                for value, row_indices in index.items():
                    key = (value,)
                    if key not in grouped_rows:
                        grouped_rows[key] = [self.tables[table_name]['rows'][i] for i in row_indices]
                    else:
                        grouped_rows[key].extend([self.tables[table_name]['rows'][i] for i in row_indices])

        else:
            for row in rows:
                key = tuple(row[idx] for idx in group_by_indices)
                if key not in grouped_rows:
                    grouped_rows[key] = []
                grouped_rows[key].append(row)

        aggregated_rows = []
        for key, group in grouped_rows.items():
            aggregated_row = list(key)
            for agg_function, agg_column in select_command.agg_functions:
                agg_col_idx = columns.index(agg_column)
                values = [row[agg_col_idx] for row in group]

                if agg_function == 'COUNT':
                    aggregated_row.append(len(values))
                elif agg_function == 'MAX':
                    aggregated_row.append(max(values))
                elif agg_function == 'LONGEST':
                    longest_value = max(values, key=len)
                    aggregated_row.append(longest_value)
            aggregated_rows.append(aggregated_row)
        rows = aggregated_rows

        new_columns = select_command.group_by_columns + [f'{func}({col})' for func, col in select_command.agg_functions]
        return aggregated_rows, new_columns
