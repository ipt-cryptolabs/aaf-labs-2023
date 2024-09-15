import re
import math

class Node:
    def __init__(self, x, y, left=None, right=None, parent=None):
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.parent = parent
        self.boundary_start = [x, y]
        self.boundary_end = [x, y]

    def __str__(self):
        if self.is_leaf():
            return f'({self.x}, {self.y})'
        return f'({self.boundary_start}, {self.boundary_end})'

    def is_leaf(self):
        if self.left or self.right:
            return False
        return True

    def children(self):
        return self.left, self.right

class RTree:
    def __init__(self):
        self.root = None

    @staticmethod
    def _calculate_adjustment(node, x, y):
        current_area = abs((node.boundary_start[0] - node.boundary_end[0]) * (node.boundary_start[1] - node.boundary_end[1]))
        new_boundary_start = (min(node.boundary_start[0], x), min(node.boundary_start[1], y))
        new_boundary_end = (max(node.boundary_end[0], x), max(node.boundary_end[1], y))
        new_area = abs((new_boundary_start[0] - new_boundary_end[0]) * (new_boundary_start[1] - new_boundary_end[1]))
        return new_area - current_area

    def insert(self, x, y):
        if self.root is None:
            self.root = Node(x, y)
        else:
            self._insert(self.root, x, y)

    def _insert(self, node, x, y):
        children = node.children()
        if all(children):
            best_child = None
            minimal_adjustment = float('inf')
            for child in children:
                adjustment = self._calculate_adjustment(child, x, y)
                if adjustment < minimal_adjustment:
                    minimal_adjustment = adjustment
                    best_child = child
            self._insert(best_child, x, y)
        else:
            node.left = Node(node.x, node.y, parent=node)
            node.right = Node(x, y, parent=node)
            self._adjust(node, x, y)

    def _adjust(self, node, x, y):
        if not node:
            return
        propagate = False
        if node.boundary_start[0] > x:
            node.boundary_start[0] = x
            propagate = True
        if node.boundary_start[1] > y:
            node.boundary_start[1] = y
            propagate = True
        if node.boundary_end[0] < x:
            node.boundary_end[0] = x
            propagate = True
        if node.boundary_end[1] < y:
            node.boundary_end[1] = y
            propagate = True
        if propagate:
            self._adjust(node.parent, x, y)

    def __str__(self):
        output = f'{self.root}\n'
        if self.root.left:
            output += self._print_tree(self.root.left, is_left=True)
        if self.root.right:
            output += self._print_tree(self.root.right, is_left=False)
        return output

    def _print_tree(self, node, prefix='', is_left=True):
        if node is None:
            return ''
        output = ''
        if is_left:
            output += f'{prefix}├── {node}\n'
            prefix += '|   '
        else:
            output += f'{prefix}└── {node}\n'
            prefix += '    '
        if node.left:
            output += self._print_tree(node.left, prefix, is_left=True)
        if node.right:
            output += self._print_tree(node.right, prefix, is_left=False)
        return output

    def __contains__(self, item):
        if isinstance(item, list) or isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError('Only a list of length 2 can be contained in an R-Tree')
            if not self.root:
                return False
            else:
                return self._contains(self.root, item[0], item[1])
        elif isinstance(item, Node):
            if not self.root:
                return False
            else:
                return self._contains(self.root, item.x, item.y)
        else:
            raise ValueError('Only a list of length 2 can be contained in an R-Tree')

    def _contains(self, node, x, y):
        if any(node.children()):
            if node.boundary_start[0] > x or \
               node.boundary_start[1] > y or \
               node.boundary_end[0] < x or \
               node.boundary_end[1] < y:
                return False
        else:
            return node.x == x and node.y == y
        return any([self._contains(child, x, y) for child in node.children()])

    def search(self, left_of=None, nn=None, inside=None):
        if not self.root:
            return
        else:
            self._search(self.root, left_of=left_of, nn=nn, inside=inside)

    def _search(self, node, left_of=None, nn=None, inside=None):
        if nn:
            nearest_neighbor = self.search_nearest_neighbor(nn[0], nn[1])
            if not nearest_neighbor:
                return
            print(f'({nearest_neighbor[1]}, {nearest_neighbor[2]})')
            return

        if inside:
            if node.boundary_end[0] < inside[0][0] or \
               node.boundary_start[0] > inside[1][0] or \
               node.boundary_end[1] < inside[0][1] or \
               node.boundary_start[1] > inside[1][1]:
                return

        if left_of:
            if node.boundary_start[0] >= left_of:
                return

        if node.is_leaf():
            print(node)

        if node.left:
            self._search(node.left, left_of=left_of, inside=inside)
        if node.right:
            self._search(node.right, left_of=left_of, inside=inside)

    def search_nearest_neighbor(self, x, y):
        if not self.root:
            return None
        elif self.root.is_leaf():
            return self.root
        else:
            return self._search_nearest_neighbor(self.root, x, y)

    def _search_nearest_neighbor(self, node, x, y):
        if node.is_leaf():
            return math.hypot(node.x - x, node.y - y), node.x, node.y
        return min([self._search_nearest_neighbor(child, x, y) for child in node.children() if child is not None], key=lambda x: x[0])

