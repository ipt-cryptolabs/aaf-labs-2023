import re

class Node:
    def __init__(self, start, end, left=None, right=None, parent=None):
        self.start = start
        self.end = end
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return f'[{self.start}, {self.end}]'

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
    def _calculate_adjustment(node, start, end):
        left_adjustment = max(node.start - start, 0)
        right_adjustment = max(end - node.end, 0)
        return left_adjustment + right_adjustment

    def insert(self, start, end):
        if self.root is None:
            self.root = Node(start, end)
        else:
            self._insert(self.root, start, end)

    def _insert(self, node, start, end):
        children = node.children()
        if all(children):
            best_child = None
            minimal_adjustment = float('inf')
            for child in children:
                adjustment = self._calculate_adjustment(child, start, end)
                if adjustment < minimal_adjustment:
                    minimal_adjustment = adjustment
                    best_child = child
            self._insert(best_child, start, end)
        else:
            node.left = Node(node.start, node.end, parent=node)
            node.right = Node(start, end, parent=node)
            if self._calculate_adjustment(node, start, end):
                self._adjust(node, start, end)

    def _adjust(self, node, start, end):
        if not node:
            return
        propagate = False
        if node.start > start:
            node.start = start
            propagate = True
        if node.end < end:
            node.end = end
            propagate = True
        if propagate:
            self._adjust(node.parent, start, end)

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
                return self._contains(self.root, item.start, item.end)
        else:
            raise ValueError('Only a list of length 2 can be contained in an R-Tree')

    def _contains(self, node, start, end):
        if any(node.children()):
            if node.start > start or node.end < end:
                return False
        else:
            return node.start == start and node.end == end
        return any([self._contains(child, start, end) for child in node.children()])

    def search(self, contains=None, intersects=None, left_of=None):
        if not self.root:
            return
        else:
            self._search(self.root, contains=contains, intersects=intersects, left_of=left_of)

    def _search(self, node, contains=None, intersects=None, left_of=None):
        if contains:
            if node.start > contains[0]:
                return
            if node.end < contains[1]:
                return

        if intersects:
            if not (intersects[1] >= node.start and node.end >= intersects[0]):
                return

        if node.is_leaf():
            if left_of:
                if node.end > left_of:
                    return
            print(node)

        if node.left:
            self._search(node.left, contains=contains, intersects=intersects, left_of=left_of)
        if node.right:
            self._search(node.right, contains=contains, intersects=intersects, left_of=left_of)


if __name__ == '__main__':
    AVAILABLE_ACTIONS = ['create', 'insert', 'print_tree', 'contains', 'search', 'exit']
    CONDITIONS = ['contains', 'intersects', 'left_of']
    LIST_REGEX = re.compile('\[\s*[-+]?(?:\d*\.\d+|\d+)\s*,\s*[-+]?(?:\d*\.\d+|\d+)\s*]')
    ALL_LISTS_REGEX = r'\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*(?:,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*)*]'
    RANGE_FROM_LIST_REGEX = re.compile('\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*]')
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
                range_to_insert = None
                for range_to_insert in re.finditer(ALL_LISTS_REGEX, ' '.join(command.split()[2:])):
                    start = float(range_to_insert.groups()[0])
                    end = float(range_to_insert.groups()[1])
                    if start > end:
                        print(f'Error: Invalid argument for range near [{start}, {end}]')
                        continue
                    TREES[tree_name].insert(start, end)
                if range_to_insert:
                    if len(''.join(command.split()[2:])[range_to_insert.end():].split()):
                        print(f'Error: Unexpected argument near {"".join(command.split()[2:])[range_to_insert.end():]}')
                        break
                else:
                    if not range_to_insert:
                        print('Error: Invalid argument for range')
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
                range_to_search = LIST_REGEX.search(' '.join(command.split()[2:]))
                if not range_to_search:
                    print('Error: Invalid argument for range')
                    continue
                if len(''.join(command.split()[2:])[range_to_search.end():].split()):
                    print(f'Error: Unexpected argument near {"".join(command.split()[2:])[range_to_search.end():range_to_search.end()+16]}')
                    continue
                new_range = RANGE_FROM_LIST_REGEX.findall(range_to_search.group(0))[0]
                start = float(new_range[0])
                end = float(new_range[1])
                if start > end:
                    print(f'Error: Invalid argument for range near [{start}, {end}]')
                    continue
                print((start, end) in TREES[tree_name])
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
                    print(f'Error: No condition provided near {command.split()[3][:16]}')
                    continue
                else:
                    if command.split()[2].lower() != 'where':
                        print(f'Error: Unexpected argument near {command.split()[2][:16]}')
                        continue
                    condition = command.split()[3].lower()
                    if condition not in CONDITIONS:
                        print(f'Error: Unexpected condition near {command.split()[3][:16]}')
                    if condition == 'contains':
                        range_to_search = LIST_REGEX.search(' '.join(command.split()[4:]))
                        if len(''.join(command.split()[4:])[range_to_search.end():].split()):
                            print(f'Error: Unexpected argument near {"".join(command.split()[4:])[range_to_search.end():range_to_search.end()+16]}')
                            continue
                        new_range = RANGE_FROM_LIST_REGEX.findall(range_to_search.group(0))[0]
                        start = float(new_range[0])
                        end = float(new_range[1])
                        TREES[tree_name].search(contains=(start, end))
                    elif condition == 'intersects':
                        range_to_search = LIST_REGEX.search(' '.join(command.split()[4:]))
                        if len(''.join(command.split()[4:])[range_to_search.end():].split()):
                            print(f'Error: Unexpected argument near {"".join(command.split()[4:])[range_to_search.end():range_to_search.end()+16]}')
                            continue
                        new_range = RANGE_FROM_LIST_REGEX.findall(range_to_search.group(0))[0]
                        start = float(new_range[0])
                        end = float(new_range[1])
                        TREES[tree_name].search(intersects=(start, end))
                    elif condition == 'left_of':
                        if len(command.split()) > 5:
                            print(f'Error: Unexpected argument near {command.split()[5][:16]}')
                            continue
                        left_of = float(command.split()[4])
                        TREES[tree_name].search(left_of=left_of)


    except KeyboardInterrupt:
        print('Exiting...')
        exit()