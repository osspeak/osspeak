import heapq

class MaxHeapObj:

    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val

    def __str__(self):
        return str(self.val)

class MinHeap:

    def __init__(self):
        self._h = []

    def push(self, x):
        heapq.heappush(self._h, x)

    def pop(self):
        return heapq.heappop(self._h)

    def top(self):
        return self._h[0]

    def __getitem__(self, i):
        return self._h[i]

    def __len__(self):
        return len(self._h)

class MaxHeap(MinHeap):

    def push(self, x):
        super().push(MaxHeapObj(x))

    def pop(self):
        return super().pop().val

    def __getitem__(self, i):
        return self._h[i].val

# Example usage:

# minh = MinHeap()
# maxh = MaxHeap()
# # add some values
# minh.heappush(12)
# maxh.heappush(12)
# minh.heappush(4)
# maxh.heappush(4)
# # fetch "top" values
# print(minh[0],maxh[0]) # "4 12"
# # fetch and remove "top" values
# print(minh.heappop(),maxh.heappop()) # "4 12"