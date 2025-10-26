import sys

def main():
    # 读取第一行，获取n和q
    first_line = sys.stdin.readline().strip()
    if not first_line:
        return
    n, q = map(int, first_line.split())

    # 读取第二行：数组的初始值
    arr_line = sys.stdin.readline().strip()
    arr = list(map(int, arr_line.split()))

    # 预处理：存储每个数字关于495因子的信息
    # 495 = 3*3*5*11，即需要至少两个3因子，一个5因子，一个11因子
    factor_info = []
    for num in arr:
        mod3 = 1 if num % 3 == 0 else 0
        mod5 = 1 if num % 5 == 0 else 0
        mod11 = 1 if num % 11 == 0 else 0
        mod9 = 1 if num % 9 == 0 else 0  # 9提供两个3因子
        mod495 = 1 if num % 495 == 0 else 0

        factor_info.append({
            'mod3': mod3, 'mod5': mod5, 'mod11': mod11,
            'mod9': mod9, 'mod495': mod495
        })

    results = []

    # 读取并处理接下来的q行指令
    for _ in range(q):
        instruction = sys.stdin.readline().strip()
        if not instruction:
            continue

        parts = instruction.split()
        op_type = int(parts[0])

        if op_type == 1:  # 更新指令: 1 x y
            x = int(parts[1]) - 1  # 转为0-indexed
            y = int(parts[2])

            # 更新数组和因子信息
            arr[x] = y
            mod3 = 1 if y % 3 == 0 else 0
            mod5 = 1 if y % 5 == 0 else 0
            mod11 = 1 if y % 11 == 0 else 0
            mod9 = 1 if y % 9 == 0 else 0
            mod495 = 1 if y % 495 == 0 else 0

            factor_info[x] = {
                'mod3': mod3, 'mod5': mod5, 'mod11': mod11,
                'mod9': mod9, 'mod495': mod495
            }

        else:  # 查询指令: 2 l r
            l = int(parts[1]) - 1  # 转为0-indexed
            r = int(parts[2]) - 1

            # 统计区间内各类数字的数量
            count_495 = 0
            count_9_5_11 = 0
            count_9_5 = 0
            count_9_11 = 0
            count_5_11 = 0
            count_9 = 0
            count_5 = 0
            count_11 = 0
            count_other = 0

            for i in range(l, r + 1):
                info = factor_info[i]

                if info['mod495']:
                    count_495 += 1
                elif info['mod9'] and info['mod5'] and info['mod11']:
                    count_9_5_11 += 1
                elif info['mod9'] and info['mod5'] and not info['mod11']:
                    count_9_5 += 1
                elif info['mod9'] and info['mod11'] and not info['mod5']:
                    count_9_11 += 1
                elif info['mod5'] and info['mod11'] and not info['mod9']:
                    count_5_11 += 1
                elif info['mod9'] and not info['mod5'] and not info['mod11']:
                    count_9 += 1
                elif info['mod5'] and not info['mod9'] and not info['mod11']:
                    count_5 += 1
                elif info['mod11'] and not info['mod9'] and not info['mod5']:
                    count_11 += 1
                else:
                    count_other += 1

            total_count = r - l + 1

            # 计算满足条件的组合数
            total = 0

            # 情况1: 至少有一个数是495的倍数
            if count_495 > 0:
                total += count_495 * (total_count - count_495)  # 495倍数与其他数的组合
                total += count_495 * (count_495 - 1) // 2  # 495倍数之间的组合

            # 情况2: 没有495倍数，但通过组合满足条件
            remaining_count = total_count - count_495

            if remaining_count >= 2:
                # 组合1: (9,5,11) 类型的数与任何数的组合
                total += count_9_5_11 * (remaining_count - count_9_5_11)
                total += count_9_5_11 * (count_9_5_11 - 1) // 2

                # 组合2: (9,5) 与 (11) 的组合
                total += count_9_5 * count_11

                # 组合3: (9,11) 与 (5) 的组合
                total += count_9_11 * count_5

                # 组合4: (5,11) 与 (9) 的组合
                total += count_5_11 * count_9

            results.append(str(total))

    # 输出所有结果
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
