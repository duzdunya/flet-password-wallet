import unittest
from data.ll import LinkedList

class TestLinkedList(unittest.TestCase):
    
    def setUp(self):
        self.ll = LinkedList()
        self.ll.insertAtBegin("TextInput")
        self.ll.insertAtBegin("Button")

        self.ll.insertAtBegin("TextInput2")
        self.ll.insertAtBegin("Button2")

        self.ll.insertAtBegin("TextInput3")
        self.ll.insertAtBegin("Button3")

    def testLinkedList(self):
        # check head
        self.assertIs(self.ll.head.data, "Button3")

        # check sizeOfLL function
        self.assertEqual(self.ll.sizeOfLL(), 6)
        
        # check returnLL function
        self.assertEqual(len(self.ll.returnLL()), 6)

        # check remove function
        self.ll.remove_at_index(1)
        self.assertIs(self.ll.returnLL()[1].data, "Button2")

        # check insert function
        self.ll.inserAtEnd("Delete Button")
        self.assertIs(self.ll.returnLL()[-1].data, "Delete Button")


    def testNode(self):
        # check current index
        fourth = self.ll.returnLL()[4]
        self.assertEqual(fourth.current_index, 4) 

        # check removeself function
        fourth.removeSelf()
        self.assertIsNot(self.ll.returnLL()[4], fourth)

    def testIndexAndPrint(self):
        self.ll.inserAtEnd("Delete Button")
        ll = self.ll.returnLL()
        self.assertIsInstance(ll, list)
        print(f"\n{30*'*'}\nList is this:\n{ll}\n{30*'*'}\nElements are:")
        for index,x in enumerate(ll):
            # check current index
            self.assertEqual(index, x.current_index)
            print(f"{index}: {x.data}")
        


if __name__ == "__main__":
    unittest.main()
