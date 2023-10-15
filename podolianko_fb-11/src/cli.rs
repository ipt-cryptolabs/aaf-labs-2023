use crate::lexer;
use crate::lexer::{Lexer, LexingError, LexingState};
use std::error::Error;
use std::io;
use std::io::Write;
use std::io::{stdout, BufRead};

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

    pub fn start_repl(&self) -> Result<(), Box<dyn Error>> {
        Self::prompt(PROMPT)?;
        let locked_stdin = io::stdin().lock();
        let mut lexer = lexer::Lexer::new();

        for line in locked_stdin.lines() {
            println!("Line: {:?}", line);
            match lexer.tokenize(&line?) {
                Ok(state) => {
                    if let lexer::LexingState::End = state {
                        // todo!(); // send to parser
                        let lexed_input = lexer.collect();
                        println!("{:?}", lexed_input);
                        Self::prompt(PROMPT)?;
                    } else {
                        // This marks an explicit whitespace later used by the parser.
                        // Would not need it if Lines preserved '\n'.
                        match lexer.tokenize("\n") {
                            Ok(LexingState::Continue) => {
                                // expected
                            }
                            Ok(LexingState::End) => {
                                // lexer is broken?
                                eprintln!("Internal Lexer error");
                                return Ok(()); // TODO implement a valid convertible Error
                            }
                            Err(err) => {
                                eprintln!("Lexer errored: {:?}", err);
                            }
                        }
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
