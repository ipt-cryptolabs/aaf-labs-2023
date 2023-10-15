pub enum Token {
    Command(Command),
    SetName(String),
    LineSegment(i64, i64),
    Point(i64),
    WhereClause(Option<WhereClause>),
}

pub enum Command {
    Create,
    Insert,
    PrintTree,
    Contains,
    Search,
}

pub enum WhereClause {
    ContainedBy,
    Intersects,
    RightOf,
}