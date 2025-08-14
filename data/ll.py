
# Not used directly
class Node:
    def __init__(self, master, data):
        self.master = master
        self.data = data
        self.next = None
    
    @property
    def current_index(self) -> int:
        position:int = 0
        current_node = self.master.head
        while current_node != self:
            position += 1
            current_node = current_node.next
        return position
    
    def removeSelf(self):
        self.master.remove_at_index(self.current_index)


class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtBegin(self, data):
        new_node = Node(self, data)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    def insertAtIndex(self, data, index):
        if (index == 0 or self.head is None):
            self.insertAtBegin(data)
            return

        position = 0
        current_node = self.head
        while (position+1 != index and current_node is not None):
            position = position+1
            current_node = current_node.next

        if current_node is not None:
            new_node = Node(self, data)
            new_node.next = current_node.next
            current_node.next = new_node
        else:
            raise IndexError(f"Index is not present, length of linked list is {self.sizeOfLL()}")


    def inserAtEnd(self, data):
        new_node = Node(self, data)
        if self.head is None:
            self.head = new_node
            return

        current_node = self.head
        while(current_node.next):
            current_node = current_node.next

        current_node.next = new_node

    # Update node of a linked list
    # at given position
    def updateNode(self, val, index):
        current_node = self.head
        position = 0
        if position == index:
            current_node.data = val
        else:
            while(current_node is not None and position != index):
                position += 1
                current_node = current_node.next

            if current_node is not None:
                current_node.data = val
            else:
                raise IndexError(f"Index is not present, length of linked list is {self.sizeOfLL()}")


    def remove_first_node(self):
        if(self.head is None):
            return
        
        self.head = self.head.next

    def remove_last_node(self):
        if self.head is None:
            return

        current_node = self.head
        while (current_node.next is not None and current_node.next.next is not None):
            current_node = current_node.next

        curr_node.next = None


    # Method to remove at given index
    def remove_at_index(self, index):
        if self.head is None:
            return

        current_node = self.head
        position = 0
        
        if index == 0:
            self.remove_first_node()
        else:
            # it goes until position equals index-1. Last time it functions, when it smaller than index-1 but then we add 1 to it, which becomes equal to index-1.
            while current_node is not None and position < index - 1:
                position += 1
                current_node = current_node.next
            
            if current_node is None or current_node.next is None:
                raise IndexError(f"Index is not present, length of linked list is {self.sizeOfLL()}")
            else:
                current_node.next = current_node.next.next

    def remove_node(self, data):
        current_node = self.head

        # Check if the head node contains the specified data
        if current_node.data == data:
            self.remove_first_node()
            return

        while current_node is not None and current_node.next.data != data:
            current_node = current_node.next

        if current_node is None:
            return
        else:
            current_node.next = current_node.next.next

    # return all linked lists items
    def returnLL(self) -> list:
        to_return: list = []
        current_node = self.head
        while(current_node):
            to_return.append(current_node)
            current_node = current_node.next
        return to_return

    def sizeOfLL(self) -> int:
        size = 0
        if(self.head):
            current_node = self.head
            while(current_node):
                size = size+1
                current_node = current_node.next
            return size
        else:
            return 0

