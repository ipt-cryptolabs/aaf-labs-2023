package com.lab.db.parser;
import java.util.List;
import java.util.Scanner;

public class Interface {
    private final String instruction = "Commands:\n" +
            "CREATE set_name;\n" +
            "INSERT set_name [l, h];\n" +
            "PRINT_TREE set_name;\n" +
            "CONTAINS set_name [l, h];\n\n" +
            "enter EXIT to stop the program.\n";
    private final Scanner scanner = new Scanner(System.in);

    public Interface() {
        System.out.println("The database stores line segments using R-trees ");
        System.out.println(instruction);
        System.out.println("Enter your commands: ");
        String line = scanner.nextLine();
        Parser parser = new Parser();
        while (!line.equalsIgnoreCase("EXIT")) {
            parser.setText(line);
            List<Parser.Token> tokens = parser.tokenize();
            System.out.println(tokens);
            handler(tokens);
            line = scanner.nextLine();
        }
    }

    private void handler(List<Parser.Token> tokens) {

    }

    //I will add functions that will work with database
    private void Create(String setName) {
        String output;
        output = "Set " + setName + " has been created";
        System.out.println(output);
    }

    private void Insert(String setName, String lineSegment) {
        String output;
        output = "Range " + lineSegment + " has been added to " + setName;
        System.out.println(output);
    }

    private void Print(String setName) {

    }
    private void Contains(String setName, String lineSegment) {
        boolean output = true;
        System.out.println(output);
    }
    private void Search(String setName) {

    }
}
