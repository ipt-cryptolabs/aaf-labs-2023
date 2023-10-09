import re

helper = '''
Available commands:
              CREATE collection_name;
              INSERT collection_name 'document';
              PRINT_INDEX collection_name;
              SEARCH collection_name [WHERE 'query'];
              HELP;
              EXIT;
'''
while True:
    command = input("Your command: ").strip()
    if not command:
        print(helper)
    else:
        parts = command.split()

        if parts[0].lower() == "create":
            if len(parts) == 2 and re.match(r'[a-zA-Z][a-zA-Z0-9_]*;', parts[1]):
                collection_name = re.sub(";","",parts[1])
                print(f"{collection_name} created")
            elif len(parts) < 2:
                print("Format: CREATE collection_name;")
            else:
                print("Your collection name is incorrect or you missed ';' at the end")

        elif parts[0].lower() == "insert":
            if len(parts) >= 3 and parts[2][0] == "'" and  parts[-1][-1] == ";":
                collection_name = parts[1]
                document = re.sub("'",""," ".join(parts[2:])[:-1])
                print(f"'{document}' inserted in {collection_name}")
            else:
                print("Format: INSERT collection_name 'document';")

        elif parts[0].lower() == "print_index":
            if len(parts) == 2 and parts[-1][-1] == ";":
                collection_name = re.sub(";","",parts[1])
                print(f"Indices for {collection_name}")
            else:
                print("Format: PRINT_INDEX collection_name;")

        elif parts[0].lower() == "search":
            if len(parts) >= 2 and parts[-1][-1] == ";":
                if len(parts) > 2:
                    collection_name = parts[1]
                    query = re.sub("'","",parts[3][:-1])
                    if re.match(r'[a-zA-Z0-9_]+', re.sub("'","",parts[3][:-1])):
                        print(f"Found matches in {collection_name} with {query}")
                    else:
                        print("Your query is incorrect")
                else:
                    collection_name = re.sub(";","",parts[1])
                    print(f"All documents in {collection_name}")
            else:
                print("Format: SEARCH collection_name [WHERE 'query'];")
        elif re.sub(";","",parts[0].lower()) == "help":
            print(helper)
        elif re.sub(";","",parts[0].lower()) == "exit":
            break
        else:
            print(helper)
