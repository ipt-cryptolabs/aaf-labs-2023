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
    private boolean in(int[] in, int[] out) {
        return in[0] >= out[0] && in[1] <= out[1];
    }
    public boolean search(int[] segment) {
        return search(root, segment);
    }

    private boolean search(Node node, int[] segment) {
        if (Arrays.equals(node.segment, segment)) {
            return true;
        }
        if (Arrays.equals(node.LeftChild.segment, segment)) {
            return true;
        }
        if (Arrays.equals(node.RightChild.segment, segment)) {
            return true;
        }
        if (in(node.RightChild.segment, segment)) {
            return search(node.RightChild, segment);
        }
        else if (in(node.LeftChild.segment, segment)) {
            return search(node.LeftChild. segment);
        }
        return false;
    }


    public void print() {
        print(root, "");
    }

    private void print(Node node, String prefix) {
        if (node.isLeaf()) {
            System.out.println(prefix + "└── " + Arrays.toString(node.segment));
        } else {
            System.out.println(prefix + "├── " + Arrays.toString(node.segment));
            print(node.LeftChild, prefix + "│    ");
            print(node.RightChild, prefix + "│    ");
        }
    }
    public void left_of(int l) {
        left_of_helper(root, l);
    }
    private void left_of_helper(Node node, int l) {
        if (node.segment[1] <= l) {
            System.out.println(Arrays.toString(node.segment));
        }
        if (!node.isLeaf()) {
            if (node.LeftChild.segment[0] <= l) {
                left_of_helper(node.LeftChild, l);
            }
            if (node.RightChild.segment[0] <= l) {
                left_of_helper(node.RightChild, l);
            }
        }
    }
    public void contains(int[] segment) {
        contains_helper(root, segment);
    }
    private void contains_helper(Node node,int[] segment) {
        if (in( segment, node.segment)) {
            System.out.println(Arrays.toString(node.segment));
        }
        if (!node.isLeaf()) {
            contains_helper(node.LeftChild, segment);
            contains_helper(node.RightChild, segment);
        }
    }
    public void intersects(int[] segment) {
        intersects_helper(root, segment);
    }
    private void intersects_helper(Node node, int[] segment) {
        if (intersect(segment, node.segment)) {
            System.out.println(Arrays.toString(node.segment));
        }
        if (!node.isLeaf()) {
            if (intersect(node.LeftChild.segment, segment)) {
                intersects_helper(node.LeftChild, segment);
            }
            if (intersect(node.LeftChild.segment, segment)) {
                intersects_helper(node.RightChild, segment);
            }
        }
    }
}