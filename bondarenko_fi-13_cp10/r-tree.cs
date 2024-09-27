using System;
using System.Collections.Generic;

public class Point
{
    public int X { get; set; }
    public int Y { get; set; }

    public Point(int x, int y)
    {
        X = x;
        Y = y;
    }
}

internal class RTree
{
    internal class Node
    {
        public List<Point> Points { get; set; }
        public List<Node> Children { get; set; }
        public (Point, Point) Rectangle { get; set; }

        public Node()
        {
            Points = new List<Point>();
            Children = new List<Node>();
        }
    }
    internal Node _root;
        
    internal void Insert(int x, int y)
    {
        if (_root == null)
        {
            _root = new Node();
            _root.Rectangle = (new Point(x, y), new Point(x, y));
        }
        else
        {
            if (x >= _root.Rectangle.Item1.X && y >= _root.Rectangle.Item1.Y &&
                x <= _root.Rectangle.Item2.X && y <= _root.Rectangle.Item2.Y)
            {
                _root.Points.Add(new Point(x, y));
            }
            else
            {
                Node newRoot = new Node();
                _root.Rectangle = (new Point(Math.Min(_root.Rectangle.Item1.X, x), Math.Min(_root.Rectangle.Item1.Y, y)),
                    new Point(Math.Max(_root.Rectangle.Item2.X, x), Math.Max(_root.Rectangle.Item2.Y, y)));
                newRoot.Children.Add(_root);
                Node newNode = new Node { Points = { new Point(x, y) } };
                newNode.Rectangle = (new Point(x, y), new Point(x, y));
                newRoot.Children.Add(newNode);
                newRoot.Rectangle = (new Point(Math.Min(_root.Rectangle.Item1.X, x), Math.Min(_root.Rectangle.Item1.Y, y)),
                    new Point(Math.Max(_root.Rectangle.Item2.X, x), Math.Max(_root.Rectangle.Item2.Y, y)));
                _root = newRoot;
            }
        }
    }

    
    internal void Print(Node node, string indent = "")
    {
        if (node == null)
        {
            return;
        }

        Console.WriteLine($"{indent}[(x_left, y_bottom), (x_right, y_top)]");
        foreach (var child in node.Children)
        {
            Print(child, indent + "  ");
        }
    }
    internal static Dictionary<string, RTree> _sets = new Dictionary<string, RTree>();

    internal static void CreateSet(string setName)
    {
        _sets[setName] = new RTree();
        Console.WriteLine($"Set {setName} has been created");
    }
    internal static void InsertPoint(string setName, int x, int y)
    {
        if (_sets.ContainsKey(setName))
        {
            _sets[setName].Insert(x, y);
            Console.WriteLine($"Point ({x}, {y}) has been added to {setName}");
        }
        else
        {
            Console.WriteLine($"Set {setName} does not exist");
        }
    }

    internal static void PrintTree(Node node, string setName, string indent = "")
    {
        if (node == null)
        {
            return;
        }

        var rectangle = node.Rectangle;
        if (rectangle.Item1 != null && rectangle.Item2 != null)
        {
            Console.WriteLine($"{indent}[({rectangle.Item1.X}, {rectangle.Item1.Y}), ({rectangle.Item2.X}, {rectangle.Item2.Y})]");
        }

        if (node.Children != null)
        {
            foreach (var child in node.Children)
            {
                PrintTree(child, setName, indent + "│  ");
            }
        }

        if (node.Points != null)
        {
            foreach (var point in node.Points)
            {
                Console.WriteLine($"{indent}└── ({point.X}, {point.Y})");
            }
        }
    }

    internal bool ContainsPoint(string setName, int x, int y)
    {
        if (_sets.ContainsKey(setName))
        {
            return ContainsPoint(_sets[setName]._root, x, y);
        }
        else
        {
            Console.WriteLine($"Set {setName} does not exist");
            return false;
        }
    }

