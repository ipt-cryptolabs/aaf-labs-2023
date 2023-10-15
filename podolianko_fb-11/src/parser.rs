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
        set_name: String
    },
    Contains{
        set_name: String,
        line_segment: LineSegment,
    },
    Search{
        set_name: String,
        where_query: Option<WhereClause>
    }
}

#[derive(Debug)]
enum WhereClause{
    ContainedBy(LineSegment),
    Intersects(LineSegment),
    RightOf(Point)
}

