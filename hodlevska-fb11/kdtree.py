import math


class Node:
    def __init__(self, point, left=None, right=None, axis=None):
        self.point = point
        self.left = left
        self.right = right
        self.axis = axis


class KDTree:
    def __init__(self):
        self.root = None


    def insert(self, point, depth=0, node=None):
        if self.root is None:
            self.root = Node(point, axis=0)
            return

        axis = depth % 2

        if node is None:
            node = self.root

        if point[axis] < node.point[axis]:
            if node.left is None:
                node.left = Node(point, axis=(axis + 1) % 2)
            else:
                self.insert(point, depth + 1, node.left)
        else:
            if node.right is None:
                node.right = Node(point, axis=(axis + 1) % 2)
            else:
                self.insert(point, depth + 1, node.right)


    def _tree_traversal(self, node=None):
        if node is None:
            node = self.root

        if node.left:
            yield from self._tree_traversal(node.left)
        
        yield node.point

        if node.right:
            yield from self._tree_traversal(node.right)
    
 
    def __iter__(self):
        yield from self._tree_traversal(self.root)


    def contains(self, target, node):
        if node is None:
            return False

        if target[0] == node.point[0] and target[1] == node.point[1]:
            return True

        axis = node.axis
        if target[axis] < node.point[axis]:
            return self.contains(target, node.left)
        else:
            return self.contains(target, node.right)


    def print_tree(self):
        stack = [(self.root, 0)]

        while stack:
            node, indent = stack.pop()
            if node:
                print(" " * indent + f"{node.point}")
                stack.append((node.right, indent + 4))
                stack.append((node.left, indent + 4))


    def points_inside_rectangle(self, x_left, y_bottom, x_right, y_top):
        result = []
        self._find_points_inside_rectangle(self.root, x_left, y_bottom, x_right, y_top, 0, result)
        return result
    

    def _find_points_inside_rectangle(self, node, x_left, y_bottom, x_right, y_top, depth, result):
        if node is None:
            return

        current_axis = depth % 2 

        if x_left <= node.point[0] <= x_right and y_bottom <= node.point[1] <= y_top:
            result.append(node.point)

        if current_axis == 0:
            if x_left <= node.point[0]:
                self._find_points_inside_rectangle(node.left, x_left, y_bottom, x_right, y_top, depth + 1, result)
            if node.point[0] <= x_right:
                self._find_points_inside_rectangle(node.right, x_left, y_bottom, x_right, y_top, depth + 1, result)
        else:
            if y_bottom <= node.point[1]:
                self._find_points_inside_rectangle(node.left, x_left, y_bottom, x_right, y_top, depth + 1, result)
            if node.point[1] <= y_top:
                self._find_points_inside_rectangle(node.right, x_left, y_bottom, x_right, y_top, depth + 1, result)


    def above_to(self, y):
        result = []
        self._find_above_to(self.root, y, 0, result)
        return result

    def _find_above_to(self, node, y, depth, result):
        if node is None:
            return

        current_axis = depth % 2

        if node.point[1] > y:
            result.append(node.point)

        if node.point[1] > y or current_axis == 1:
            self._find_above_to(node.left, y, depth + 1, result)
        if node.point[1] <= y or current_axis == 1:
            self._find_above_to(node.right, y, depth + 1, result)


    def nn(self, x, y):
        result = []
        target_point = (x, y)
        self._find_nn(self.root, target_point, result)
        return result


    def _find_nn(self, node, target_point, result):
        if node is None:
            return

        current_distance = math.dist(node.point, target_point)

        if not result or current_distance < math.dist(result[0], target_point):
            result.clear()
            result.append(node.point)
        elif current_distance == math.dist(result[0], target_point):
            result.append(node.point)

        if node.point[0] > target_point[0] or (node.point[0] == target_point[0] and node.point[1] > target_point[1]):
            self._find_nn(node.left, target_point, result)
        else:
            self._find_nn(node.right, target_point, result)
