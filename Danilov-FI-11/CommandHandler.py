
def handle_create(parsed_command):
    print(f"Creating table {parsed_command['table_name']} with columns {parsed_command['columns']}", end='. ')
    if parsed_command['indexed_columns']:
        print(f"Indexed columns: {parsed_command['indexed_columns']}")
    else:
        print("No columns are indexed.")

def handle_insert(parsed_command):
    print(f"Inserting into table {parsed_command['table_name']} with values {parsed_command['values']}")

def handle_select(parsed_command):
    output = f"Selecting from table {parsed_command['table_name']}"
    
    if parsed_command['conditions']:
        output += f" applying WHERE conditions: {parsed_command['conditions']}"
        #...
    
    if parsed_command['group_by']:
        output += f" grouping by: {parsed_command['group_by']}"
        if parsed_command['agg_columns']:
            output += f" with aggregate functions {parsed_command['agg_columns']}"
    
    print(output)
    #...
