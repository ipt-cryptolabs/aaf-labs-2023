class Database:
    def __init__(self):
        self.tables = {}
        
    def create_table(self, table_name, columns, indexed_columns=[]):
        if table_name in self.tables:
            return f"Error: Table '{table_name}' already exists"
        self.tables[table_name] = {"columns": columns, "data": [], "indexed_columns": indexed_columns}
    
    def insert_into_table(self, table_name, values):
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist"
        if len(values) != len(self.tables[table_name]['columns']):
            return f"Error: Number of values ({len(values)}) does not match the number of columns ({len(self.tables[table_name]['columns'])}) in table '{table_name}'"
        
        self.tables[table_name]["data"].append(values)
    
    def select(self, table_name, where=None, group_by=None, agg_funs=None):
        if table_name not in self.tables:
            return f"Error: Table '{table_name}' does not exist"
             
        return self.tables[table_name]['data']
            

    def handle_create(self, parsed_command):
        table_name = parsed_command.get('table_name')
        columns = parsed_command.get('columns')
        indexed_columns = parsed_command.get('indexed_columns', [])
        return self.create_table(table_name, columns, indexed_columns)

    def handle_insert(self, parsed_command):
        table_name = parsed_command.get('table_name')
        values = parsed_command.get('values')
        return self.insert_into_table(table_name, values)

    def handle_select(self, parsed_command):
        table_name = parsed_command.get('table_name')
        where = parsed_command.get('conditions')
        group_by = parsed_command.get('group_by')
        agg_funs = parsed_command.get('agg_columns')
        return self.select(table_name, where, group_by, agg_funs)