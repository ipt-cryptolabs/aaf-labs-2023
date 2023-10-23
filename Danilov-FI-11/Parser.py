import re


def parse_create(command):
    # Regular expression pattern to match the CREATE command
    pattern = r"^\s*CREATE\s+([a-zA-Z][a-zA-Z0-9_]*)\s*\((.+?)\)\s*;.*$"
    match = re.search(pattern, command, re.IGNORECASE | re.DOTALL)
    
    # If no match, return an error message
    if not match:
        return {"success": False, "error": "Command not matched"}
    
    # Extract table name
    table_name = match.group(1)

    # Extract column information
    columns_str = match.group(2).strip()
    columns = [col.strip() for col in re.split(r",\s*", columns_str)]
    
    # Check for indexed columns and separate them
    indexed_columns = []
    for i, col in enumerate(columns):
        if col.upper().endswith(" INDEXED"):
            indexed_columns.append(col.upper().replace(" INDEXED", "").strip())
            columns[i] = col.upper().replace(" INDEXED", "").strip()
    
    # Return the parsed information
    return {
        "success": True,
        "table_name": table_name,
        "columns": columns,
        "indexed_columns": indexed_columns
    }

def parse_insert(command):
    # Regular expression pattern to match the INSERT command
    pattern = r"^\s*INSERT\s+(?:INTO\s+)?([a-zA-Z][a-zA-Z0-9_]*)\s*\((.*?)\)\s*;.*$"
    match = re.search(pattern, command, re.IGNORECASE)

    # If no match, return an error message
    if not match:
        return {"success": False, "error": "Command not matched"}
    
    # If match is found, extract the table name and values
    table_name = match.group(1)
    values = [value.strip().strip('"') for value in match.group(2).split(",")]
    return {
        "success": True,
        "table_name": table_name,
        "values": values,
    }
    

def parse_select(command):
    select_pattern_with_agg = r'^\s*SELECT\s+(.*?)\s+FROM\s+([a-zA-Z][a-zA-Z0-9_]*)'
    select_pattern = r'^\s*SELECT\s+FROM\s+([a-zA-Z][a-zA-Z0-9_]*)'  
    where_pattern = r'\s+WHERE\s+(.*?)(?=\s+GROUP_BY|$)'
    groupby_pattern = r'\s+GROUP_BY\s+(.*?)(?=\s*;|$)'
    
    # Try to match with aggregate functions first
    select_match = re.search(select_pattern_with_agg, command, re.IGNORECASE | re.DOTALL)

    # If not found, try to match the simpler pattern
    if not select_match:
        select_match = re.search(select_pattern, command, re.IGNORECASE | re.DOTALL)
        agg_columns = None      
        table_name = select_match.group(1) if select_match else None
        group_by = None
    else:
        # If aggregate functions are found, also look for a GROUP BY clause
        groupby_match = re.search(groupby_pattern, command, re.IGNORECASE | re.DOTALL)
        if not groupby_match:
            return {"success": False, "error": "Command not matched"}
                
        agg_columns_str = select_match.group(1)
        group_by = [item.strip() for item in groupby_match.group(1).split(",")];
        table_name = select_match.group(2)
        
        # Parse the aggregate functions
        agg_pattern = r'(\w+)\((.*?)\)'
        agg_matches = re.findall(agg_pattern, agg_columns_str, re.IGNORECASE)
        if agg_matches:
            agg_columns = [{"function": func, "column": col.strip()} for func, col in agg_matches]
        else:
            agg_columns = None    

    # If still not matched, return an error message
    if not select_match:
        return {"success": False, "error": "Command not matched"}

    # Check for a WHERE clause
    where_match = re.search(where_pattern, command, re.IGNORECASE | re.DOTALL)
   
    # Return the parsed command
    parsed_command = {
        "success": True,
        "agg_columns": agg_columns,
        "table_name": table_name,
        "conditions": where_match.group(1).strip() if where_match else None,
        "group_by": group_by
    }
    
    return parsed_command

