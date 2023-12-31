package com.lab.db.parser;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;


public class Parser {
    class Token {
        private TokenType type;
        private String value; // value depends on token type, for example if token type is command then value can only be 'where', 'contains', etc

        public Token(TokenType type, String value) {
            this.type = type;
            this.value = value;
        }

        public String getValue() {
            return this.value;
        }

        @Override
        public String toString() {
            String s = String.format("Token: %s, %s", this.type.name(), this.value);
            return s;
        }
    }
    private String text;
    private int pos;
    private Token currentToken;
    private Character currentChar;

    private boolean checkText(String text) {
        return Pattern.matches("([a-zA-Z][a-zA-Z0-9_]* *(\\[\\s*-?\\d+\\s*,\\s*-?\\d+\\s*\\])?\\d* *)*;", text);
    }
    public Parser(String text) {
        if (checkText(text)) {
            this.text = text;
        }
        else {
            throw new SyntaxError("Syntax Error");
        }
        this.pos = 0;
        this.currentToken = null;
        this.currentChar = text.charAt(pos);
    }
    public Parser() {

    }
    public void setText(String text) {
        if (checkText(text)) {
            this.text = text;
        }
        else {
            throw new SyntaxError("Syntax Error");
        }
        this.pos = 0;
        this.currentToken = null;
        this.currentChar = text.charAt(pos);
    }
    private void advance() {
        this.pos += 1;
        if (this.pos > text.length() - 1) {
            this.currentChar = null;
        }
        else {
            this.currentChar = text.charAt(this.pos);
        }
    }

    private void skipWhitespace() {
        while (this.currentChar != null && this.currentChar.equals(' ')) {
            this.advance();
        }
    }

    private int integer() {
        String result = "";
        while (Character.isDigit(this.currentChar) || this.currentChar == '-') {
            result += this.currentChar;
            this.advance();
        }
        return Integer.parseInt(result);
    }
    private String command() {
        String result = "";
        while (this.currentChar != ';' && this.currentChar != ' ') {
            result += this.currentChar;
            this.advance();
        }
        return result;
    }
    private String identificator() {
        String result = "";
        while (this.currentChar != ';' && this.currentChar != ' ') {
            result += this.currentChar;
            this.advance();
        }
        return result;
    }
    private String lineSegment() {
        int a = 0, b = 0;
        boolean isFirstNumber = true;
        // [    23 ,   32 ]   ;
        while (this.currentChar != null) {
            if (this.currentChar == ' ') {
                skipWhitespace();
            }
            if (Character.isDigit(this.currentChar) || this.currentChar == '-') {
                if (isFirstNumber) {
                    a = integer();
                    isFirstNumber = false;
                }
                else {
                    b = integer();
                }
            }
            this.advance();
        }
        String aAndB = Integer.toString(a) + " " + Integer.toString(b);
        return aAndB;
    }
    public List<Token> tokenize() {
        List<Token> tokens = new ArrayList<>();
        if (this.currentChar == ' ') {
            this.skipWhitespace();
        }
        String command = command();
        boolean isCorrectCommand = false;
        short commandType = 1;
        for (KeyWords k : KeyWords.values()) {
            if (k.name().equalsIgnoreCase(command.toLowerCase())) {
                tokens.add(new Token(TokenType.COMMAND, command));
                if (command.equalsIgnoreCase("create") || command.equalsIgnoreCase("search") || command.equalsIgnoreCase("print_tree")) {
                    commandType = 2;
                }
                if (command.equalsIgnoreCase("search")) {
                    commandType = 3;
                }
                isCorrectCommand = true;
                break;
            }
        }
        if (!isCorrectCommand) {
            throw new SyntaxError("Not valid command");
        }
        if (this.currentChar == ' ') {
            this.skipWhitespace();
        }
        if ((this.currentChar >= 65 && this.currentChar <=90) || (this.currentChar >=97 && this.currentChar <=122)) {
            String id = identificator();
            tokens.add(new Token(TokenType.ID, id));
        }
        else {
            throw new SyntaxError("No id");
        }
        this.skipWhitespace();
        if (commandType == 1) {
            if (this.currentChar == ' ') {
                this.skipWhitespace();
            }
            if (this.currentChar != ';') {
                String lineSegment = lineSegment();
                tokens.add(new Token(TokenType.LINE_SEGMENT, lineSegment));
            }
            else {
                throw new SyntaxError("No line segment");
            }
        }
        else if(commandType == 3) {
            if (this.currentChar == ' ') {
                this.skipWhitespace();
            }
            String set_name = identificator();
            this.skipWhitespace();
            if (this.currentChar == ';') {
                tokens.add(new Token(TokenType.ID, set_name));
            }
            else {
                String _command = command();
                if (!_command.equalsIgnoreCase("left_of")) {
                    String line_segment = lineSegment();
                    tokens.add(new Token(TokenType.COMMAND, _command));
                    tokens.add(new Token(TokenType.LINE_SEGMENT, line_segment));
                }
                else {
                    this.skipWhitespace();
                    String i = "";
                    while (Character.isDigit(this.currentChar)) {
                        i += this.currentChar;
                        this.advance();
                    }
                    System.out.println(i);
                    tokens.add(new Token(TokenType.COMMAND, _command));
                    tokens.add(new Token(TokenType.INT, i));
                }

            }
//            if (this.currentChar != ';') {
//                String lineSegment = lineSegment();
//                tokens.add(new Token(TokenType.LINE_SEGMENT, lineSegment));
//            }
        }
        this.skipWhitespace();
        return tokens;
    }
}
