import os


def in_path(parent: str, child: str) -> bool:
    if parent == child:
        return False
    head, tail = os.path.split(child)
    if not tail:
        return False
    if head == parent:
        return True
    return in_path(parent, head)
