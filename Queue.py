# Author : Maximilien Schmitt-Laurin
# Date : 31 octobre 2019

class Replay:

	def __init__(self):
		self.first = None
		self.current = None
		self.last = None

	def enqueue(self, board_state):

		if self.first is None:
			self.first = self.last = Node(board_state, None, None)

		else:
			self.last.next = Node(board_state, self.last, None)
			self.last = self.last.next

	def start_replay(self):
		self.current = self.first

	def back(self):

		prev = self.current.prev
		self.current = prev
		return prev

	def next(self):

		next = self.current.next
		self.current = next
		return next

class Node:

	def __init__(self, data, prev, next):
		self.data = data
		self.prev = prev
		self.next = next