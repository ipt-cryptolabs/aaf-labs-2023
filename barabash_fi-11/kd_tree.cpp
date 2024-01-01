#include "head.h"

kd_tree::kd_tree()
{
	root = NULL;
}

kd_tree::~kd_tree()
{
	delete_tree(root);
}

void kd_tree::delete_tree(Node *current)
{
    if (current != NULL){
        delete_tree(current->left);
        delete_tree(current->right);
        delete current;
    }
}

void kd_tree::insert(int l, int h)
{
    if (root!=NULL){
        Node *current = NULL;
        Node *next = root;
        bool a_comparison = 0;
        bool coordinate_bigger;
        while (next!=NULL){
            current = next;
            a_comparison = !(a_comparison);
            coordinate_bigger = 0;
            if (a_comparison){
                if ((current->a)<l)
                    coordinate_bigger = 1;
            } else {
                if ((current->b)<h)
                    coordinate_bigger = 1;
            }
            if (coordinate_bigger)
                next = current->right;
            else
                next = current->left;
        }
        next = new Node;
        next->left = NULL;
        next->right = NULL;
        next->a = l;
        next->b = h;
        if (coordinate_bigger)
            current->right = next;
        else
            current->left = next;
    }
    else {
        root = new Node;
        root->left = NULL;
        root->right = NULL;
        root->a = l;
        root->b = h;
    }
}

bool kd_tree::contains(int l, int h)
{
    bool in_tree = 0;
    if (root!=NULL){
        Node *current = NULL;
        Node *next = root;
        bool a_comparison = 0;
        bool coordinate_bigger;
        while (next!=NULL){
            current = next;
            if ((current->a == l)&&(current->b == h)){
                in_tree = 1;
                break;
            }
            a_comparison = !(a_comparison);
            coordinate_bigger = 0;
            if (a_comparison){
                if ((current->a)<l)
                    coordinate_bigger = 1;
            } else {
                if ((current->b)<h)
                    coordinate_bigger = 1;
            }
            if (coordinate_bigger)
                next = current->right;
            else
                next = current->left;
        }

    }
    return in_tree;
}

void kd_tree::print_tree()
{
    print_leaf(root, "", "");
}

void kd_tree::print_leaf(Node *current, string prefix, string childprefix)
{
    if (current!=NULL){
        cout<<prefix<<"["<<current->a<<", "<<current->b<<"]\n";
        Node *left = current->left;
        if (left==NULL){
            print_leaf(current->right, childprefix+"'---", childprefix + "    ");
        }
        else{
            print_leaf(current->right, childprefix+">---", childprefix + "|   ");
            print_leaf(current->left , childprefix+"'---", childprefix + "    ");
        }
    }
}

void kd_tree::search(string type, int l, int h)
{
    if (type == "EOF")
        all(root);
    else if (type == "RIGHT_OF")
        right_of(root, l, 1);
    else if (type == "CONTAINED_BY")
        cointained_by(root, l, h, 1);
    else if (type == "INTERSECTS")
        intersects(root, l, h, 1);
}

void kd_tree::all(Node *current)
{
    if (current!=NULL){
        all(current->left);
        all(current->right);
        cout<<"["<<current->a<<", "<<current->b<<"] ";
    }
}

void kd_tree::cointained_by(Node *current, int l, int h, bool a_comparison)
{
    if (current!=NULL){
        int a = current->a;
        int b = current->b;
        if (a_comparison){
            if (a<=h) cointained_by(current->right, l, h, !(a_comparison));
            if (a>=l) cointained_by(current->left, l, h, !(a_comparison));
        } else {
            if (b<=h) cointained_by(current->right, l, h, !(a_comparison));
            if (b>=l) cointained_by(current->left, l, h, !(a_comparison));
        }
        if ((l<=a)&&(b<=h)) cout<<"["<<a<<", "<<b<<"] ";
    }
}

void kd_tree::intersects(Node *current, int l, int h, bool a_comparison)
{
    if (current!=NULL){
        int a = current->a;
        int b = current->b;
        if (a_comparison){
            intersects(current->left, l, h, !(a_comparison));
            if (a<=h) intersects(current->right, l, h, !(a_comparison));
        } else {
            intersects(current->right, l, h, !(a_comparison));
            if (l<=b) intersects(current->left, l, h, !(a_comparison));
        }
        if (!((b<l)||(a>h))) cout<<"["<<a<<", "<<b<<"] ";
    }
}

void kd_tree::right_of(Node *current, int l, bool a_comparison)
{
    if (current!=NULL){
        int a = current->a;
        int b = current->b;
        if (a_comparison){
            right_of(current->right, l, !(a_comparison));
            if (l<=a){
                right_of(current->left, l, !(a_comparison));
                cout<<"["<<a<<", "<<b<<"] ";
            }
        } else {
            right_of(current->right, l, !(a_comparison));
            if (l<=b){
                right_of(current->left, l, !(a_comparison));
                if (l<=a) cout<<"["<<a<<", "<<b<<"] ";
            }
        }
    }
}

