package com.lab.db.r_tree;

import java.util.*;

public class RTree {
    private static class Node {
        Node parent;
        Node LeftChild, RightChild;
        int[] segment;

        Node() {
            LeftChild = null;
            RightChild = null;
            segment = new int[2];
            parent = null;
        }
        void setLeftChild(int[] segment) {
            Node node = new Node();
            node.addSegment(segment);
            node.parent = this;
            this.LeftChild = node;
        }
        void setRightChild(int[] segment) {
            Node node = new Node();
            node.addSegment(segment);
            node.parent = this;
            this.RightChild = node;
        }

        boolean isLeaf() {
            return LeftChild == null && RightChild == null;
        }

        void addSegment(int[] segment) {
            this.segment[0] = segment[0];
            this.segment[1] = segment[1];
        }
    }

    private Node root;

    public RTree() {
        root = new Node();
    }
    void updateBounds(Node node, int[] segment) {
        node.segment[0] = Math.min(node.segment[0], segment[0]);
        node.segment[1] = Math.max(node.segment[1], segment[1]);
    }
    public void insert(int[] segment) {
        if (root.segment[0] == 0 && root.segment[1] == 0) {
            root.addSegment(segment);
        }
        else {
            Node node = chooseNode(root, segment);

            Node l = node;
            node.setLeftChild(l.segment);
            Node r = new Node();
            r.addSegment(segment);
            node.setRightChild(r.segment);
            Node x = node.RightChild;
            while (x.parent != null) {
                updateBounds(x, segment);
                x = x.parent;
            }
            updateBounds(root, segment);
        }
    }
    private boolean intersect(int[] bounds1, int[] bounds2) {
        // Check if the two bounding boxes intersect.
        return !(bounds1[1] < bounds2[0] || bounds1[0] > bounds2[1]);
    }
    private Node chooseNode(Node node, int[] segment) {
        if (node.isLeaf()) {
            return node;
        } else {
            Node bestChild = null;
            int area1 = intersectArea(node.LeftChild.segment, segment);
            int area2 = intersectArea(node.RightChild.segment, segment);
            bestChild = area1 > area2 ? node.LeftChild : node.RightChild;
            return chooseNode(bestChild, segment);
        }
    }
    private int area(int[] bounds) {
        // Calculate the area of a bounding box.
        return Math.abs(bounds[1] - bounds[0]);
    }
    private int intersectArea(int[] bounds1, int[] bounds2) {
        // Calculate the union of two bounding boxes.
        if (intersect(bounds1, bounds2)) {
            int[] result = new int[2];
            result[0] = Math.max(bounds1[0], bounds2[0]);
            result[1] = Math.min(bounds1[1], bounds2[1]);
            return result[1] - result[0];
        }
        else {return 0;}
    }
    private int[] union(int[] bounds1, int[] bounds2) {
        // Calculate the union of two bounding boxes.
        int[] result = new int[2];
        result[0] = Math.min(bounds1[0], bounds2[0]);
        result[1] = Math.max(bounds1[1], bounds2[1]);
        return result;
    }
//
//    public List<int[]> search(int[] segment) {
//        List<int[]> result = new ArrayList<>();
//        search(root, segment, result);
//        return result;
//    }
//
//    private void search(Node node, int[] segment, List<int[]> result) {
//        if (node.isLeaf()) {
//            for (int[] s : node.segments) {
//                if (intersect(s, segment)) {
//                    result.add(s);
//                }
//            }
//        } else {
//            for (Node child : node.children) {
//                if (intersect(child.bounds, segment)) {
//                    search(child, segment, result);
//                }
//            }
//        }
//    }


//    public void print() {
//        print(root, "");
//    }
//
//    private void print(Node node, String prefix) {
//        if (node.isLeaf()) {
//            System.out.println(prefix + "└── " + Arrays.toString(node.bounds));
//            for (int[] segment : node.segments) {
//                System.out.println(prefix + "    ├── " + Arrays.toString(segment));
//            }
//        } else {
//            System.out.println(prefix + "├── " + Arrays.toString(node.bounds));
//
//            int childCount = node.children.size();
//            for (int i = 0; i < childCount - 1; i++) {
//                print(node.children.get(i), prefix + "│   ");
//            }
//            if (childCount > 0) {
//                print(node.children.get(childCount - 1), prefix + "    ");
//            }
//        }
//    }
}