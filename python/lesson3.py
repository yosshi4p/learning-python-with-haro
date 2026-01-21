




N = int(input()) 
nums_list = list(map(int, input().split()))
result_list = []

result_list = [num*3 for num in nums_list if num >= 0]

sorted_list = sorted(result_list)
print(sorted_list)

