using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using static DatabaseApplication.Parser;

namespace DatabaseApplication
{
    public class Database
    {
        private Dictionary<string, Table> tables;

        public Database()
        {
            tables = new Dictionary<string, Table>();
        }

        public string CreateTable(CreateTableCommand command)
        {
            if (tables.ContainsKey(command.TableName))
                return "Error: Table already exists.";

            List<Column> columns = command.Columns.Select(c => new Column(c.ColumnName, c.ColumnType, c.IsIndexed)).ToList();
            Table newTable = new Table(command.TableName, columns);
            tables.Add(command.TableName, newTable);
            return $"Table {command.TableName} created successfully with {command.Columns.Count} columns.";
        }

        public string InsertIntoTable(InsertIntoCommand command)
        {
            if (!tables.ContainsKey(command.TableName))
                return "Error: Table does not exist.";

            Table table = tables[command.TableName];
            if (command.Values.Count != table.Columns.Count)
                return "Error: The number of values does not match the number of columns.";

            table.Rows.Add(new List<string>(command.Values));
            return "Data inserted successfully.";
        }

        private bool EvaluateCondition(string rowValue, string operatorSymbol, string conditionValue, string columnType)
        {
            if (columnType == "TEXT")
            {
                
                return operatorSymbol == "=" ? string.Equals(rowValue, conditionValue, StringComparison.OrdinalIgnoreCase) :
                       operatorSymbol == ">" ? string.Compare(rowValue, conditionValue, StringComparison.OrdinalIgnoreCase) > 0 :
                       string.Compare(rowValue, conditionValue, StringComparison.OrdinalIgnoreCase) < 0;
            }
            else if (columnType == "INT")
            {
                int rowValueInt = int.Parse(rowValue);
                int conditionValueInt = int.Parse(conditionValue);
                return operatorSymbol == ">" ? rowValueInt > conditionValueInt :
                       operatorSymbol == "<" ? rowValueInt < conditionValueInt :
                       rowValueInt == conditionValueInt;
            }
            throw new InvalidOperationException("Invalid type for comparison.");
        }

        public string SelectFromTable(Parser.SelectCommand command)
        {
            if (!tables.ContainsKey(command.TableName))
                return $"Table {command.TableName} does not exist.";

            Table table = tables[command.TableName];
            IEnumerable<List<string>> rows = table.Rows;

            // Apply WHERE 
            if (!string.IsNullOrEmpty(command.WhereCondition))
            {
                var parts = command.WhereCondition.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length == 3)
                {
                    var columnName = parts[0];
                    var operatorSymbol = parts[1];
                    var value = parts[2].Trim('\''); // Assume the condition value is properly quoted if it's a string

                    int columnIndex = table.Columns.FindIndex(col => col.Name == columnName);
                    if (columnIndex == -1)
                        return "Column not found.";

                    var columnType = table.Columns[columnIndex].Type;

                    rows = rows.Where(row =>
                    {
                        if (columnType == "INT")
                        {
                            // Handle integer comparisons
                            int rowValueInt = int.Parse(row[columnIndex]);
                            int conditionValueInt = int.Parse(value);
                            return operatorSymbol == ">" ? rowValueInt > conditionValueInt :
                                   operatorSymbol == "<" ? rowValueInt < conditionValueInt :
                                   rowValueInt == conditionValueInt;
                        }
                        else
                        {
                            // Handle string comparisons
                            return operatorSymbol == "=" ? row[columnIndex] == value :
                                   operatorSymbol == ">" ? string.Compare(row[columnIndex], value, StringComparison.Ordinal) > 0 :
                                   string.Compare(row[columnIndex], value, StringComparison.Ordinal) < 0;
                        }
                    }).ToList();
                }
            }

            // Display results
            StringBuilder result = new StringBuilder();
            foreach (var row in rows)
            {
                result.AppendLine(string.Join(", ", row));
            }

            return result.Length > 0 ? result.ToString() : "No rows found.";
        }
    }

    class Table
    {
        public string Name { get; }
        public List<Column> Columns { get; }
        public List<List<string>> Rows { get; }

        public Table(string name, List<Column> columns)
        {
            Name = name;
            Columns = columns;
            Rows = new List<List<string>>();
        }

        public string InsertRow(List<string> values)
        {
            if (values.Count != Columns.Count)
                return "Error: The number of values does not match the number of columns.";

            for (int i = 0; i < values.Count; i++)
            {
                if (!IsValidType(values[i], Columns[i].Type))
                    return $"Error: Type mismatch for column {Columns[i].Name}. Expected {Columns[i].Type}.";
            }

            Rows.Add(new List<string>(values));
            return "Data inserted successfully.";
        }

        private bool IsValidType(string value, string type)
        {
            switch (type.ToUpper())
            {
                case "INT":
                    return int.TryParse(value, out _);
                case "TEXT":
                    return true;  
                default:
                    return true;  // Default case
            }
        }

        public string SelectRows(List<string> aggFunctions, List<string> groupByColumns)
        {         
            
            var result = "Query Results:\n";
            foreach (var row in Rows)
            {
                result += string.Join(", ", row) + "\n";
            }
            return result;
        }
    }

    class Column
    {
        public string Name { get; }
        public bool IsIndexed { get; }
        public string Type { get; private set; }  // "INT", "TEXT", ...

        public Column(string name, string type, bool isIndexed)
        {
            Name = name;
            IsIndexed = isIndexed;
            Type = type;
        }
    }

    public class ColumnDefinition
    {
        public string ColumnName { get; private set; }
        public bool IsIndexed { get; private set; }
        public string ColumnType { get; private set; }

        public ColumnDefinition(string columnName, string columnType, bool isIndexed = false)
        {
            ColumnName = columnName;
            ColumnType = columnType;
            IsIndexed = isIndexed;
        }
    }

}


