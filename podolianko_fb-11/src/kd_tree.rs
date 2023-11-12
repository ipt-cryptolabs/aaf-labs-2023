use crate::parser;
use std::fmt::{Display, Formatter};

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub struct LineSegment {
    // have to make fields public to allow bounds checking in the interpreter module;
    // tried impl TryFrom with checks, got conflict with blanket implementation
    pub l: i64,
    pub h: i64,
}

type LSNodePointer = Option<Box<LSNode>>;

pub struct LSNode {
    key: LineSegment,
    left: LSNodePointer,
    right: LSNodePointer,
}

impl LSNode {
    fn new(key: LineSegment) -> Self {
        Self {
            key,
            left: None,
            right: None,
        }
    }

    fn add_left(&mut self, node: LSNodePointer) {
        self.left = node;
    }

    fn add_right(&mut self, node: LSNodePointer) {
        self.right = node;
    }
}

impl Display for LSNode {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        // use sign flag to determine if self was left or right
        let self_right = f.sign_plus();
        let pad = f.width().unwrap_or(0);

        if pad == 0 {
            write!(f, "{}\n", self.key)?;
        } else {
            if !self_right {
                write!(f, "{:>pad$}{}{}\n", "", "├", self.key, pad = pad)?;
            } else {
                write!(f, "{:>pad$}{}{}\n", "", "└", self.key, pad = pad)?;
            }
        }

        let pad_increase = 2;
        if let Some(ref node) = self.left {
            // println!("Will pad: {}", pad);
            write!(f, "{:pad$}", node.as_ref(), pad = pad + pad_increase)?;
        } else {
            // write!(f, "{:pad$}├\n", "", pad = pad + pad_increase)?;
        }

        if let Some(ref node) = self.right {
            // println!("Will pad: {}", pad);
            write!(f, "{:+pad$}", node.as_ref(), pad = pad + pad_increase)?;
        } else {
            // write!(f, "{:+pad$}└\n", "", pad = pad + pad_increase)?;
        }

        // preint the key of current node;
        Ok(())
    }
}

pub struct LSTree {
    root: LSNodePointer,
}

impl LSTree {
    pub fn new() -> Self {
        Self { root: None }
    }

    /// returns None if inserted successfully, Some(&Node) if node with such key is already present
    pub fn insert(&mut self, key: LineSegment) -> Option<&LSNode> {
        if self.root.is_none() {
            self.root = Some(Box::new(LSNode::new(key)));
            return None;
        }

        if let Some(root) = &mut self.root {
            let mut dim = 0;
            let mut current_node = root;
            loop {
                if dim == 0 {
                    if key.l <= current_node.key.l {
                        if current_node.left.is_none() {
                            if current_node.key == key {
                                return Some(&*current_node);
                            }

                            current_node.add_left(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.left.as_mut().unwrap();
                            continue;
                        }
                    } else {
                        if current_node.right.is_none() {
                            if current_node.key == key {
                                return Some(&*current_node);
                            }
                            current_node.add_right(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.right.as_mut().unwrap();
                            continue;
                        }
                    }
                } else {
                    if key.h <= current_node.key.h {
                        if current_node.left.is_none() {
                            if current_node.key == key {
                                return Some(&*current_node);
                            }
                            current_node.add_left(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.left.as_mut().unwrap();
                            continue;
                        }
                    } else {
                        if current_node.right.is_none() {
                            if current_node.key == key {
                                return Some(&*current_node);
                            }
                            current_node.add_right(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.right.as_mut().unwrap();
                            continue;
                        }
                    }
                }
            }
        }
        None
    }
}

impl Display for LSTree {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "\n")?;
        if let Some(node) = &self.root {
            write!(f, "{}", node)?;
        }
        write!(f, "")
    }
}

impl LineSegment {
    fn new(l: i64, h: i64) -> Self {
        if h > l {
            panic!("Line Segment lower bound should be less than or equal to the higher bound, got {} <= {}", l, h);
        }
        Self { l, h }
    }
}

impl Display for LineSegment {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{}, {}]", self.l, self.h)
    }
}

impl From<parser::LineSegment> for LineSegment {
    fn from(value: parser::LineSegment) -> Self {
        Self {
            l: value.0,
            h: value.1,
        }
    }
}

impl From<(i64, i64)> for LineSegment {
    fn from(value: (i64, i64)) -> Self {
        if value.0 > value.1 {
            panic!("Line Segment lower bound should be less than or equal to the higher bound, got {} <= {}", &value.0, &value.1);
        }
        Self {
            l: value.0,
            h: value.1,
        }
    }
}

