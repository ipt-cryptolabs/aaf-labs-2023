pub mod cli {
    use crate::lexer;
    use std::error::Error;
    use std::io;
    use std::io::BufRead;

    pub struct CLI;

    impl CLI {
        pub fn new() -> Self {
            CLI
        }

        pub fn start_repl(&self) -> Result<(), Box<dyn Error>> {
            let locked_stdin = io::stdin().lock();
            let mut lexer = lexer::Lexer::new();
            for line in locked_stdin.lines() {
                if let lexer::LexingState::End = lexer.tokenize(line?) {
                    todo!(); // send to parser, reset lexer
                } else {
                    continue;
                }
            }

            Ok(())
        }
    }
}

pub mod lexer {
    pub enum Token {
        KeywordOrIdentifier(String),
        LineSegment(i64, i64),
        Point(i64),
        EndOfCommand,
    }

    pub enum LexingState {
        Continue,
        End,
    }

    pub struct Lexer {
        state: LexingState,
        tokens: Vec<Token>,
    }

    impl Lexer {
        pub fn new() -> Self {
            Self {
                state: LexingState::End,
                tokens: Vec::new(),
            }
        }

        pub fn tokenize(&mut self, input: String) -> LexingState{
            todo!()
        }

        pub fn flush(&mut self) -> Vec<Token>{
            todo!()
        }

        fn get_koi(slice: &str) -> String{
            todo!()
        }

        fn get_linesegment(slice: &str) -> (i64, i64){
            todo!()
        }

        fn get_point(slice: &str) -> i64{
            todo!()
        }
    }

    #[cfg(test)]
    mod tests {
        #[test]
        fn lexer_manual_test() {}
    }
}

pub mod parser {
    pub enum Token {
        Command(Command),
        SetName(String),
        LineSegment(i64, i64),
        Point(i64),
        WhereClause(Option<WhereClause>),
    }

    pub enum Command {
        Create,
        Insert,
        PrintTree,
        Contains,
        Search,
    }

    pub enum WhereClause {
        ContainedBy,
        Intersects,
        RightOf,
    }
}

mod interpreter {}
