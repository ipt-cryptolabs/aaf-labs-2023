package com.lab.db.parser;

class SyntaxError extends NoSuchMethodError {
    public SyntaxError(String message) {
        super(message);
        this.getMessage();
    }
}