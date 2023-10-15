use crate::lexer::Token;

#[derive(Debug)]
struct Point(i64);

#[derive(Debug)]
struct LineSegment(i64, i64);

#[derive(Debug)]
enum Command {
    Create(String),
    Insert {
        set_name: String,
        line_segment: LineSegment,
    },
    PrintTree {
        set_name: String,
    },
    Contains {
        set_name: String,
        line_segment: LineSegment,
    },
    Search {
        set_name: String,
        where_query: Option<WhereClause>,
    },
    NOP,
}

#[derive(Debug)]
enum WhereClause {
    ContainedBy(LineSegment),
    Intersects(LineSegment),
    RightOf(Point),
}

struct Parser;

#[derive(Debug, PartialEq)]
struct ParserError;

impl Parser {
    fn new() -> Self {
        Parser
    }

    fn parse_command(&mut self, tokens: Vec<Token>) -> Result<Command, ParserError> {
        let mut command: Command = Command::NOP;
        let mut current_token_index: usize = 0;

        while current_token_index < tokens.len() {
            match tokens[current_token_index] {
                Token::KeywordOrIdentifier(ref token) => {
                    current_token_index += 1;
                    let consumed_tokens;
                    let maybe_command = match token.to_lowercase().as_str() {
                        "create" => Self::parse_create(&tokens[current_token_index..]),
                        "insert" => Self::parse_insert(&tokens[current_token_index..]),
                        "print_tree" => Self::parse_printtree(&tokens[current_token_index..]),
                        "contains" => Self::parse_contains(&tokens[current_token_index..]),
                        "search" => Self::parse_search(&tokens[current_token_index..]),
                        _ => return Err(ParserError),
                    };

                    (consumed_tokens, command) = match maybe_command {
                        Ok(tuple) => tuple,
                        Err(err) => {
                            return Err(err);
                        }
                    }
                }
                Token::EndOfCommand => {
                    break;
                }
                _ => {
                    return Err(ParserError);
                }
            }
        }

        if let Command::NOP = command {
             Err(ParserError)
        } else {
            Ok(command)
        }
    }

    fn parse_create(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut consumed_tokens = tokens.len();

        todo!()
    }

    fn parse_insert(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut consumed_tokens = tokens.len();

        todo!()
    }

    fn parse_printtree(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut consumed_tokens = tokens.len();

        todo!()
    }

    fn parse_contains(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut consumed_tokens = tokens.len();

        todo!()
    }

    fn parse_search(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut consumed_tokens = tokens.len();

        todo!()
    }
}
