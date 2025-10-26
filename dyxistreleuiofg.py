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
        # 每个节点存储12种状态的计数
        self.data = [[0] * 12 for _ in range(2 * self.size)]

        # 初始化叶子节点
        for i in range(self.n):
            state = get_state(data[i])
            self.data[self.size + i][state] = 1

        # 构建线段树
        for i in range(self.size - 1, 0, -1):
            self._combine(i)

    def _combine(self, i):
        """合并左右子节点的状态计数"""
        left = self.data[2 * i]
        right = self.data[2 * i + 1]
        for j in range(12):
            self.data[i][j] = left[j] + right[j]

    def update(self, idx, value):
        """更新指定位置的值"""
        pos = self.size + idx
        new_state = get_state(value)
        # 重置该位置的状态计数
        for j in range(12):
            self.data[pos][j] = 0
        self.data[pos][new_state] = 1
        pos //= 2

        # 向上更新父节点
        while pos:
            for j in range(12):
                self.data[pos][j] = self.data[2*pos][j] + self.data[2*pos+1][j]
            pos //= 2

    def query(self, l, r):
        """查询区间[l, r]的状态计数"""
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

# 预计算所有有效的状态对
valid_pairs = []
for s1 in range(12):
    a1 = s1 // 4
    b1 = (s1 // 2) % 2
    c1 = s1 % 2

    for s2 in range(s1, 12):
        a2 = s2 // 4
        b2 = (s2 // 2) % 2
        c2 = s2 % 2

        # 检查因子需求：3因子和≥2，5因子和≥1，11因子和≥1
        if a1 + a2 >= 2 and b1 + b2 >= 1 and c1 + c2 >= 1:
            valid_pairs.append((s1, s2))

# 读取输入数据
n, q = map(int, sys.stdin.readline().split())
arr = list(map(int, sys.stdin.readline().split()))

seg_tree = SegmentTree(arr)
results = []

# 处理每个查询
for _ in range(q):
    parts = sys.stdin.readline().split()
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

        # 只枚举预计算的有效状态对
        for s1, s2 in valid_pairs:
            if s1 == s2:
                n_s = cnt[s1]
                if n_s >= 2:
                    total_pairs += n_s * (n_s - 1) // 2
            else:
                total_pairs += cnt[s1] * cnt[s2]

        results.append(str(total_pairs))

# 输出所有结果
print("\n".join(results))
