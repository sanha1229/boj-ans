import sys
input = sys.stdin.readline

def segmentify(tree, index, merge, arr):
    start, end, idx = index # 리스트 시작 인덱스, 리스트 끝 인덱스, 트리 인덱스
    
    if start == end:
        tree[idx] = arr[start]
        return tree[idx]
    
    mid = (start+end)//2
    a = segmentify(tree, (start, mid, idx<<1), merge, arr)
    b = segmentify(tree, (mid+1, end, (idx<<1)+1), merge, arr)
    tree[idx] = merge(a, b)
    return tree[idx]

class MinMaxSegmentTree:
    
    def __init__(self, arr, min_value, max_value):
        self.arr = arr
        self.size = len(arr)<<2
        self.tree = [(max_value, min_value)]*(self.size) # 0번인덱스: 최소, 1번인덱스: 최대
        self.merge = lambda a,b: (min(a[0], b[0]), max(a[1], b[1]))
        self.min_value = min_value
        self.max_value = max_value
        segmentify(tree=self.tree, index=(0,(self.size>>2)-1,1), merge=self.merge, arr=self.arr)
    
    def minmax(self, L, R, index=0):
        if not index: index = (0,(self.size>>2)-1,1)
        start, end, idx = index # 리스트 시작 인덱스, 리스트 끝 인덱스, 트리 인덱스
    
        if R < start or L > end:
            return (self.max_value, self.min_value)
        elif L <= start and R >= end:
            return self.tree[idx]
        else:
            mid = (start+end)//2
            a = self.minmax(L, R, (start, mid, idx<<1))
            b = self.minmax(L, R, (mid+1, end, (idx<<1)+1))
            return self.merge(a, b)
        
n, m = map(int, input().split())

A = [0]*n
for i in range(n):
    k = int(input())
    A[i] = (k, k)
    
segtree = MinMaxSegmentTree(A, -10**9, 10**9)    

for i in range(m):
    a, b = map(int, input().split())
    print(*segtree.minmax(a-1, b-1))
