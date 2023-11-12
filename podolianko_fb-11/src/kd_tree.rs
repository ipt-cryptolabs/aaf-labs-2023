use std::collections::VecDeque;
use std::fmt::{Display, Formatter};

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub struct LineSegment {
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
        // had to put this up here and not in the else calse of the `if let` because of the borrow checker

        if self.root.is_none() {
            self.root = Some(Box::new(LSNode::new(key)));
            return None;
        }

        if let Some(root) = &mut self.root {
            let mut dim = 0; // start by subdividing the plane to L/R (x/1st coord)
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
                        }
                    }
                }
                // next node down the tree will subdivide the plane by Y/2nd coord
                dim = (dim + 1) % 2;
            }
        }
        // if we reach here, a new node has been inserted
        None
    }
    /// Returns Some(&LineSegment) is such line segment is present in the tree; None otherwise.
    pub fn get(&self, key: &LineSegment) -> Option<&LineSegment> {
        let mut current_node_ptr = self.root.as_ref();
        let mut dim = 0;
        while let Some(node) = current_node_ptr {
            if &node.key == key {
                return Some(&node.key);
            } else {
                match dim {
                    0 => {
                        if key.l <= node.key.l {
                            current_node_ptr = node.left.as_ref();
                        } else {
                            current_node_ptr = node.right.as_ref();
                        }
                    }
                    1 => {
                        if key.h <= node.key.h {
                            current_node_ptr = node.left.as_ref();
                        } else {
                            current_node_ptr = node.right.as_ref();
                        }
                    }
                    _ => { panic!("Implementation error: dim > 1") }
                };
            }
            dim = (dim + 1) % 2;
        }
        // reached here - no such line segment
        None
    }
    pub fn get_inorder(&self) -> Vec<LineSegment>{
        use std::collections::vec_deque::VecDeque;

        let mut res:Vec<LineSegment> = Vec::new();
        let mut queue: VecDeque<&Box<LSNode>> = VecDeque::new();
        if let Some(root) = &self.root{
            queue.push_back(root)
        }

        while !queue.is_empty(){
            if let Some(node) = queue.pop_front(){
                if let Some(ref lchild) = node.left{
                    queue.push_back(lchild);
                }
                res.push(node.key);
                if let Some(ref rchild) = node.right{
                    queue.push_back(rchild);
                }
            }
        }

        res
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
        if h < l {
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

// impl From<(i64, i64)> for LineSegment {
//     fn from(value: (i64, i64)) -> Self {
//         if value.0 > value.1 {
//             panic!("Line Segment lower bound should be less than or equal to the higher bound, got {} <= {}", &value.0, &value.1);
//         }
//         Self {
//             l: value.0,
//             h: value.1,
//         }
//     }
// }

// impl TryFrom<(i64, i64)> for LineSegment {
//     type Error = TryFromLineSegmentError;
//     fn try_from(value: (i64, i64)) -> Result<Self, Self::Error> {
//         if value.0 > value.1 {
//             return Err(TryFromLineSegmentError);
//         }
//         Ok(Self {
//             l: value.0,
//             h: value.1,
//         })
//     }
// }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn print_test() {
        let mut tree = LSTree::new();
        tree.insert(LineSegment::from((3, 4)));
        tree.insert(LineSegment::from((2, 7)));
        tree.insert(LineSegment::from((1, 3)));
        tree.insert(LineSegment::from((5, 8)));
        tree.insert(LineSegment::from((4, 6)));
        tree.insert(LineSegment::from((5, 10)));
        println!("{}", &tree);
    }
}
