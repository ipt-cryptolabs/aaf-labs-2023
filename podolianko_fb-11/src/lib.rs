pub mod cli;
pub mod lexer;

pub mod parser;

pub mod interpreter;

pub mod kd_tree;
#[cfg(test)]
mod tests{
    use crate::kd_tree::LSTree;
    use crate::kd_tree::LineSegment;

    #[test]
    fn print_test(){
        let mut tree = LSTree::new();
        tree.insert(LineSegment::from((3,4)));
        tree.insert(LineSegment::from((2,7)));
        tree.insert(LineSegment::from((1,3)));
        tree.insert(LineSegment::from((5,8)));
        tree.insert(LineSegment::from((4,6)));
        tree.insert(LineSegment::from((5,10)));
        println!("{}", &tree);
    }
}