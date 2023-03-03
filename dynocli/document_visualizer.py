from rich.tree import Tree
from rich.console import Console


class DocumentVisualizer:
    def __init__(self) -> None:
        self.console = Console()
        self.colors = ["turquoise2",
                       "green1",
                       "spring_green2",
                       "spring_green1",
                       "medium_spring_green",
                       "cyan2"]

    def print_items(self, items):
        tree = Tree('Items')
        for idx, item in enumerate(items):
            tree_item = tree.add(str(idx))
            for i, kv_tuple in enumerate(item.items()):
                key = kv_tuple[0]
                val = str(kv_tuple[1])
                color = '[' + self.colors[i % len(self.colors)-1] + ']'
                tree_item.add(color+key+': ' + val)
        self.console.print(tree)
