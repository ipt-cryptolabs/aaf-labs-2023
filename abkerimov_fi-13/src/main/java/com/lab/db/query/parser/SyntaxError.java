package com.lab.db.query.parser;

class SyntaxError extends NoSuchMethodError {
    public SyntaxError(String message) {
        super(message);
        this.getMessage();
    }
}