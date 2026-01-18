"""
Task 1: Queue Abstract Classes and Implementations
This module provides an abstract Queue interface and three concrete implementations.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class Queue(ABC, Generic[T]):
    """Abstract base class for Queue implementations."""
    
    @abstractmethod
    def enqueue(self, item: T) -> None:
        """Add an item to the queue."""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[T]:
        """Remove and return an item from the queue."""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Return the number of items in the queue."""
        pass


class ArrayQueue(Queue[T]):
    """Array-based queue implementation."""
    
    def __init__(self):
        self._items = []
    
    def enqueue(self, item: T) -> None:
        self._items.append(item)
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self._items.pop(0)
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)


class Node(Generic[T]):
    """Node for linked list implementation."""
    
    def __init__(self, data: T):
        self.data = data
        self.next: Optional[Node[T]] = None


class LinkedListQueue(Queue[T]):
    """Linked list-based queue implementation."""
    
    def __init__(self):
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        new_node = Node(item)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        data = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return data
    
    def is_empty(self) -> bool:
        return self._head is None
    
    def size(self) -> int:
        return self._size


class CircularQueue(Queue[T]):
    """Circular queue implementation with fixed capacity."""
    
    def __init__(self, capacity: int = 100):
        self._capacity = capacity
        self._items = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        if self._size >= self._capacity:
            raise OverflowError("Queue is full")
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def size(self) -> int:
        return self._size


# ============== TESTS ==============
import unittest


class TestQueues(unittest.TestCase):
    """Test suite for Queue implementations."""
    
    def test_array_queue_with_integers(self):
        """Test ArrayQueue with integer values."""
        queue = ArrayQueue()
        self.assertTrue(queue.is_empty())
        self.assertEqual(queue.size(), 0)
        
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        self.assertFalse(queue.is_empty())
        self.assertEqual(queue.size(), 3)
        
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.size(), 1)
        self.assertEqual(queue.dequeue(), 3)
        
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.dequeue())
    
    def test_linked_list_queue_with_strings(self):
        """Test LinkedListQueue with string values."""
        queue = LinkedListQueue()
        self.assertTrue(queue.is_empty())
        
        queue.enqueue("first")
        queue.enqueue("second")
        queue.enqueue("third")
        
        self.assertEqual(queue.size(), 3)
        self.assertEqual(queue.dequeue(), "first")
        self.assertEqual(queue.dequeue(), "second")
        self.assertEqual(queue.dequeue(), "third")
        self.assertIsNone(queue.dequeue())
    
    def test_circular_queue_basic_operations(self):
        """Test CircularQueue basic operations."""
        queue = CircularQueue(capacity=5)
        
        for i in range(5):
            queue.enqueue(i)
        
        self.assertEqual(queue.size(), 5)
        
        # Queue is full
        with self.assertRaises(OverflowError):
            queue.enqueue(6)
        
        self.assertEqual(queue.dequeue(), 0)
        self.assertEqual(queue.dequeue(), 1)
        
        # Now we can add more
        queue.enqueue(5)
        queue.enqueue(6)
        
        self.assertEqual(queue.size(), 5)
    
    def test_queue_fifo_order(self):
        """Test that all queues maintain FIFO order."""
        queues = [ArrayQueue(), LinkedListQueue(), CircularQueue(10)]
        
        for queue in queues:
            for i in range(10):
                queue.enqueue(i)
            
            for i in range(10):
                self.assertEqual(queue.dequeue(), i)
            
            self.assertTrue(queue.is_empty())


if __name__ == '__main__':
    unittest.main()
