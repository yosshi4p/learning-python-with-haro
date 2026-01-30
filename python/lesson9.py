

nums_list = list(map(int, input().split()))

a = nums_list[0]
c = nums_list[1]

total_price = 0

def calc_price(a, c):
    total_price = a * 1200 + c * 700
    if a + c >= 5:
        total_price -= 500
    return total_price
    
print(calc_price(a, c))
