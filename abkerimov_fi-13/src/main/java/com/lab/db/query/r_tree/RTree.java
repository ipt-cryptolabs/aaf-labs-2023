//package com.lab.db.query.r_tree;
//
//import java.util.HashSet;
//import java.util.Set;
//
//
//class RTreeNode {
//    private int l;
//    private int r;
//
//    public void setL(int l) {
//        this.l = l;
//    }
//
//    public void setR(int r) {
//        this.r = r;
//    }
//
//    public RTreeNode getLeftChild() {
//        return leftChild;
//    }
//
//    public RTreeNode getRightChild() {
//        return rightChild;
//    }
//
//    private RTreeNode leftChild = null;
//    private RTreeNode rightChild = null;
//    public RTreeNode(int l, int r) {
//        this.l = l;
//        this.r = r;
//    }
//    public int getL() {
//        return l;
//    }
//
//    public int getR() {
//        return r;
//    }
//    public void setLeftChild(RTreeNode leftChild) {
//        this.leftChild = leftChild;
//    }
//    public void setRightChild(RTreeNode rightChild) {
//        this.rightChild = rightChild;
//    }
//}
//
//public final class RTree {
//    private RTreeNode root = null;
//    public void insert(RTreeNode node) {
//        if (this.root == null) {
//            this.root = node;
//        }
//        else {
//            updateRoot(node);
//        }
//    }
////    private RTreeNode chooseLeaf(RTreeNode node) {
////
////    }
//    private void insert() {
//
//    }
//    private void chooseLeaf(RTreeNode node) {
//        if (node.getLeftChild() == null) {
//            doInsert();
//        }
//    }
//    private void linearSplit() {}
//    private void doInsert() {}
//
//    private void adjustBounds(int l, int r) {
//        this.root.setL(Math.min(this.root.getL(), l));
//        this.root.setR(Math.max(this.root.getR(), r));
//    }
//
//}
