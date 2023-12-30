from structures import *


collections = dict()


def create(stack: list):
    if len(stack) == 0:
        raise Exception("CREATE function requires a collection name identifier")
    
    if (new_col := stack.pop(0)) in collections:
        raise Exception(f"Collection \"{new_col}\" already exists")
    
    collections.update({new_col: RDTree()})

    return f"Collection \"{new_col}\" has been created"


def insert(stack: list):
    if (col := stack.pop(0)) not in collections.keys():
        raise Exception(f"Collection \"{col}\" doesn't exists")
    
    if len(stack) == 0:
        raise Exception("INSERT requires a set as input too")
    
    to_insert = stack.pop(0)

    collections[col].insert(to_insert)

    return f"Insert \"{str(to_insert)}\" in \"{col}\""


def print_tree(stack: list):
    if len(stack) == 0:
        raise Exception(f"PRINT_TREE requires a collection name to print")

    if (col := stack.pop(0)) not in collections:
        raise Exception(f"Collection \"{col}\" doesn't exists")
    
    if collections[col].root is None:
        raise Exception(f"Collection \"{col}\" is empty")
    
    print('\n' + col)
    print_rdtree(collections[col].root)

    return f"Collection \"{col}\" has been printed"


def contains(stack: list):
    if len(stack) == 0:
        raise Exception(f"CONTAINS requires a collection name to search")
    
    if (col := stack.pop(0)) not in collections:
        raise Exception(f"Collection \"{col}\" doesn't exists")
    
    if collections[col].root is None:
        raise Exception(f"Collection \"{col}\" is empty")
    
    return str(collections[col].contains(stack.pop(0)))


def search(stack: list):
    if (col := stack.pop(0)) not in collections:
        raise Exception(f"Collection \"{col}\" doesn't exists")
    
    if collections[col].root is None:
        raise Exception(f"Collection \"{col}\" is empty")
    
    if len(stack) == 0:
        result = collections[col].search()
        return f"Search result in \"{col}\":\n{str(result)}"

    else:
        stack.pop(0)
        condition = stack.pop(0)

        condition_op = condition[0].value
        condition_set = condition[1].value

        result = collections[col].search(condition_set, condition_op)
        return f"Search result in \"{col}\" WHERE {str(condition_op)} {str(condition_set)}:{str(result)}"
