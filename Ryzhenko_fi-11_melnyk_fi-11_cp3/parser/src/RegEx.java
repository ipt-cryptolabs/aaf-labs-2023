package com.test.testdb.query.parser;

import java.util.*;
import java.util.regex.*;

public class RegEx {
    private static final Map<String, List<String>> tables = new HashMap<>();

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        StringBuilder commandBuffer = new StringBuilder();
        while (true) {
            System.out.print("> ");
            String input = scanner.nextLine();

            if (input.equalsIgnoreCase("exit")) {
                break;
            }

            commandBuffer.append(input).append(" ");

            if (input.endsWith(";")) {
                try {
                    parseCommand(commandBuffer.toString().trim().toLowerCase());
                    commandBuffer.setLength(0);
                } catch (ParseException e) {
                    System.out.println("Помилка: " + e.getMessage());
                    commandBuffer.setLength(0);
                }
            }
        }
    }

    public static void parseCommand(String input) throws ParseException {
        String createPattern = "\\s*create\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*\\(([^)]*)\\);\\s*";
        String insertPattern = "\\s*insert(\\s+into)?\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*\\(([^)]*)\\);\\s*";
        String selectPattern = "\\s*select(\\s+(count|max|avg)\\(([^)]*)\\))?\\s+from\\s+([a-zA-Z][a-zA-Z0-9_]*)"
                + "(\\s+where\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*=\\s*([a-zA-Z][a-zA-Z0-9_]*|\\d+))?\\s*"
                + "(group by\\s+([a-zA-Z][a-zA-Z0-9_]*(,\\s*[a-zA-Z][a-zA-Z0-9_]*)*)\\s*)?;\\s*";

        if (Pattern.matches(createPattern, input)) {
            Matcher matcher = Pattern.compile(createPattern).matcher(input);
            if (matcher.find()) {
                String tableName = matcher.group(1);
                String columns = matcher.group(2).trim();
                String columnsWithId = "id," + columns;
                createTable(tableName, columnsWithId);
            }
        } else if (Pattern.matches(insertPattern, input)) {
            Matcher matcher = Pattern.compile(insertPattern).matcher(input);
            if (matcher.find()) {
                String tableName = matcher.group(2);
                String values = matcher.group(3).trim();
                insertIntoTable(tableName, values);
            }
        } else if (Pattern.matches(selectPattern, input)) {
            Matcher matcher = Pattern.compile(selectPattern).matcher(input);
            if (matcher.find()) {
                String functionName = matcher.group(2);
                String columnName = matcher.group(3);
                String tableName = matcher.group(4);
                String whereColumn = matcher.group(6);
                String whereValue = matcher.group(7);
                String groupBy = matcher.group(9);

                handleSelect(functionName, columnName, tableName, whereColumn, whereValue, groupBy);
            }
        } else {
            throw new ParseException("Некоректний синтаксис команди.");
        }
    }

    public static void createTable(String tableName, String columns) {
        tables.put(tableName, new ArrayList<>());
        System.out.println("Створено таблицю " + tableName);
    }

    public static void insertIntoTable(String tableName, String values) {
        List<String> table = tables.get(tableName);
        if (table != null) {
            int id = table.size() + 1;
            String rowWithId = id + "," + values;
            table.add(rowWithId);
            System.out.println("Додано дані до таблиці " + tableName);
        } else {
            System.out.println("Таблиця " + tableName + " не існує.");
        }
    }

    public static void handleSelect(String functionName, String columnName, String tableName,
                                    String whereColumn, String whereValue, String groupBy) {
        List<String> table = tables.get(tableName);
        if (table != null) {

            if (functionName == null && columnName == null) {
                // Print the entire table
                printTable(table);
            } else {
                if ("count".equalsIgnoreCase(functionName)) {
                    int count = getCount(table, whereColumn, whereValue);
                    System.out.println("count(" + columnName + ") ");
                    System.out.println(count);
                } else if ("max".equalsIgnoreCase(functionName)) {
                    int max = getMax(table, columnName, whereColumn, whereValue);
                    System.out.println("max(" + columnName + ") ");
                    System.out.println(max);
                } else if ("avg".equalsIgnoreCase(functionName)) {
                    double avg = getAverage(table, columnName, whereColumn, whereValue);
                    System.out.println("avg(" + columnName + ") ");
                    System.out.println(avg);
                } else {
                    System.out.println("Unsupported aggregate function: " + functionName);
                }
            }
        } else {
            System.out.println("Таблиця " + tableName + " не існує.");
        }
    }

    private static void printTable(List<String> table) {
        // Print all rows of the table
        for (String row : table) {
            System.out.println(row);
        }
    }

    private static int getCount(List<String> table, String whereColumn, String whereValue) {
        int count = 0;
        int whereColumnIndex = -1;
        if (whereColumn != null) {
            whereColumnIndex = Arrays.asList(table.get(0).split(",")).indexOf(whereColumn);
        }

        for (String row : table) {
            String[] columns = row.split(",");
            String whereColumnValue = whereColumnIndex != -1 ? columns[whereColumnIndex].trim() : "";

            if (whereColumn != null && !whereColumnValue.equals(whereValue)) {
                continue;
            }

            count++;
        }
        return count;
    }

    private static int getMax(List<String> table, String columnName, String whereColumn, String whereValue) {
        int max = Integer.MIN_VALUE;

        int columnIndex = getColumnIndex(table.get(0), columnName);

        if (columnIndex != -1) {
            for (String row : table) {
                String[] values = row.split(",");
                if (values.length > columnIndex) {
                    try {
                        int currentValue = Integer.parseInt(values[columnIndex].trim());
                        if (currentValue > max) {
                            max = currentValue;
                        }
                    } catch (NumberFormatException ignored) {
                        // Ignore non-integer values
                    }
                }
            }
        }

        return max;
    }

    private static int getColumnIndex(String headerRow, String columnName) {
        String[] columns = headerRow.split(",");
        for (int i = 0; i < columns.length; i++) {
            if (columns[i].trim().equalsIgnoreCase(columnName)) {
                return i;
            }
        }
        return -1;  // Column not found
    }

    private static double getAverage(List<String> table, String columnName, String whereColumn, String whereValue) {
        int sum = 0;
        int count = 0;
        int columnIndex = getColumnIndex(table.get(0), columnName);
        int whereColumnIndex = -1;
        if (whereColumn != null) {
            whereColumnIndex = getColumnIndex(table.get(0), whereColumn);
        }

        if (columnIndex != -1) {
            for (String row : table) {
                String[] columns = row.split(",");
                String whereColumnValue = whereColumnIndex != -1 ? columns[whereColumnIndex].trim() : "";

                if (whereColumn != null && !whereColumnValue.equals(whereValue)) {
                    continue;
                }

                int value = Integer.parseInt(columns[columnIndex].trim());
                sum += value;
                count++;
            }
        }

        return count > 0 ? (double) sum / count : 0.0;
    }



    static class ParseException extends Exception {
        public ParseException(String message) {
            super(message);
        }
    }
}