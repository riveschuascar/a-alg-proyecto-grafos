from collections import defaultdict

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]

        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]

        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
            self.size[root_a] += self.size[root_b]

    def component_sizes(self):
        roots = defaultdict(int)

        for i in range(len(self.parent)):
            root = self.find(i)
            roots[root] += 1

        return roots