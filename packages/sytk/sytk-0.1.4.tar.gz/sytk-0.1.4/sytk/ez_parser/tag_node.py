from __future__ import annotations
from typing import Union


def _contain(l1: list[tuple], l2: list[tuple]) -> bool:
    if l1 is None:
        return False

    for i in l2:

        if i[1] is None:
            if i[0] not in [j[0] for j in l1]:
                return False

        elif i not in l1:
            return False

    return True


class TagNode:
    __slots__ = ('tag', 'args', 'data', 'text', 'parent', 'children', '_arg_dict')

    def __init__(
            self,
            tag: str,
            args: list[tuple[str, str]] = None,
            parent: TagNode = None,
    ):
        self.tag = tag
        self.args = args
        self.data = ''
        self.text = ''
        self.parent = parent
        self.children = []

        self._arg_dict = dict()
        if args is None:
            return
        for i in args:
            self._arg_dict[i[0]] = i[1]

    # Depth first search
    def find(self, tag: str = None, args: dict = None) -> Union[TagNode, None]:

        if tag is None and args is None:
            raise AttributeError("tag and args can't both be None!")

        # if tag is handed, pair it firstly
        if tag is not None:

            if self.tag == tag:
                if args is not None:
                    args_items = list(args.items())  # dict -> list[tuple]
                    if _contain(self.args, args_items):
                        return self
                else:
                    return self

            # leaf node
            if len(self.children) == 0:
                return None

            # recurse
            for i in self.children:
                if i.find(tag, args) is not None:
                    return i

        # only args is handed
        else:

            args_items = list(args.items())  # dict -> list[tuple]
            if _contain(self.args, args_items):
                return self

            # leaf node
            if len(self.children) == 0:
                return None

            # recurse
            for i in self.children:
                if i.find(tag, args) is not None:
                    return i

        return None

    def find_all(self, tag: str = None, args: dict = None) -> list[TagNode]:

        if tag is None and args is None:
            raise AttributeError("tag and args can't both be None!")

        res = []

        if tag is not None:

            if self.tag == tag:
                if args is not None:
                    args_items = list(args.items())  # dict -> list[tuple]
                    if _contain(self.args, args_items):
                        res.append(self)
                else:
                    res.append(self)

            # leaf node
            if len(self.children) == 0:
                return res

            # recurse
            for i in self.children:
                res += i.find_all(tag, args)

        # only args are handed
        elif args is not None:

            args_items = list(args.items())  # dict -> list[tuple]
            if _contain(self.args, args_items):
                res.append(self)

            # leaf node
            if len(self.children) == 0:
                return res

            # recurse
            for i in self.children:
                res.extend(i.find_all(tag, args))

        else:
            return [self]

        return res

    def copy(self):
        node = TagNode(self.tag, self.args, self.parent)
        node.data = self.data
        node.text = self.text
        node.children = self.children.copy()
        return node

    def __repr__(self):
        return f'<TagNode {self.tag}, {self.args}>'

    def __getitem__(self, item):
        return self._arg_dict[item]
