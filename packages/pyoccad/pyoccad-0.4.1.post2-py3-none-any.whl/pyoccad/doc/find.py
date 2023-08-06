from pyoccad.doc import get


def label_by_name(root_label, name):
    for i in range(1, root_label.NbChildren() + 1):
        ch = root_label.FindChild(i, False)
        if name == get.label_name(ch):
            return ch


def all_label_by_name(root_label, name):
    found_labels = []
    for i in range(1, root_label.NbChildren() + 1):
        ch = root_label.FindChild(i, False)
        if name == get.label_name(ch):
            found_labels.append(ch)
    return found_labels
