
N = int(input())
nums_list = list(map(int, input().split()))

count_dict = {}

best_name = None
best_count = -1

for num in nums_list:
    count_dict[num] = count_dict.get(num, 0) + 1

for name, count in count_dict.items():
    if count > best_count:
        best_name = name
        best_count = count

print(best_name)