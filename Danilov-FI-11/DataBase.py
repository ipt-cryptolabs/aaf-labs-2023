from prettytable import PrettyTable

class Database:
    def __init__(self):
        self.tables = {}  # Store tables as dictionaries
    
    def create_table(self, create_command):
        table_name = create_command.table_name
        if table_name in self.tables:
            return f"Table {table_name} already exists."

        columns = [col_name for col_name, col_info in create_command.columns]
         
        self.tables[table_name] = {
            "columns": columns,
            "rows": []
        }
        return f"Table {table_name} has been created."
    
    def insert_into_table(self, insert_command):
        table_name = insert_command.table_name
        if table_name not in self.tables:
            return f"Table {table_name} does not exist."
        
        if len(insert_command.values) != len(self.tables[table_name]["columns"]):
            return "The number of values does not match the number of columns."
        
        self.tables[table_name]["rows"].append(insert_command.values)
        return f"1 row has been inserted into {table_name}."
    
    def select_from_table(self, select_command):
        table_name = select_command.table_name
        if table_name not in self.tables:
            return f"Table {table_name} does not exist."
        rows = self.tables[table_name]["rows"]
        columns = self.tables[table_name]['columns']

        if select_command.where_condition:
            col1 = select_command.where_condition.left_column
            col2_or_value = select_command.where_condition.right_operand

            col1_idx = columns.index(col1)

            if col2_or_value.startswith('"') and col2_or_value.endswith('"'):
                col2_or_value = col2_or_value.strip('"')
                rows = [row for row in rows if row[col1_idx] < col2_or_value]
            elif col2_or_value in columns:
                col2_idx = columns.index(col2_or_value)
                rows = [row for row in rows if row[col1_idx] < row[col2_idx]]
                
        # If GROUP BY is used, handle grouping and aggregation
        if select_command.group_by_columns:
            group_by_indices = [columns.index(col) for col in select_command.group_by_columns]
            grouped_rows = {}

            for row in rows:
                key = tuple(row[idx] for idx in group_by_indices)
                if key not in grouped_rows:
                    grouped_rows[key] = []
                grouped_rows[key].append(row)

            # Apply aggregation functions
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
            # Set columns to group by columns followed by aggregated functions
            columns = select_command.group_by_columns + [f'{func}({col})' for func, col in select_command.agg_functions]

        # Create PrettyTable object
        table = PrettyTable()
        table.field_names = columns

        for row in rows:
            table.add_row(row)

        return table.get_string()