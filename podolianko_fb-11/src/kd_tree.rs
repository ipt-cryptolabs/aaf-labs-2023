use std::collections::VecDeque;
use std::fmt::{Display, Formatter};
use std::ops::Add;

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

    fn set_left(&mut self, node: LSNodePointer) {
        self.left = node;
    }

    fn set_right(&mut self, node: LSNodePointer) {
        self.right = node;
    }

    fn print(&self, mut buffer: &mut String, prefix: &str, children_prefix: &str){
        // https://stackoverflow.com/questions/4965335/how-to-print-binary-tree-diagram-in-java/8948691#8948691
        buffer.push_str(prefix);
        buffer.push_str(format!("{}", &self.key).as_str());
        buffer.push('\n');
        if self.right.is_some(){
            if let Some(child) = &self.left{
                let mut p = String::from(children_prefix);
                p.push_str("├── ");
                let mut cp = String::from(children_prefix);
                cp.push_str("│   ");
                child.print(&mut buffer, &p, &cp);
            }
        } else {
            if let Some(child) = &self.left{
                let mut p = String::from(children_prefix);
                p.push_str("└── ");
                let mut cp = String::from(children_prefix);
                cp.push_str("    ");
                child.print(&mut buffer, &p, &cp);
            }
        }

        if let Some(child) = &self.right{
            let mut p = String::from(children_prefix);
            p.push_str("└── ");
            let mut cp = String::from(children_prefix);
            cp.push_str("    ");
            child.print(&mut buffer, &p, &cp);
        }
    }
}

impl Display for LSNode {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let mut buffer = String::new();
        self.print(&mut buffer, "", "");
        write!(f, "{}", buffer)
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
                                return Some(current_node);
                            }
                            current_node.set_left(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.left.as_mut().unwrap();
                        }
                    } else {
                        if current_node.right.is_none() {
                            if current_node.key == key {
                                return Some(current_node);
                            }
                            current_node.set_right(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.right.as_mut().unwrap();
                        }
                    }
                } else {
                    if key.h <= current_node.key.h {
                        if current_node.left.is_none() {
                            if current_node.key == key {
                                return Some(current_node);
                            }
                            current_node.set_left(Some(Box::new(LSNode::new(key))));
                            break;
                        } else {
                            current_node = current_node.left.as_mut().unwrap();
                        }
                    } else {
                        if current_node.right.is_none() {
                            if current_node.key == key {
                                return Some(current_node);
                            }
                            current_node.set_right(Some(Box::new(LSNode::new(key))));
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

    pub fn get_inorder(&self) -> Vec<LineSegment> {
        use std::collections::vec_deque::VecDeque;

        let mut res: Vec<LineSegment> = Vec::new();
        let mut queue: VecDeque<&Box<LSNode>> = VecDeque::new();
        if let Some(root) = &self.root {
            queue.push_back(root)
        }

        while !queue.is_empty() {
            if let Some(node) = queue.pop_front() {
                if let Some(ref lchild) = node.left {
                    queue.push_back(lchild);
                }
                res.push(node.key);
                if let Some(ref rchild) = node.right {
                    queue.push_back(rchild);
                }
            }
        }

        res
    }

    pub fn contained_by(&self, key: &LineSegment) -> Vec<&LineSegment> {
        let mut results: Vec<&LineSegment> = Vec::new();

        if let Some(root) = &self.root {
            Self::contained_by_rec(root, 0, key, &mut results);
        }

        results
    }

    fn contained_by_rec<'a>(node: &'a LSNode, dimension: i32, key: &LineSegment, results: &mut Vec<&'a LineSegment>) {
        match dimension {
            0 => {
                if node.key.l >= key.l {
                    if node.key.h <= key.h {
                        results.push(&node.key);
                    }
                    if let Some(child) = &node.left {
                        Self::contained_by_rec(child, (dimension + 1) % 2, key, results);
                    }
                }

                // we always check the right subtree because our search range extends infinitely to the right
                if let Some(child) = &node.right {
                    Self::contained_by_rec(child, (dimension + 1) % 2, key, results);
                }
            }
            1 => {
                if node.key.h <= key.h {
                    if node.key.l >= key.l {
                        results.push(&node.key);
                    }
                    if let Some(child) = &node.right {
                        Self::contained_by_rec(child, (dimension + 1) % 2, key, results);
                    }
                }

                // we always check the right subtree because our search range extends down infinitely
                if let Some(child) = &node.left {
                    Self::contained_by_rec(child, (dimension + 1) % 2, key, results);
                }
            }
            _ => panic!("unexpected dimension")
        };
    }

    pub fn right_of(&self, x: i64) -> Vec<&LineSegment> {
        let mut results: Vec<&LineSegment> = Vec::new();

        if let Some(root) = &self.root {
            Self::right_of_rec(root, 0, x, &mut results);
        }

        results
    }

    fn right_of_rec<'a>(node: &'a LSNode, dimension: i32, x: i64, results: &mut Vec<&'a LineSegment>) {
        match dimension {
            0 => {
                if node.key.l >= x {
                    // current node is to the right of x and it's left child might be
                    results.push(&node.key);
                    if let Some(child) = &node.left {
                        Self::right_of_rec(child, (dimension + 1) % 2, x, results);
                    }
                }
                // right child might be right of x for any node
                if let Some(child) = &node.right {
                    Self::right_of_rec(child, (dimension + 1) % 2, x, results);
                }
            }
            1 => {
                if node.key.l >= x {
                    results.push(&node.key);
                }
                // we can't say anything about children of odd nodes, so we'll have to check both subtrees
                if let Some(child) = &node.left {
                    Self::right_of_rec(child, (dimension + 1) % 2, x, results);
                }
                if let Some(child) = &node.right {
                    Self::right_of_rec(child, (dimension + 1) % 2, x, results);
                }
            }
            _ => panic!("unexpected dimension")
        };
    }

    pub fn intersects(&self, key: &LineSegment) -> Vec<&LineSegment> {
        let mut results: Vec<&LineSegment> = Vec::new();

        // fictive point
        let key = LineSegment { l: key.h, h: key.l };

        if let Some(root) = &self.root {
            Self::intersects_rec(root, 0, &key, &mut results);
        }

        results
    }

    fn intersects_rec<'a>(node: &'a LSNode, dimension: i32, key: &LineSegment, results: &mut Vec<&'a LineSegment>) {
        // same as contained_by, but searching for points in the top rught quadrant
        // from a fictive point [l',h'] := [h,l] where [h,l] == key
        match dimension {
            0 => {
                if node.key.l <= key.l {
                    if node.key.h >= key.h {
                        results.push(&node.key);
                    }
                    if let Some(child) = &node.right {
                        Self::intersects_rec(child, (dimension + 1) % 2, key, results);
                    }
                }

                if let Some(child) = &node.left {
                    Self::intersects_rec(child, (dimension + 1) % 2, key, results);
                }
            }
            1 => {
                if node.key.h >= key.h {
                    if node.key.l <= key.l {
                        results.push(&node.key);
                    }
                    if let Some(child) = &node.left {
                        Self::intersects_rec(child, (dimension + 1) % 2, key, results);
                    }
                }

                if let Some(child) = &node.right {
                    Self::intersects_rec(child, (dimension + 1) % 2, key, results);
                }
            }
            _ => panic!("unexpected dimension")
        };
    }
}

impl Display for LSTree {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        writeln!(f)?;
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

impl From<LSNode> for LineSegment {
    fn from(value: LSNode) -> Self {
        value.key
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn display_test() {
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
