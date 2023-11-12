use std::collections::HashMap;
use std::error::Error;
use std::fmt::{Display, Formatter};
use std::ops::Add;
use crate::kd_tree;
use crate::parser::{Command, WhereClause};
use crate::kd_tree::{LineSegment, LSTree};

pub struct Interpreter {
    sets: HashMap<String, LSTree>,
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
            }
            Command::Insert { set_name, line_segment } => {
                let new_ls = LineSegment::from(line_segment);
                if new_ls.l <= new_ls.h {
                    let set = self.get_mut_set(&set_name)?;
                    if let Some(_) = set.insert(new_ls) {
                        return Err(InterpreterError {
                            message: format!("Line segment {new_ls} already exists in set {set_name}")
                        });
                    } else {
                        return Ok(format!("Added {new_ls} to set {set_name}"));
                    }
                } else {
                    return Err(InterpreterError {
                        message: format!("Line segment lower bound mustn't be greater that the higher bound (l <= h, got {new_ls})")
                    });
                }
            }
            Command::PrintTree { set_name } => {
                let set = self.get_set(&set_name)?;
                return Ok(format!("{}", { set }));
            }
            Command::Contains { line_segment, set_name } => {
                let set = self.get_set(&set_name)?;
                if let Some(_) = set.get(&line_segment) {
                    return Ok(format!("TRUE"));
                } else {
                    return Ok(format!("FALSE"));
                }
            }
            Command::Search {set_name, where_query}=>{
                let set = self.get_set(&set_name)?;
                let segments:Vec<LineSegment> = set.get_inorder();
                match where_query{
                    Some(_) =>{}
                    None =>{
                        let mut dispstr = String::new();
                        for s in &segments{
                            dispstr = dispstr.add(format!("{} ", s).as_str());
                        }
                        return Ok(dispstr)
                    }
                }
            }
            _ => {}
        };

        Err(InterpreterError {
            message: format!("Command not implemented (yet)")
        })
    }

    fn get_set(&self, set_name: &str) -> Result<&LSTree, InterpreterError> {
        if let Some(set) = self.sets.get(set_name) {
            Ok(set)
        } else {
            Err(
                InterpreterError {
                    message: format!("Set {set_name} does not exist")
                }
            )
        }
    }
    fn get_mut_set(&mut self, set_name: &str) -> Result<&mut LSTree, InterpreterError> {
        if let Some(set) = self.sets.get_mut(set_name) {
            Ok(set)
        } else {
            Err(
                InterpreterError {
                    message: format!("Set {set_name} does not exist")
                }
            )
        }
    }
}