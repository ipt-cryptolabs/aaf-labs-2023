
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

pub enum LexingState {
    Continue,
    End,
}

pub struct Lexer {
    state: LexingState,
    tokens: Vec<Token>,
}

#[derive(Debug, PartialEq)]
pub struct LexingError;

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
                        '0'..='9' => {
                            let (token_len, point) = match Self::get_point(&input[str_b_index..]) {
                                Ok(tuple) => {tuple},
                                Err(_) =>{return Err(LexingError)},
                            };
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
                            str_b_index += 1; // just in case I'll ever want to use Lexer after the EndCommmand token
                            return Ok(LexingState::End);
                        }
                        c @ _ => {
                            // None of the above and not whitespace is an unexpected lexeme
                            if !c.is_whitespace() {
                                return Err(LexingError);
                            } else{
                                str_b_index += Self::get_whitespace(&input[str_b_index..]);
                                // let's just keep one whitespace, its meaningful enough
                                match self.tokens.last(){
                                    // we'll also ignore None, effectively skipping whitespace-only lines
                                    Some(Token::Whitespace) | None  => {

                                    }
                                    _ => {self.tokens.push(Token::Whitespace);}
                                }
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

    pub fn collect(&mut self) -> Vec<Token> {
        let result = self.tokens.drain(0..).collect();

        result
    }

    fn get_koi(slice: &str) -> (usize, String) {
        let mut token_length = slice.len();
        for (pos, c) in slice.char_indices() {
            match c {
                'a'..='z' | 'A'..='Z' | '0'..='9' => {
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
        for (pos, c) in slice.char_indices() {
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

        let maybe_point = i64::from_str_radix(&slice[0..token_length], 10);

        Ok((token_length, maybe_point?))
    }

    fn get_whitespace(slice: &str) -> usize{
        let mut token_length = slice.len();
        for (pos, c) in slice.char_indices() {
            if !c.is_whitespace(){
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