package com.lab.db;

import com.lab.db.parser.Interface;
import com.lab.db.parser.*;
import com.lab.db.r_tree.RTree;

public class Main {
    public static void main(String[] args) {
        //Interface _interface = new Interface();
        RTree r = new RTree();
        r.insert(new int[] {3, 4});
        r.insert(new int[] {2, 7});
        r.insert(new int[] {5, 8});
        r.insert(new int[] {4, 6});
        r.insert(new int[] {5, 10});
    }
}
