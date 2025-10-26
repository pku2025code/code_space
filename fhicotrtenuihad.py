import sys

def get_state(x):
    """计算数字x的状态索引（0-11）"""
    a = 2 if x % 9 == 0 else (1 if x % 3 == 0 else 0)
    b = 1 if x % 5 == 0 else 0
    c = 1 if x % 11 == 0 else 0
    return a * 4 + b * 2 + c

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.data = [[0] * 12 for _ in range(2 * self.size)]

        for i in range(self.n):
            state = get_state(data[i])
            self.data[self.size + i][state] = 1

        for i in range(self.size - 1, 0, -1):
            for j in range(12):
                self.data[i][j] = self.data[2*i][j] + self.data[2*i+1][j]

    def update(self, idx, value):
        pos = self.size + idx
        new_state = get_state(value)
        for j in range(12):
            self.data[pos][j] = 0
        self.data[pos][new_state] = 1
        pos //= 2

        while pos:
            for j in range(12):
                self.data[pos][j] = self.data[2*pos][j] + self.data[2*pos+1][j]
            pos //= 2

    def query(self, l, r):
        l += self.size
        r += self.size
        res = [0] * 12

        while l <= r:
            if l % 2 == 1:
                for j in range(12):
                    res[j] += self.data[l][j]
                l += 1
            if r % 2 == 0:
                for j in range(12):
                    res[j] += self.data[r][j]
                r -= 1
            l //= 2
            r //= 2
        return res

# 精确读取输入：根据第一行的n和q确定要读取的总行数
n, q = map(int, sys.stdin.readline().split())
arr = list(map(int, sys.stdin.readline().split()))

seg_tree = SegmentTree(arr)
results = []

# 读取并处理q条指令
for _ in range(q):
    parts = sys.stdin.readline().split()
    if not parts:
        continue

    op_type = int(parts[0])

    if op_type == 1:
        x = int(parts[1]) - 1
        y = int(parts[2])
        seg_tree.update(x, y)
    else:
        l = int(parts[1]) - 1
        r = int(parts[2]) - 1

        cnt = seg_tree.query(l, r)
        total_pairs = 0

        # 枚举所有状态对
        for s1 in range(12):
            a1 = s1 // 4
            b1 = (s1 // 2) % 2
            c1 = s1 % 2

            for s2 in range(s1, 12):
                a2 = s2 // 4
                b2 = (s2 // 2) % 2
                c2 = s2 % 2

                if a1 + a2 >= 2 and b1 + b2 >= 1 and c1 + c2 >= 1:
                    if s1 == s2:
                        n_s = cnt[s1]
                        total_pairs += n_s * (n_s - 1) // 2
                    else:
                        total_pairs += cnt[s1] * cnt[s2]

        results.append(str(total_pairs))

# 输出所有结果
print("\n".join(results))
