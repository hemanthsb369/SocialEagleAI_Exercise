# multiplication_table.py

# Get user input
try:
    num = int(input("Enter an integer to generate its multiplication table: "))
    
    print(f"\nMultiplication Table for {num}:\n")
    for i in range(1, 11):
        print(f"{num} x {i} = {num * i}")
except ValueError:
    print("Please enter a valid integer.")