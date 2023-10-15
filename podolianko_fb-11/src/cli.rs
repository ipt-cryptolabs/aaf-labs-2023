use crate::lexer;
use std::error::Error;
use std::io;
use std::io::{BufRead, stdout};
use std::io::Write;

pub struct CLI;
const PROMPT: &str = " > ";
const PROMPT_CONT: &str = " ...\t";

impl CLI {
    pub fn new() -> Self {
        CLI
    }

    fn prompt(prompt_text: &str) -> io::Result<()>{
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
                        // todo!(); // send to parser, reset lexer
                        let lexed_input = lexer.collect();
                        println!("{:?}", lexed_input);
                        Self::prompt(PROMPT)?;
                    } else {
                        Self::prompt(PROMPT_CONT)?;
                        continue;
                    }
                }
                Err(err) => {
                    eprintln!("Lexer errored: {:?}", err);
                }
            }
        }

        Ok(())
    }
}