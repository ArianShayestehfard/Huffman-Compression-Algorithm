import heapq
import pickle
import os
from collections import Counter

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq
def build_tree(text):
    heap = [Node(c, f) for c, f in Counter(text).items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        l = heapq.heappop(heap)
        r = heapq.heappop(heap)
        heapq.heappush(heap, Node(freq=l.freq+r.freq, left=l, right=r))
    return heap[0]

def get_codes(root, code='', codes=None):
    if codes is None:
        codes = {}
    if root.char is not None:
        codes[root.char] = code
    else:
        get_codes(root.left, code+'0', codes)
        get_codes(root.right, code+'1', codes)
    return codes

def compress(inp, out):
    with open(inp, 'r') as f:
        text = f.read()
    root = build_tree(text)
    codes = get_codes(root)
    bits = ''.join(codes[c] for c in text)
    pad = (8 - len(bits) % 8) % 8
    bits += '0' * pad
    data = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    with open(out, 'wb') as f:
        pickle.dump((root, pad), f)
        f.write(data)
