

###平均との差の最大値を求めるプログラム###

N = int(input())
A = list(map(int, input().split()))
mean_A = sum(A) // N
max_diff = 0

for a in A:
    diff = abs(a - mean_A)
    if diff > max_diff:
        max_diff = diff
print(max_diff)

###lesson11.py###
