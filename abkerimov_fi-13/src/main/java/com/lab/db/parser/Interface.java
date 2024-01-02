package com.lab.db.parser;
import com.lab.db.r_tree.RTree;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

public class Interface {
    private final String instruction = "Commands:\n" +
            "CREATE set_name;\n" +
            "INSERT set_name [l, h];\n" +
            "PRINT_TREE set_name;\n" +
            "CONTAINS set_name [l, h];\n\n" +
            "SEARCH set_name *[WHERE query]" +
            "query := CONTAINS [L, H]\n" +
            " \t\t | INTERSECTS [L, H]\n" +
            " \t\t | LEFT_OF x" +
            "enter EXIT to stop the program.\n";
    private final Scanner scanner = new Scanner(System.in);
    List<HashMap<String, RTree>> rTrees = new ArrayList<>();
    List<String> rTreesNames = new ArrayList<>();

    public Interface() {
        System.out.println("The database stores line segments using R-trees ");
        System.out.println(instruction);
        System.out.println("Enter your commands: ");
        String line = scanner.nextLine();
        Parser parser = new Parser();
        while (!line.equalsIgnoreCase("EXIT")) {
            try {
                parser.setText(line);
                List<Parser.Token> tokens = parser.tokenize();
                handler(tokens);
                line = scanner.nextLine();
            }
            catch (SyntaxError e) {
                System.out.println(e.toString());
                line = scanner.nextLine();
            }
        }
    }

    private void handler(List<Parser.Token> tokens) {
        if (tokens.get(0).getValue().equalsIgnoreCase("create")) {
            Create(tokens.get(1).getValue());
        }
        if (tokens.get(0).getValue().equalsIgnoreCase("insert")) {
            Insert(tokens.get(1).getValue(), tokens.get(2).getValue());
        }
        if (tokens.get(0).getValue().equalsIgnoreCase("print_tree")) {
            Print(tokens.get(1).getValue());
        }
        if (tokens.get(0).getValue().equalsIgnoreCase("contains")) {
            Contains(tokens.get(1).getValue(), tokens.get(2).getValue());
        }
        if (tokens.get(0).getValue().equalsIgnoreCase("search")) {
            if (tokens.get(2).getValue().equals("")) {
                Search(tokens.get(1).getValue());
            }
            else {
                Search(tokens.get(1).getValue(), tokens.get(2).getValue(), tokens.get(3).getValue());
            }
        }
    }

    private void Create(String setName) {
        if (rTrees.contains(setName)) {
            System.out.println("This set already exists, choose another name");
        }
        else {
            String output;
            output = "Set " + setName + " has been created";
            HashMap<String, RTree> hm = new HashMap<>();
            hm.put(setName, new RTree());
            rTrees.add(hm);
            rTreesNames.add(setName);
            System.out.println(output);
        }
    }

    private void Insert(String setName, String lineSegment) {
        String output;
        output = "Range " + lineSegment + " has been added to " + setName;
        if (rTreesNames.contains(setName)) {
            for (HashMap hp : rTrees) {
                if (hp.containsKey(setName)) {
                    RTree rt = (RTree)hp.get(setName);
                    int[] ls = new int[2];
                    String[] segment = lineSegment.split(" ");
                    ls[0] = Integer.parseInt(segment[0]);
                    ls[1] = Integer.parseInt(segment[1]);
                    rt.insert(ls);
                    System.out.println(output);
                    break;
                }
            }
        }
        else {
            System.out.println("Set was not found");
        }
    }

    private void Print(String setName) {
        if (rTreesNames.contains(setName)) {
            for (HashMap hp : rTrees) {
                if (hp.containsKey(setName)) {
                    RTree rt = (RTree)hp.get(setName);
                    rt.print();
                }
            }
        }
        else {
            System.out.println("Set was not found");
        }
    }
    private void Contains(String setName, String lineSegment) {
        if (rTreesNames.contains(setName)) {
            for (HashMap hp : rTrees) {
                if (hp.containsKey(setName)) {
                    RTree rt = (RTree)hp.get(setName);
                    int[] ls = new int[2];
                    String[] segment = lineSegment.split(" ");
                    ls[0] = Integer.parseInt(segment[0]);
                    ls[1] = Integer.parseInt(segment[1]);
                    System.out.println(rt.search(ls));
                }
            }
        }
    }
    private void Search(String setName) {
        if (rTreesNames.contains(setName)) {
            for (HashMap hp : rTrees) {
                if (hp.containsKey(setName)) {
                    RTree rt = (RTree)hp.get(setName);
                    rt._print();
                }
            }
        }
        else {
            System.out.println("Set was not found");
        }
    }
    private void Search(String setName, String additional_command, String integer) {
        if (additional_command.equalsIgnoreCase("left_of")) {
            if (rTreesNames.contains(setName)) {
                for (HashMap hp : rTrees) {
                    if (hp.containsKey(setName)) {
                        RTree rt = (RTree)hp.get(setName);
                        rt.left_of(Integer.parseInt(integer));
                    }
                }
            }
        }
        if (additional_command.equalsIgnoreCase("contains")) {
            if (rTreesNames.contains(setName)) {
                for (HashMap hp : rTrees) {
                    if (hp.containsKey(setName)) {
                        RTree rt = (RTree)hp.get(setName);
                        int[] ls = new int[2];
                        String[] segment = integer.split(" ");
                        ls[0] = Integer.parseInt(segment[0]);
                        ls[1] = Integer.parseInt(segment[1]);
                        rt.contains(ls);
                    }
                }
            }
        }
        if (additional_command.equalsIgnoreCase("intersects")) {
            if (rTreesNames.contains(setName)) {
                for (HashMap hp : rTrees) {
                    if (hp.containsKey(setName)) {
                        RTree rt = (RTree)hp.get(setName);
                        int[] ls = new int[2];
                        String[] segment = integer.split(" ");
                        ls[0] = Integer.parseInt(segment[0]);
                        ls[1] = Integer.parseInt(segment[1]);
                        rt.intersects(ls);
                    }
                }
            }
        }
    }
}
