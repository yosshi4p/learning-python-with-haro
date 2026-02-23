"""VSCodeの拡張機能「Code Runner」を使用して、Pythonコードを実行するための簡単な電卓プログラムです。"""
def add(x, y):
    """2つの数値を加算する関数"""
    return x + y
def subtract(x, y):
    """2つの数値を減算する関数"""
    return x - y
def multiply(x, y):
    """2つの数値を乗算する関数"""
    return x * y
def divide(x, y):
    """2つの数値を除算する関数"""
    if y == 0:
        return "Error: Division by zero is not allowed."
    return x / y
def main():
    """ユーザーからの入力を受け取り、選択された演算を実行するメイン関数"""
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    choice = input("Enter choice (1/2/3/4): ")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    if choice == '1':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == '2':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice == '3':
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice == '4':
        print(f"{num1} / {num2} = {divide(num1, num2)}")
    else:
        print("Invalid input")
if __name__ == "__main__":    main()
