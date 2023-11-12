use std::fmt::{Display, Formatter};
use crate::lexer::Token;

#[derive(Debug)]
pub struct Point(i64);

#[derive(Debug)]
pub struct LineSegment(pub i64, pub i64);

impl Display for LineSegment {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{}, {}]", self.0, self.1)
    }
}

#[derive(Debug)]
pub enum Command {
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
pub enum WhereClause {
    ContainedBy(LineSegment),
    Intersects(LineSegment),
    RightOf(Point),
}

pub struct Parser;

#[derive(Debug, PartialEq)]
pub struct ParserError;

impl Parser {
    pub fn new() -> Self {
        Parser
    }

    pub fn parse_command(&self, tokens: Vec<Token>) -> Result<Command, ParserError> {
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
                    };

                    current_token_index += consumed_tokens;
                }
                // skip whitespaces
                Token::Whitespace => current_token_index += 1,
                Token::EndOfCommand => {
                    current_token_index += 1; // just in case...
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

    // this and the following should DEFINITELY shoul be refactored ... - TODO

    fn parse_create(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut cti: usize = 0; // current token index

        if let Some(Token::Whitespace) = tokens.get(cti) {
            cti += 1;
            if let Some(Token::KeywordOrIdentifier(ref name)) = tokens.get(cti) {
                cti += 1;
                return Ok((cti, Command::Create(String::from(name))));
            }
        }

        Err(ParserError)
    }

    fn parse_insert(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut cti: usize = 0; // current token index

        if let Some(Token::Whitespace) = tokens.get(cti) {
            cti += 1;
            if let Some(Token::KeywordOrIdentifier(ref set_name)) = tokens.get(cti) {
                cti += 1;
                if let Some(Token::Whitespace) = tokens.get(cti) {
                    cti += 1;

                    let (parsed_len, line_segment) = Self::parse_line_segment(&tokens[cti..])?;
                    cti += parsed_len;

                    return Ok((
                        cti,
                        Command::Insert {
                            set_name: String::from(set_name),
                            line_segment: line_segment,
                        },
                    ));
                }
            }
        }

        Err(ParserError)
    }

    fn parse_printtree(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut cti: usize = 0; // current token index

        if let Some(Token::Whitespace) = tokens.get(cti) {
            cti += 1;
            if let Some(Token::KeywordOrIdentifier(ref set_name)) = tokens.get(cti) {
                cti += 1;

                return Ok((
                    cti,
                    Command::PrintTree {
                        set_name: String::from(set_name),
                    },
                ));
            }
        }

        Err(ParserError)
    }

    fn parse_contains(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut cti: usize = 0; // current token index

        if let Some(Token::Whitespace) = tokens.get(cti) {
            cti += 1;
            if let Some(Token::KeywordOrIdentifier(ref set_name)) = tokens.get(cti) {
                cti += 1;
                if let Some(Token::Whitespace) = tokens.get(cti) {
                    cti += 1;

                    let (parsed_len, line_segment) = Self::parse_line_segment(&tokens[cti..])?;
                    cti += parsed_len;

                    return Ok((
                        cti,
                        Command::Contains {
                            set_name: String::from(set_name),
                            line_segment: line_segment,
                        },
                    ));
                }
            }
        }

        Err(ParserError)
    }

    fn parse_search(tokens: &[Token]) -> Result<(usize, Command), ParserError> {
        let mut cti: usize = 0; // current token index

        if let Some(Token::Whitespace) = tokens.get(cti) {
            cti += 1;
            if let Some(Token::KeywordOrIdentifier(ref set_name)) = tokens.get(cti) {
                cti += 1;
                if let (parsed_len, Some(where_clause)) = Self::parse_where(&tokens[cti..])? {
                    cti += parsed_len;

                    return Ok((
                        cti,
                        Command::Search {
                            set_name: String::from(set_name),
                            where_query: Some(where_clause),
                        },
                    ));
                } else {
                    return Ok((
                        cti,
                        Command::Search {
                            set_name: String::from(set_name),
                            where_query: None,
                        },
                    ));
                }
            }
        }

        Err(ParserError)
    }

    fn parse_line_segment(tokens: &[Token]) -> Result<(usize, LineSegment), ParserError> {
        let mut cti: usize = 0;

        if let Some(Token::OpenSqBracket) = tokens.get(cti) {
            cti += 1;
            // Whitespace is optional
            if let Some(Token::Whitespace) = tokens.get(cti) {
                cti += 1
            }
            if let Some(Token::Point(x)) = tokens.get(cti) {
                cti += 1;
                // Whitespace is optional
                if let Some(Token::Whitespace) = tokens.get(cti) {
                    cti += 1
                }
                if let Some(Token::Comma) = tokens.get(cti) {
                    cti += 1;
                    if let Some(Token::Whitespace) = tokens.get(cti) {
                        cti += 1
                    }
                    if let Some(Token::Point(y)) = tokens.get(cti) {
                        cti += 1;
                        if let Some(Token::Whitespace) = tokens.get(cti) {
                            cti += 1
                        }
                        if let Some(Token::CloseSqBracket) = tokens.get(cti) {
                            cti += 1;
                            return Ok((cti, LineSegment(*x, *y)));
                        }
                    }
                }
            }
        }

        Err(ParserError)
    }

    fn parse_where(tokens: &[Token]) -> Result<(usize, Option<WhereClause>), ParserError> {
        let mut cti: usize = 0;

        if let Some(Token::Whitespace) = tokens.get(cti) {
            cti += 1;
            if let Some(Token::KeywordOrIdentifier(maybe_where)) = tokens.get(cti) {
                cti += 1;
                if maybe_where.to_lowercase() == "where" {
                    if let Some(Token::Whitespace) = tokens.get(cti) {
                        cti += 1;
                        if let Some(Token::KeywordOrIdentifier(ref query)) = tokens.get(cti) {
                            cti += 1;
                            match query.to_lowercase().as_str() {
                                "contained_by" => {
                                    if let Some(Token::Whitespace) = tokens.get(cti) {
                                        cti += 1;

                                        let (parsed_len, line_segment) =
                                            Self::parse_line_segment(&tokens[cti..])?;

                                        cti += parsed_len;

                                        return Ok((
                                            cti,
                                            Some(WhereClause::ContainedBy(line_segment)),
                                        ));
                                    }

                                    return Err(ParserError);
                                }
                                "intersects" => {
                                    if let Some(Token::Whitespace) = tokens.get(cti) {
                                        cti += 1;

                                        let (parsed_len, line_segment) =
                                            Self::parse_line_segment(&tokens[cti..])?;

                                        cti += parsed_len;

                                        return Ok((
                                            cti,
                                            Some(WhereClause::Intersects(line_segment)),
                                        ));
                                    }

                                    return Err(ParserError);
                                }
                                "right_of" => {
                                    if let Some(Token::Whitespace) = tokens.get(cti) {
                                        cti += 1;

                                        if let Some(Token::Point(x)) = tokens.get(cti) {
                                            cti += 1;
                                            return Ok((
                                                cti,
                                                Some(WhereClause::RightOf(Point(*x))),
                                            ));
                                        }
                                    }

                                    return Err(ParserError);
                                }
                                _ => return Err(ParserError),
                            }
                        }
                    }
                }
            }
        }

        Err(ParserError)
    }
}
