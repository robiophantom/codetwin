def calculate_sum(numbers):
    """Sum all numbers in a list"""
    total = 0
    for num in numbers:
        total += num
    return total

def find_max(numbers):
    """Find the largest number in a list"""
    if len(numbers) == 0:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

x = calculate_sum([2, 4, 6, 8])
y = find_max([15, 3, 25, 5])
print(x, y)
