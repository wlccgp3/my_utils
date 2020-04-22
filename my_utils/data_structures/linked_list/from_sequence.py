# Recursive Prorgam to create a Linked List from a sequence and
# print a string representation of it.


class Node:
    def __init__(self, val=None):
        self.val = val
        self.next = None

    def __repr__(self):
        """Returns a visual representation of the node and all its following nodes."""
        string_rep = ""
        temp = self
        while temp:
            string_rep += f"Node({temp.val}) --> "
            temp = temp.next
        string_rep += "<END>"
        return string_rep


def make_linked_list(elements_list):
    """Creates a Linked List from the elements of the given sequence
    (list/tuple) and returns the head of the Linked List."""

    # if elements_list is empty
    if not elements_list:
        raise Exception("The Elements List is empty")

    # Set first element as Head
    head = Node(elements_list[0])
    current = head
    # Loop through elements from position 1
    for val in elements_list[1:]:
        current.next = Node(val)
        current = current.next
    return head


if __name__ == '__main__':
    list_val = [1, 3, 5, 32, 44, 12, 43]
    print(f"List: {list_val}")
    print("Creating Linked List from List.")
    linked_list = make_linked_list(list_val)
    print("Linked List:")
    print(linked_list)
