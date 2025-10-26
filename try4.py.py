t = int(input().strip())
results = []

for _ in range(t):
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    count_0 = arr.count(0)
    count_1 = n - count_0
    
    min_diff = 2  # 最大可能差值是1-0=1,所以初始设为2
    
    for x in range(max(0, k - count_0), min(k, count_1) + 1):
        y = k - x
        
        max_val = 1 if x > 0 else 0
        
        mid_pos = (k + 1) // 2
        
        if mid_pos <= y:
            mid_val = 0
        else:
            mid_val = 1
        
        diff = max_val - mid_val
        if diff < min_diff:
            min_diff = diff
    
    results.append(str(min_diff))

print("\n".join(results))
