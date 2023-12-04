use std::error::Error;
use std::fmt::{Display, Formatter};
use std::num::ParseIntError;

#[derive(Debug)]
pub enum Token {
    KeywordOrIdentifier(String),
    Whitespace,
    OpenSqBracket,
    CloseSqBracket,
    Comma,
    Point(i64),
    EndOfCommand,
}

#[derive(PartialEq, PartialOrd, Eq)]
pub enum LexingState {
    Continue,
    Empty,
    End,
}

pub struct Lexer {
    tokens: Vec<Token>,
    state: LexingState,
}

#[derive(Debug, PartialEq, Eq)]
pub enum LexerError {
    UnexpectedLexeme,
    ParseIntError
}

impl Display for LexerError {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "Lexer error: ")?;
        match self{
            Self::UnexpectedLexeme => {
                write!(f, "unexpected lexeme")
            },
            Self::ParseIntError =>{
            write!(f, "integer could not be parsed")
        }
        }
    }
}

impl Error for LexerError {}

impl From<ParseIntError> for LexerError{
    fn from(value: ParseIntError) -> Self {
        LexerError::ParseIntError
    }
}

impl Lexer {
    pub fn new() -> Self {
        Self {
            tokens: Vec::new(),
            state: LexingState::End,
        }
    }

    /// tokenize input and push tokens to state. Last non-erroneous state is preserved on error.
    pub fn tokenize(&mut self, input: &str) -> Result<LexingState, LexerError> {
        if self.state == LexingState::End && input.is_empty() {
            return Ok(LexingState::Empty);
        }

        let mut str_b_index = 0;

        // If tokenization was interrupted, insert an implicit whitespace
        // This moves the hanling of lexer's state out of CLI
        if let LexingState::Continue = self.state {
            self.maintain_single_whitespace()
        }

        // the state will be Continue until we collect a complete command
        self.state = LexingState::Continue;

        while str_b_index < input.len() {
            match input[str_b_index..].chars().next() {
                Some(c) => {
                    match c {
                        // TODO all str_b... += could be refactored out
                        'a'..='z' | 'A'..='Z' => {
                            let (token_len, koi) = Self::get_koi(&input[str_b_index..]);
                            self.tokens.push(Token::KeywordOrIdentifier(koi));
                            str_b_index += token_len;
                        }
                        '0'..='9' | '-' => {
                            let (token_len, point) = Self::get_point(&input[str_b_index..])?;
                            self.tokens.push(Token::Point(point));
                            str_b_index += token_len;
                        }
                        '[' => {
                            self.tokens.push(Token::OpenSqBracket);
                            str_b_index += 1;
                        }
                        ']' => {
                            self.tokens.push(Token::CloseSqBracket);
                            str_b_index += 1;
                        }
                        ',' => {
                            self.tokens.push(Token::Comma);
                            str_b_index += 1;
                        }
                        ';' => {
                            // End of command, the rest will be ignored
                            self.tokens.push(Token::EndOfCommand);
                            self.state = LexingState::End;
                            str_b_index += 1; // just in case I'll ever want to use Lexer after the EndCommmand token
                            return Ok(LexingState::End);
                        }
                        c @ _ => {
                            // None of the above and not whitespace is an unexpected lexeme
                            if !c.is_whitespace() {
                                return Err(LexerError::UnexpectedLexeme);
                            } else {
                                str_b_index += Self::get_whitespace(&input[str_b_index..]);
                                // let's just keep one whitespace, its meaningful enough
                                self.maintain_single_whitespace();
                            }
                            // Ignore all the rest (the rest being whitespaces)
                        }
                    }
                }

                // We will just ignore empty queries and ask for more data
                None => return Ok(LexingState::Continue),
            }
        }

        // No end-of-command encountered, continue parsing
        Ok(LexingState::Continue)
    }

    fn maintain_single_whitespace(&mut self) {
        match self.tokens.last() {
            // we'll also ignore None, effectively skipping whitespace-only lines
            Some(Token::Whitespace) => {}
            _ => {
                self.tokens.push(Token::Whitespace);
            }
        }
    }

    pub fn collect(&mut self) -> Vec<Token> {
        let result = self.tokens.drain(0..).collect();

        result
    }

    fn get_koi(slice: &str) -> (usize, String) {
        let mut token_length = slice.len();
        for (pos, c) in slice.char_indices() {
            match c {
                'a'..='z' | 'A'..='Z' | '0'..='9' | '_' => {
                    //character is OK, go on
                }
                _ => {
                    token_length = pos;
                    break;
                }
            }
        }

        (token_length, String::from(&slice[0..token_length]))
    }

    fn get_point(slice: &str) -> Result<(usize, i64), ParseIntError> {
        let mut token_length = slice.len();
        let skippedminus:usize  =  if &slice[0..=0] == "-" {1} else {0};

        for (pos, c) in slice.char_indices().skip(skippedminus) {
            match c {
                '0'..='9' => {
                    //character is OK
                }
                _ => {
                    token_length = pos;
                    break;
                }
            }
        }

        let point = i64::from_str_radix(&slice[skippedminus..token_length], 10)?;

        Ok((token_length, if skippedminus == 0 {point} else {-point}))
    }

    fn get_whitespace(slice: &str) -> usize {
        let mut token_length = slice.len();
        for (pos, c) in slice.char_indices() {
            if !c.is_whitespace() {
                token_length = pos;
                break;
            }
        }

        token_length
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn lexer_manual_test() {}
}