    private bool ContainsPoint(Node node, int x, int y)
    {
        if (node == null)
        {
            return false;
        }

        var rectangle = node.Rectangle;
        if (rectangle.Item1 != null && rectangle.Item2 != null)
        {
            if (x >= rectangle.Item1.X && y >= rectangle.Item1.Y &&
                x <= rectangle.Item2.X && y <= rectangle.Item2.Y)
            {
                if (node.Points.Exists(point => point.X == x && point.Y == y))
                {
                    return true;
                }
                foreach (var child in node.Children)
                {
                    if (ContainsPoint(child, x, y))
                    {
                        return true;
                    }
                }
            }
        }

        return false;
    }
internal List<Point> SearchPoints(string setName)
{
    if (_sets.ContainsKey(setName))
    {
        return SearchPoints(_sets[setName]._root);
    }
    else
    {
        Console.WriteLine($"Set {setName} does not exist");
        return new List<Point>();
    }
}

private List<Point> SearchPoints(Node node)
{
    List<Point> points = new List<Point>();

    if (node != null)
    {
        points.AddRange(node.Points);

        foreach (var child in node.Children)
        {
            points.AddRange(SearchPoints(child));
        }
    }

    return points;
}

internal List<Point> SearchPointsWithQuery(string setName, string query)
{
    if (_sets.ContainsKey(setName))
    {
        string[] parts = query.Split(' ');

        if (parts[0] == "INSIDE")
        {
            string[] bottomLeft = parts[1].Trim('(', ')').Split(',');
            string[] topRight = parts[2].Trim('(', ')').Split(',');
            Point bottomLeftPoint = new Point(int.Parse(bottomLeft[0]), int.Parse(bottomLeft[1]));
            Point topRightPoint = new Point(int.Parse(topRight[0]), int.Parse(topRight[1]));

            return SearchPointsInside(_sets[setName]._root, bottomLeftPoint, topRightPoint);
        }
        else if (parts[0] == "LEFT_OF")
        {
            int x = int.Parse(parts[1]);

            return SearchPointsLeftOf(_sets[setName]._root, x);
        }
        else if (parts[0] == "NN")
        {
            string[] coordinates = parts[1].Trim('(', ')').Split(',');
            Point queryPoint = new Point(int.Parse(coordinates[0]), int.Parse(coordinates[1]));

            return SearchNearestNeighbour(_sets[setName]._root, queryPoint);
        }
        else
        {
            Console.WriteLine($"Invalid query: {query}");
            return new List<Point>();
        }
    }
    else
    {
        Console.WriteLine($"Set {setName} does not exist");
        return new List<Point>();
    }
}

private List<Point> SearchPointsInside(Node node, Point bottomLeft, Point topRight)
{
    List<Point> points = new List<Point>();

    if (node != null)
    {
        foreach (var point in node.Points)
        {
            if (point.X >= bottomLeft.X && point.Y >= bottomLeft.Y &&
                point.X <= topRight.X && point.Y <= topRight.Y)
            {
                points.Add(point);
            }
        }

        foreach (var child in node.Children)
        {
            points.AddRange(SearchPointsInside(child, bottomLeft, topRight));
        }
    }

    return points;
}

private List<Point> SearchPointsLeftOf(Node node, int x)
{
    List<Point> points = new List<Point>();

    if (node != null)
    {
        foreach (var point in node.Points)
        {
            if (point.X < x)
            {
                points.Add(point);
            }
        }

        foreach (var child in node.Children)
        {
            points.AddRange(SearchPointsLeftOf(child, x));
        }
    }

    return points;
}

private List<Point> SearchNearestNeighbour(Node node, Point queryPoint)
{
    List<Point> points = new List<Point>();
    double minDistance = double.MaxValue;

    if (node != null)
    {
        foreach (var point in node.Points)
        {
            double distance = Math.Sqrt(Math.Pow(point.X - queryPoint.X, 2) + Math.Pow(point.Y - queryPoint.Y, 2));

            if (distance < minDistance)
            {
                minDistance = distance;
                points.Clear();
                points.Add(point);
            }
            else if (distance == minDistance)
            {
                points.Add(point);
            }
        }

        foreach (var child in node.Children)
        {
            List<Point> childPoints = SearchNearestNeighbour(child, queryPoint);
            if (childPoints.Count > 0)
            {
                double childMinDistance = Math.Sqrt(Math.Pow(childPoints[0].X - queryPoint.X, 2) + Math.Pow(childPoints[0].Y - queryPoint.Y, 2));

                if (childMinDistance < minDistance)
                {
                    minDistance = childMinDistance;
                    points = childPoints;
                }
                else if (childMinDistance == minDistance)
                {
                    points.AddRange(childPoints);
                }
            }
        }
    }

    return points;
}

}

class RTreeProgram
{
    internal static void Main()
    {
        RTree.CreateSet("cities");
        RTree.InsertPoint("cities", 1, 2);
        RTree.InsertPoint("cities", 3, 4);
        RTree.InsertPoint("cities", 2, 2);
        RTree.InsertPoint("cities", 5, 3);
        RTree.InsertPoint("cities", 4, 4);
        RTree.PrintTree(RTree._sets["cities"]._root, "cities");

        bool contains = RTree._sets["cities"].ContainsPoint("cities", 1, 2);
        Console.WriteLine($"Contains: {contains}");

        List<Point> allPoints = RTree._sets["cities"].SearchPoints("cities");
        Console.WriteLine("All points:");
        foreach (var point in allPoints)
        {
            Console.WriteLine($"({point.X}, {point.Y})");
        }

        List<Point> pointsWithQuery = RTree._sets["cities"].SearchPointsWithQuery("cities", "inside (1, 1), (5, 5)");
        Console.WriteLine("Points matching the query:");
        foreach (var point in pointsWithQuery)
        {
            Console.WriteLine($"({point.X}, {point.Y})");
        }
    }
}
