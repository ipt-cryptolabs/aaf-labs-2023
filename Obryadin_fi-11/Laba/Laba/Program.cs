using System;

namespace DatabaseApplication
{
    class Program
    {
        static void Main(string[] args)
        {
            Database db = new Database();
            Console.WriteLine("Enter commands, or 'exit;' to quit.");

            while (true)
            {
                Console.Write("> ");
                string fullCommand = Console.ReadLine().Trim();

                if (fullCommand.Equals("exit;", StringComparison.OrdinalIgnoreCase))
                    break;

                try
                {
                    var tokens = Parser.Tokenize(fullCommand);
                    if (tokens.Count > 0)
                    {
                        switch (tokens[0].Value.ToUpper())
                        {
                            case "CREATE":
                                var createCommand = Parser.ParseCreate(tokens);
                                var createResult = db.CreateTable(createCommand);
                                Console.WriteLine(createResult);
                                break;
                            case "INSERT":
                                var insertCommand = Parser.ParseInsert(tokens);
                                var insertResult = db.InsertIntoTable(insertCommand);
                                Console.WriteLine(insertResult);
                                break;
                            case "SELECT":
                                var selectCommand = Parser.ParseSelect(tokens);
                                var selectResult = db.SelectFromTable(selectCommand);
                                Console.WriteLine(selectResult);
                                break;
                            default:
                                Console.WriteLine("Error: Unknown or incorrect command.");
                                break;
                        }
                    }
                    else
                    {
                        Console.WriteLine("Error: No input detected.");
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }
            }
        }
    }
}