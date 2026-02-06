

N = int(input())

A = list(map(int, input().split()))

current = 1
best = 1

for a in range(N-1):
    if A[a] < A[a+1]:
        current += 1
    else:
        current = 1
    if best < current:
        best = current

print(best)
