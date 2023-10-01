import re


def parse_create(command):
    pattern = r"^[\s\r\n\t]*CREATE[\s\r\n\t]+([a-zA-Z][a-zA-Z0-9_]*)[\s\r\n\t]*\((.+?)\)[\s\r\n\t]*;.*$"
    match = re.search(pattern, command, re.IGNORECASE | re.DOTALL)
    
    if not match:
        return {"success": False, "error": "Command not matched"}
    
    table_name = match.group(1)

    columns_str = match.group(2).strip()
    columns = [col.strip() for col in re.split(r",\s*", columns_str)]
    
    indexed_columns = []
    for i, col in enumerate(columns):
        if col.upper().endswith(" INDEXED"):
            indexed_columns.append(col.replace(" INDEXED", "").strip())
            columns[i] = col.replace(" INDEXED", "").strip()
    
    return {
        "success": True,
        "type": "CREATE",
        "table_name": table_name,
        "columns": columns,
        "indexed_columns": indexed_columns
    }

def parse_insert(command):
    pattern = r"^\s*INSERT\s+(?:INTO\s+)?([a-zA-Z][a-zA-Z0-9_]*)\s*\((.*?)\)\s*;.*$"
    match = re.search(pattern, command, re.IGNORECASE)

    if match:
        table_name = match.group(1)
        values = [value.strip().strip('\'"') for value in match.group(2).split(",")]
        return {
        "success": True,
        "type": "INSERT",
        "table_name": table_name,
        "values": values,
    }
    else:
        return {"success": False, "error": "Command not matched"}
    

def parse_select(command):
    select_pattern_with_agg = r'^\s*SELECT\s+(.*?)\s+FROM\s+([a-zA-Z][a-zA-Z0-9_]*)'
    select_pattern = r'^\s*SELECT\s+FROM\s+([a-zA-Z][a-zA-Z0-9_]*)'  
    where_pattern = r'\s+WHERE\s+(.*?)(?=\s+GROUP_BY|$)'
    groupby_pattern = r'\s+GROUP_BY\s+(.*?)(?=\s*;|$)'
    
    select_match = re.search(select_pattern_with_agg, command, re.IGNORECASE | re.DOTALL)

    if not select_match:
        select_match = re.search(select_pattern, command, re.IGNORECASE | re.DOTALL)
        agg_columns = None      
        table_name = select_match.group(1) if select_match else None
        group_by = None
    else:
        groupby_match = re.search(groupby_pattern, command, re.IGNORECASE | re.DOTALL)
        if not groupby_match:
            return {"success": False, "error": "Command not matched"}        
        agg_columns_str = select_match.group(1)
        group_by = [item.strip() for item in groupby_match.group(1).split(",")];
        table_name = select_match.group(2)
        
        agg_pattern = r'(\w+)\((.*?)\)'
        agg_matches = re.findall(agg_pattern, agg_columns_str, re.IGNORECASE)
        if agg_matches:
            agg_columns = [{"function": func, "column": col.strip()} for func, col in agg_matches]
        else:
            agg_columns = None    

    if not select_match:
        return {"success": False, "error": "Command not matched"}

    where_match = re.search(where_pattern, command, re.IGNORECASE | re.DOTALL)
   
    
    parsed_command = {
        "success": True,
        "type": "SELECT",
        "agg_columns": agg_columns,
        "table_name": table_name,
        "conditions": where_match.group(1).strip() if where_match else None,
        "group_by": group_by
    }
    
    return parsed_command

