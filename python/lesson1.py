




N = int(input())
nums_list = list(map(int, input().split()))
total = 0
found = False

for i in range(N):
    total += nums_list[i]
    if total > 10:
        print(i + 1)
        found = True
        break
    
if not found:
    print(-1)
