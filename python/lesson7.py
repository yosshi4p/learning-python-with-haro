
N = int(input())
nums_list = list(map(int, input().split()))

mid = sum(nums_list) // N

anser = sum(abs(a - mid) for a in nums_list)
print(anser)