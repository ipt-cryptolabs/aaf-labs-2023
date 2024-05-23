using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using static DatabaseApplication.Parser;

namespace DatabaseApplication
{
    public static class Parser
    {
        public enum TokenType
        {
            Keyword,
            Identifier,
            String,
            Symbol,
            ComparisonOperator,
            Whitespace,
            Number,
            Unknown
        }

        private static Dictionary<TokenType, string> tokenPatterns = new Dictionary<TokenType, string>
{
    { TokenType.Keyword, @"\b(CREATE|INSERT|INTO|SELECT|FROM|WHERE|ORDER BY)\b" },
    { TokenType.Identifier, @"[a-zA-Z_][a-zA-Z0-9_]*" },
    { TokenType.ComparisonOperator, @"[=><]" },  
    { TokenType.String, @"'[^']*'|""[^""]*""" },  
    { TokenType.Number, @"\b\d+\b" },  //capture numbers
    { TokenType.Symbol, @"[(),;]" },
    { TokenType.Whitespace, @"\s+" }
};

        private static string combinedPattern = String.Join("|", Array.ConvertAll(tokenPatterns.ToArray(), pair =>
            $"(?<{pair.Key}>{pair.Value})"));

        private static Regex tokenRegex = new Regex(combinedPattern, RegexOptions.IgnoreCase);

        public static List<Token> Tokenize(string text)
        {
            List<Token> tokens = new List<Token>();
            foreach (Match match in tokenRegex.Matches(text))
            {
                TokenType firstMatchType = TokenType.Unknown;
                string firstMatchValue = "";
                foreach (Group group in match.Groups)
                {
                    if (group.Success && group.Name != "0" && group.Name != "Whitespace") 
                    {
                        TokenType currentType = (TokenType)Enum.Parse(typeof(TokenType), group.Name, true);
                        if (firstMatchType == TokenType.Unknown || currentType == TokenType.Keyword)
                        {
                            firstMatchType = currentType;
                            firstMatchValue = group.Value;
                        }
                    }
                }
                
                if (firstMatchType != TokenType.Unknown)
                {
                    tokens.Add(new Token(firstMatchType, firstMatchValue));
                    // debug tokens
                    //Console.WriteLine($"Tokenized: {firstMatchType} - '{firstMatchValue}'"); 
                }
            }
            return tokens;
        }

        public class Token
        {

            public TokenType Type { get; private set; }
            public string Value { get; private set; }

            public Token(TokenType type, string value)
            {
                Type = type;
                Value = value;
            }
        }

        //Comands

        public class CreateTableCommand
        {
            public string TableName { get; }
            public List<ColumnDefinition> Columns { get; }

            public CreateTableCommand(string tableName, List<ColumnDefinition> columns)
            {
                TableName = tableName;
                Columns = columns;
            }
        }

        public class InsertIntoCommand
        {
            public string TableName { get; }
            public List<string> Values { get; }

            public InsertIntoCommand(string tableName, List<string> values)
            {
                TableName = tableName;
                Values = values;
            }
        }

        public class SelectCommand
        {
            public string TableName { get; }
            public List<string> SelectedColumns { get; }
            public string WhereCondition { get; }
            public List<(string ColumnName, string SortDirection)> OrderByClauses { get; }

            public SelectCommand(string tableName, List<string> selectedColumns, string whereCondition, List<(string ColumnName, string SortDirection)> orderByClauses)
            {
                TableName = tableName;
                SelectedColumns = selectedColumns;
                WhereCondition = whereCondition;
                OrderByClauses = orderByClauses;
            }
        }


      //

