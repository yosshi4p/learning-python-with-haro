

N = int(input())
A = list(map(int, input().split()))

sorted_A = sorted(A, reverse=True)

print(sorted_A[1])
