use std::collections::HashMap;
use std::error::Error;
use std::fmt::{Display, Formatter};
use crate::parser::{Command, WhereClause};
use crate::kd_tree;

pub struct Interpreter {
    sets: HashMap<String, kd_tree::LSTree>,
}

#[derive(PartialOrd, PartialEq, Debug)]
pub struct InterpreterError {
    message: String,
}

impl Display for InterpreterError {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "Interpreter error: {}", self.message)
    }
}

impl Error for InterpreterError {}

impl Interpreter {
    pub fn new() -> Self {
        Self {
            sets: HashMap::new()
        }
    }
    pub fn interpret_command(&mut self, command: Command) -> Result<String, InterpreterError> {
        match command {
            Command::Create(set_name) => {
                if self.sets.contains_key(&set_name) {
                    return Err(InterpreterError {
                        message: format!("Set with name {set_name} already exists")
                    });
                } else {
                    self.sets.insert(set_name.clone(), kd_tree::LSTree::new());
                    return Ok(format!("Set {set_name} has been created"));
                }
            },
            Command::Insert { set_name, line_segment } => {
                let new_ls = kd_tree::LineSegment::from(line_segment);
                if new_ls.l <= new_ls.h{
                    if let Some(set) = self.sets.get_mut(&set_name) {
                        if let Some(_) = set.insert(new_ls) {
                            return Err(InterpreterError {
                                message: format!("Line segment {new_ls} already exists in set {set_name}")
                            });
                        } else {
                            return Ok(format!("Added {new_ls} to set {set_name}"));
                        }
                    } else {
                        return Err(InterpreterError {
                            message: format!("Set {set_name} does not exist")
                        });
                    }
                }else{
                    return Err(InterpreterError{
                        message: format!("Line segment lower bound mustn't be greater that the higher bound (l <= h, got {new_ls})")
                    });
                }
            },
            Command::PrintTree {set_name} =>{
                if let Some(set) = self.sets.get(&set_name){
                    return Ok(format!("{}", {set}))
                }else{
                    return Err(InterpreterError{
                        message: format!("Set {set_name} does not exist")
                    });
                }
            },
            _ => {}
        };

        Err(InterpreterError {
            message: format!("Command not implemented (yet)")
        })
    }
}