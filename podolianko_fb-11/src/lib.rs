pub mod cli {
    use crate::lexer;
    use std::error::Error;
    use std::io;
    use std::io::BufRead;

    pub struct CLI;
    const PROMPT:&str = " > ";
    const PROMPT_CONT:&str = " ...\t";

    impl CLI {
        pub fn new() -> Self {
            CLI
        }

        pub fn start_repl(&self) -> Result<(), Box<dyn Error>> {
            let locked_stdin = io::stdin().lock();
            let mut lexer = lexer::Lexer::new();

            print!("{}", PROMPT);

            for line in locked_stdin.lines() {
                match lexer.tokenize(line?) {
                    Ok(state) => {
                        if let lexer::LexingState::End = state {
                            todo!(); // send to parser, reset lexer
                            print!("{}", PROMPT);
                        } else {
                            print!("{}", PROMPT_CONT);
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

    #[derive(Debug, PartialEq)]
    struct LexingError;

    impl Lexer {
        pub fn new() -> Self {
            Self {
                state: LexingState::End,
                tokens: Vec::new(),
            }
        }

        /// tokenize input and push tokens to state. Last non-erroneous state is preserved on error.
        pub fn tokenize(&mut self, input: &str) -> Result<LexingState, LexingError> {
            let mut str_b_index = 0;
            while str_b_index < input.len(){
                match input[str_b_index..].chars().next(){
                    Some(c) => {
                        match c {
                            'a'..='z' | 'A'..='Z' => {
                                let (token_len, koi) = Self::get_koi(&input[str_b_index..])?;
                                self.tokens.push(Token::KeywordOrIdentifier(koi));
                                str_b_index += token_len;
                            },
                            '0'..='9' => {
                                let (token_len, point) = Self::get_point(&input[str_b_index..])?;
                                self.tokens.push(Token::Point(point));
                                str_b_index += token_len;
                            },
                            '[' => {
                                let (token_len, linesegment) = Self::get_linesegment(&input[str_b_index..])?;
                                self.tokens.push(Token::LineSegment(linesegment.0, linesegment.1));
                                str_b_index += token_len;
                            },
                            ';' => {
                                // End of command, the rest will be ignored
                                self.tokens.push(Token::EndOfCommand);
                                return Ok(LexingState::End);
                            }
                            c @ _ => {
                                // None of the above and not whitespace is an unexpected lexeme
                               if !c.is_whitespace(){
                                   return Err(LexingError)
                               }
                                // Ignore ll the rest (the rest being whitespaces)
                            }
                        }
                    },

                    // We will just ignore empty queries and ask for more data
                    None => {return Ok(LexingState::Continue)}
                }
            }

            // No end-of-command encountered, continue parsing
            Ok(LexingState::Continue)
        }

        pub fn collect(&mut self) -> Vec<Token> {
            todo!()
        }

        fn get_koi(slice: &str) -> Result<(usize, String), LexingError> {
            let mut token_length = slice.len();
            for (pos, c) in slice.char_indices() {
                match c {
                    'a'..='z' | 'A'..='Z' | '0'..='9' => {
                        //character is OK
                    },
                    other @ _ => {
                        if other.is_whitespace() {
                            // This is ok, end of KOI
                            // we must get the byte position of this character, it will be the token length in bytes:
                            token_length = pos;
                        } else{
                            // This is not a valid koi character!
                            return Err(LexingError);
                        }
                    }
                }
            }

            Ok((token_length, String::from(&slice[0..token_length])))
        }

        fn get_point(slice: &str) -> Result<(usize, i64), LexingError> {
            let mut token_length = slice.len();
            for (pos, c) in slice.char_indices() {
                match c {
                    '0'..='9' => {
                        //character is OK
                    },
                    other @ _ => {
                        if other.is_whitespace() {
                            // This is ok, end of Point
                            // we must get the byte position of this character, it will be the token length in bytes:
                            token_length = pos;
                        } else{
                            // This is not a valid koi character!
                            return Err(LexingError);
                        }
                    }
                }
            }

            let maybe_point = i64::from_str_radix(&slice[0..token_length], 10);
            if let Ok(point) = maybe_point{
                Ok((token_length, point))
            }
            else{
                Err(LexingError)
            }
        }

        fn get_linesegment(slice: &str) -> Result<(usize, (i64, i64)), LexingError> {
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
