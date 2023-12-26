from typing import Generator


class RDNode:
    def __init__(self, data=None, bounding_box=None, parent=None) -> None:
        self.data = data
        self.bounding_box = bounding_box
        self.children = []
        self.parrent = parent


    def _update_bbox(self, new_data: set):
        self.bounding_box = self.bounding_box.union(new_data)


    def __str__(self) -> str:
        return f"RDNode<{self.bounding_box}>"
    

    def __repr__(self) -> str:
        return self.__str__()
    

class RDTree:
    def __init__(self, root=None) -> None:
        self.root = root
        self.max_children = 4


    def insert(self, data: set) -> None:
        if self.root is None:
            self.root = RDNode(data=data, bounding_box=self._calc_bbox(data))
        else:
            if self.contains(data):
                raise Exception("This set already exists")
            
            self._insert_recursive(data=data, root_node=self.root)


    def _find_prop_child(self, data: set, root_node: RDNode) -> tuple[RDNode, bool]:
        intersec = 0
        min_child_len = 999999
        child_with_min_bbox = None

        for child in root_node.children:
            if (temp_intersec := self._find_diff(data, child.bounding_box)) > intersec:
                intersec = temp_intersec
                prop_kid = child
            
            elif temp_intersec == intersec and intersec > 0:
                if len(child.bounding_box) < len(prop_kid.bounding_box):
                    prop_kid = child
                else:
                    continue

            if (len(child.bounding_box) < min_child_len):
                child_with_min_bbox = child
                min_child_len = len(child.bounding_box)

        if intersec == 0:
            return child_with_min_bbox, False

        return prop_kid, True
    

    def _find_diff(self, data: set, bounding_box: set) -> int:
        return len(bounding_box.intersection(data))


    def _insert_recursive(self, data: set, root_node: RDNode) -> None:
        root_node.bounding_box = root_node.bounding_box.union(data)

        if root_node.children:
            prop_kid, is_intersec_found = self._find_prop_child(data, root_node)

            if not is_intersec_found and (len(root_node.children) < self.max_children):
                root_node.children.append(RDNode(data, self._calc_bbox(data)))
                return

            self._insert_recursive(data, prop_kid)
        else:
            another_child = RDNode(root_node.data, self._calc_bbox(root_node.data))
            root_node.children.append(another_child)
            root_node.children.append(RDNode(data, self._calc_bbox(data)))
            
    
    def _calc_bbox(self, data: set) -> set:
        return data
    

    def _tree_traversal(self, node: RDNode) -> Generator:
        if not node.children:
            yield node.data
        
        else:
            for child in node.children:
                yield from self._tree_traversal(child)

                
    def contains(self, data: set) -> bool:
        return self._contains_recursive(data, self.root)


    def _contains_recursive(self, data: set, root_node: RDNode, was_found=False) -> bool:
        if not root_node.children:
            if root_node.data == data:
                return True
            return False
        
        for child in root_node.children:
            if not data.issubset(child.bounding_box):
                continue
            was_found = self._contains_recursive(data, child, was_found)

            if was_found:
                break
        
        return was_found


    def search(self, data=None, condition=None) -> list:
        if not condition:
            return [s for s in self]
        
        if condition == "CONTAINS":
            return self._cond_contains(data)

        if condition == "CONTAINED_BY":
            return self._cond_contained_by(data)

        if condition == "INTERSECTS":
            return self._cond_intersects(data)


    def _cond_contains(self, data: set) -> list:
        res = []
        return self._cond_contains_recursive(data, self.root, res)


    def _cond_contains_recursive(self, data: set, root_node: RDNode, result: list) -> list:
        if not root_node.children:
            if root_node.data.issuperset(data):
                return result + [root_node.data]
            return result
        
        for child in root_node.children:
            if not data.issubset(child.bounding_box):
                continue
            result = self._cond_contains_recursive(data, child, result)
        
        return result


    def _cond_contained_by(self, data: set) -> list:
        res = []
        return self._cond_contained_by_recursive(data, self.root, res)


    def _cond_contained_by_recursive(self, data: set, root_node: RDNode, result: list) -> list:
        if not root_node.children:
            if root_node.data.issubset(data):
                return result + [root_node.data]
            return result
        
        for child in root_node.children:
            if not data.intersection(child.bounding_box):
                continue
            result = self._cond_contained_by_recursive(data, child, result)
        
        return result


    def _cond_intersects(self, data: set) -> list:
        res = []
        return self._cond_intersects_recursive(data, self.root, res)


    def _cond_intersects_recursive(self, data: set, root_node: RDNode, result: list) -> list:
        if not root_node.children:
            if root_node.data.intersection(data):
                return result + [root_node.data]
            return result
        
        for child in root_node.children:
            if not data.intersection(child.bounding_box):
                continue
            result = self._cond_intersects_recursive(data, child, result)
        
        return result

 
    def __iter__(self) -> Generator:
        yield from self._tree_traversal(self.root)


def print_rdtree(root: RDNode, last=True, header='') -> None:
    elbow = "└──"
    pipe = "│  "
    tee = "├──"
    blank = "   "
    print(header + (elbow if last else tee) + str(root))

    children = root.children
    for i, c in enumerate(children):
        print_rdtree(c, header=header + (blank if last else pipe), last=i == len(children) - 1)


if __name__ == "__main__":
    t = RDTree()

    t.insert({1, 3})
    t.insert({9, 12})
    t.insert({21, 18})
    t.insert({115})
    t.insert({97})
    t.insert({1, 3, 4})
    t.insert({1, 3, 5})
    t.insert({1, 3, 6})
    t.insert({1, 3, 7})
    t.insert({1, 3, 8})

    print("\nRDTree")
    print_rdtree(t.root)
    t.insert({9, 21214, 21421111, 22})
    print("\nRDTree")
    print_rdtree(t.root)


    print(t.search())
    print(t.search({22, 13, 9, 17, 15}, "INTERSECTS"))
