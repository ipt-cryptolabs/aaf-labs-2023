use crate::lexer;
use crate::parser;
use crate::interpreter;
use std::error::Error;
use std::io;
use std::io::{Write, stdout, BufRead};

pub struct CLI;

const PROMPT: &str = " > ";
const PROMPT_CONT: &str = " ...\t";

impl CLI {
    pub fn new() -> Self {
        CLI
    }

    fn prompt(prompt_text: &str) -> io::Result<()> {
        print!("{}", prompt_text);
        stdout().flush()
    }

    pub fn start_repl(&self) -> Result<(), Box<dyn Error>>{
        let mut interpr = interpreter::Interpreter::new();
        loop {
            if let Err(err) = self.repl(&mut interpr) {
                eprintln!("{}", err);
                continue;
            } else {
                break;
            }
        }
        Ok(())
    }

    pub fn repl(&self, interpr: &mut interpreter::Interpreter) -> Result<(), Box<dyn Error>> {
        Self::prompt(PROMPT)?;
        let locked_stdin = io::stdin().lock();
        let mut lexer = lexer::Lexer::new();
        let parser = parser::Parser::new();
        for line in locked_stdin.lines() {
            // println!("Line: {:?}", line);
            match lexer.tokenize(&line?) {
                Ok(state) => {
                    if let lexer::LexingState::End = state {
                        let lexed_input = lexer.collect();
                        // println!("Lexer: {:?}", lexed_input);
                        let parsed_command = parser.parse_command(lexed_input)?;
                        // println!("Parser: {:?}", parsed_command);
                        match interpr.interpret_command(parsed_command) {
                            Ok(mesg) => {
                                println!("{}", mesg)
                            }
                            Err(err) => {
                                eprintln!("{}", err)
                            }
                        }


                        Self::prompt(PROMPT)?;
                    } else {
                        Self::prompt(PROMPT_CONT)?;
                        continue;
                    }
                }
                Err(err) => {
                    // TODO implement a valid convertible Error yet
                    eprintln!("Lexer errored: {:?}", err);
                }
            }
        }

        Ok(())
    }
}