        public static CreateTableCommand ParseCreate(List<Token> tokens)
        {
            if (tokens[0].Type != TokenType.Keyword || tokens[0].Value.ToUpper() != "CREATE")
                throw new ArgumentException("Invalid command. Expected 'CREATE'.");

            int i = 1; 
            if (tokens[i].Type != TokenType.Identifier)
                throw new ArgumentException("Invalid syntax. Expected table name after 'CREATE'.");

            string tableName = tokens[i].Value;
            i++; 

            if (tokens[i].Type != TokenType.Symbol || tokens[i].Value != "(")
                throw new ArgumentException("Invalid syntax. Expected '(' after table name.");
            i++;

            List<ColumnDefinition> columns = new List<ColumnDefinition>();
            while (i < tokens.Count && (tokens[i].Type != TokenType.Symbol || tokens[i].Value != ")"))
            {
                if (tokens[i].Type != TokenType.Identifier)
                    throw new ArgumentException("Invalid syntax. Expected column name.");

                string columnName = tokens[i].Value;
                i++;

                if (tokens[i].Type != TokenType.Identifier)
                    throw new ArgumentException("Invalid syntax. Expected column type after column name.");

                string columnType = tokens[i].Value;
                i++;

                bool isIndexed = false;
                
                if (i < tokens.Count && tokens[i].Type == TokenType.Keyword && tokens[i].Value.ToUpper() == "INDEXED")
                {
                    isIndexed = true;
                    i++; 
                }

                columns.Add(new ColumnDefinition(columnName, columnType, isIndexed));

                
                if (i < tokens.Count && tokens[i].Type == TokenType.Symbol && tokens[i].Value == ",")
                    i++;
            }

            if (i >= tokens.Count || tokens[i].Type != TokenType.Symbol || tokens[i].Value != ")")
                throw new ArgumentException("Invalid syntax. Expected ')' to close table definition.");
            i++; 

            if (i < tokens.Count && (tokens[i].Type != TokenType.Symbol || tokens[i].Value != ";"))
                throw new ArgumentException("Invalid syntax. Expected ';' at the end of the command.");

            return new CreateTableCommand(tableName, columns);
        }

        public static InsertIntoCommand ParseInsert(List<Token> tokens)
        {
            int i = 0;
            if (tokens[i++].Value.ToUpper() != "INSERT" || tokens[i++].Value.ToUpper() != "INTO")
                throw new ArgumentException("Syntax error in INSERT INTO statement.");

            string tableName = tokens[i++].Value;  
            if (tokens[i++].Value != "(")
                throw new ArgumentException("Expected '(' after table name.");

            List<string> values = new List<string>();
            while (tokens[i].Value != ")")
            {
                if (tokens[i].Type == TokenType.String || tokens[i].Type == TokenType.Number)
                {
                    values.Add(tokens[i].Value.Trim('"')); 
                }
                i++;
                if (tokens[i].Value == ",") i++; 
            }

            return new InsertIntoCommand(tableName, values);
        }

        public static SelectCommand ParseSelect(List<Token> tokens)
        {
            if (tokens[0].Value.ToUpper() != "SELECT")
                throw new ArgumentException("Invalid command. Expected 'SELECT'.");

            int i = 1; 
            List<string> selectedColumns = new List<string>();
            string whereCondition = ""; 
            List<(string ColumnName, string SortDirection)> orderByClauses = new List<(string, string)>();

            while (i < tokens.Count && tokens[i].Value.ToUpper() != "FROM")
            {
                selectedColumns.Add(tokens[i].Value);
                i++;
                if (i < tokens.Count && tokens[i].Value == ",") i++;
            }

            i++; 
            if (i >= tokens.Count || tokens[i].Type != TokenType.Identifier)
                throw new ArgumentException("Invalid syntax. Expected table name.");

            string tableName = tokens[i].Value;
            i++;
          

            if (i < tokens.Count && tokens[i].Value.ToUpper() == "WHERE")
            {
                i++; 
                while (i < tokens.Count && tokens[i].Value.ToUpper() != "ORDER_BY" && tokens[i].Value != ";")
                {
                    whereCondition += tokens[i].Value + " ";
                    i++;
                }
                whereCondition = whereCondition.Trim(); 
            }

           
            if (i < tokens.Count && tokens[i].Value.ToUpper() == "ORDER_BY")
            {
                i++; 
                while (i < tokens.Count && tokens[i].Value != ";")
                {
                    string columnName = tokens[i].Value;
                    i++;
                    string sortDirection = "ASC"; 
                    if (i < tokens.Count && (tokens[i].Value.ToUpper() == "ASC" || tokens[i].Value.ToUpper() == "DESC"))
                    {
                        sortDirection = tokens[i].Value.ToUpper();
                        i++;
                    }
                    orderByClauses.Add((columnName, sortDirection));
                    if (i < tokens.Count && tokens[i].Value == ",") i++;
                }
            }

            return new SelectCommand(tableName, selectedColumns, whereCondition, orderByClauses);
        }
    }
}