if __name__ == '__main__':
    AVAILABLE_ACTIONS = ['create', 'insert', 'print_tree', 'contains', 'search', 'exit']
    CONDITIONS = ['inside', 'left_of', 'nn']
    POINT_REGEX = re.compile('\(\s*[-+]?(?:\d*\.\d+|\d+)\s*,\s*[-+]?(?:\d*\.\d+|\d+)\s*\)')
    ALL_POINTS_REGEX = r'\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*(?:,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*)*\)'
    POINT_FROM_POINT_REGEX = re.compile('\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)')
    TREES = {}
    try:
        while True:
            command = input('> ')
            while ';' not in command:
                command += '\n'
                command += input('  ')
            command = command.split(';', 1)[0]

            action = command.split()[0].lower()
            if action not in AVAILABLE_ACTIONS:
                print(f'Error: Unknown command near {action[:16]}')
                continue
            elif action == 'create':
                if len(command.split()) > 2:
                    print(f'Error: Unexpected argument near {command.split()[2][:16]}')
                    continue
                try:
                    tree_name = command.split()[1]
                except IndexError:
                    print(f'Error: Not enough arguments')
                    continue
                TREES.update({tree_name: RTree()})
                print(f'Tree "{tree_name}" was created successfully')
                continue
            elif action == 'insert':
                if len(command.split()) < 2:
                    print(f'Error: Not enough arguments')
                    continue
                tree_name = command.split()[1]
                if tree_name not in TREES:
                    print(f'Error: Tree with name "{tree_name}" was not found')
                    continue
                point_to_insert = None
                for point_to_insert in re.finditer(ALL_POINTS_REGEX, ' '.join(command.split()[2:])):
                    x = float(point_to_insert.groups()[0])
                    y = float(point_to_insert.groups()[1])
                    TREES[tree_name].insert(x, y)
                if point_to_insert:
                    if len(''.join(command.split()[2:])[point_to_insert.end():].split()):
                        print(f'Error: Unexpected argument near {"".join(command.split()[2:])[point_to_insert.end():]}')
                        break
                else:
                    if not point_to_insert:
                        print('Error: Invalid argument for point')
                        continue
            elif action == 'print_tree':
                if len(command.split()) > 2:
                    print(f'Error: Unexpected argument near {command.split()[2][:16]}')
                    continue
                try:
                    tree_name = command.split()[1]
                except IndexError:
                    print(f'Error: Not enough arguments')
                    continue
                print(TREES[tree_name])
            elif action == 'contains':
                if len(command.split()) < 2:
                    print(f'Error: Not enough arguments')
                    continue
                tree_name = command.split()[1]
                if tree_name not in TREES:
                    print(f'Error: Tree with name "{tree_name}" was not found')
                    continue
                point_to_search = POINT_REGEX.search(' '.join(command.split()[2:]))
                if not point_to_search:
                    print('Error: Invalid argument for point')
                    continue
                if len(''.join(command.split()[2:])[point_to_search.end():].split()):
                    print(f'Error: Unexpected argument near {"".join(command.split()[2:])[point_to_search.end():point_to_search.end()+16]}')
                    continue
                new_point = POINT_FROM_POINT_REGEX.findall(point_to_search.group(0))[0]
                x = float(new_point[0])
                y = float(new_point[1])
                print((x, y) in TREES[tree_name])
            elif action == 'search':
                if len(command.split()) < 2:
                    print(f'Error: Not enough arguments')
                    continue
                tree_name = command.split()[1]
                if tree_name not in TREES:
                    print(f'Error: Tree with name "{tree_name}" was not found')
                    continue
                if len(command.split()) == 2:
                    TREES[tree_name].search()
                elif len(command.split()) == 3:
                    if command.split()[2].lower() != 'where':
                        print(f'Error: Unexpected argument near {command.split()[2][:16]}')
                        continue
                    print(f'Error: No condition provided near WHERE')
                    continue
                elif len(command.split()) == 4:
                    if command.split()[2].lower() != 'where':
                        print(f'Error: Unexpected argument near {command.split()[2][:16]}')
                        continue
                    if command.split()[3].lower() not in CONDITIONS:
                        print(f'Error: Unexpected condition near {command.split()[3][:16]}')
                        continue
                    print(f'Error: No condition provided near {command.split()[3][:16]}')
                    continue
                else:
                    if command.split()[2].lower() != 'where':
                        print(f'Error: Unexpected argument near {command.split()[2][:16]}')
                        continue
                    condition = command.split()[3].lower()
                    if condition not in CONDITIONS:
                        print(f'Error: Unexpected condition near {command.split()[3][:16]}')
                    if condition == 'inside':
                        points = re.finditer(ALL_POINTS_REGEX, ' '.join(command.split()[2:]))
                        try:
                            point1 = next(points)
                            x1 = float(point1.groups()[0])
                            y1 = float(point1.groups()[1])
                        except StopIteration:
                            print('Not enough arguments to search')
                            continue
                        try:
                            point2 = next(points)
                            x2 = float(point2.groups()[0])
                            y2 = float(point2.groups()[1])
                        except StopIteration:
                            print('Not enough arguments to search')
                            continue
                        if len(''.join(command.split()[2:])[point2.end():].split()):
                            print(f'Error: Unexpected argument near {"".join(command.split()[2:])[point2.end():]}')
                            continue
                        if x2 < x1 or y2 < y1:
                            print('Invalid search range')
                            continue
                        TREES[tree_name].search(inside=((x1, y1), (x2, y2)))
                    elif condition == 'left_of':
                        if len(command.split()) > 5:
                            print(f'Error: Unexpected argument near {command.split()[5][:16]}')
                            continue
                        left_of = float(command.split()[4])
                        TREES[tree_name].search(left_of=left_of)
                    elif condition == 'nn':
                        point_to_search = POINT_REGEX.search(' '.join(command.split()[4:]))
                        if len(''.join(command.split()[4:])[point_to_search.end():].split()):
                            print(f'Error: Unexpected argument near {"".join(command.split()[4:])[point_to_search.end():point_to_search.end()+16]}')
                            continue
                        new_point = POINT_FROM_POINT_REGEX.findall(point_to_search.group(0))[0]
                        x = float(new_point[0])
                        y = float(new_point[1])
                        TREES[tree_name].search(nn=(x, y))


    except KeyboardInterrupt:
        print('Exiting...')
        exit()