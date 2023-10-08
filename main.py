from tree_node import *
from forming_dict_of_words import *
# Приклад використання
list_of_collections = list()
documents = [
    "Це перший документ.",
    "Це другий документ.",
    "А це третій документ.",
    "Це також перший документ."
]

inverted_index = build_inverted_index(documents)

# Виведемо результат

collection1 = {tuple(documents): Tree.build_binary_tree_from_dict(inverted_index)}
list_of_collections.append(collection1)
list(list_of_collections[0].values())[0].display()

# # Будуємо бінарне дерево із словника
# tree = Tree.build_binary_tree_from_dict(data_dict)

# # Виводимо корінь дерева
# root_key, root_value = tree.root_item()
# print(f"Корінь: {root_key} -> {root_value}")

# # Виводимо бінарне дерево
# print("Бінарне дерево:")
# tree.display()

# # Видаляємо пару ключ-значення
# tree.delete("banana")

# # Виводимо оновлене бінарне дерево
# print("Після видалення:")
# tree.display()