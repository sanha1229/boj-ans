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

class MinSegmentTree:
    
    def __init__(self, arr, M):
        self.arr = arr
        self.size = len(arr)<<2
        self.tree = [M]*(self.size)
        self.merge = lambda a,b: min(a, b)
        self.max = M
        segmentify(tree=self.tree, index=(0,(self.size>>2)-1,1), merge=self.merge, arr=self.arr)
    
    def min(self, L, R, index=0):
        if not index: index = (0,(self.size>>2)-1,1)
        start, end, idx = index # 리스트 시작 인덱스, 리스트 끝 인덱스, 트리 인덱스
    
        if R < start or L > end:
            return self.max
        elif L <= start and R >= end:
            return self.tree[idx]
        else:
            mid = (start+end)//2
            a = self.min(L, R, (start, mid, idx<<1))
            b = self.min(L, R, (mid+1, end, (idx<<1)+1))
            return self.merge(a, b)

n, m = map(int, input().split())
A = [0]*n
for i in range(n):
    A[i] = int(input())

segtree = MinSegmentTree(A, 10**9)
    
for i in range(m):
    a, b = map(int, input().split())
    print(segtree.min(a-1, b-1))
