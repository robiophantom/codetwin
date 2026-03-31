def calculate_sum(numbers):
    """Calculate the sum of a list of numbers"""
    total = 0
    for num in numbers:
        total += num
    return total

def find_max(numbers):
    """Find the maximum value in a list"""
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

result1 = calculate_sum([1, 2, 3, 4, 5])
result2 = find_max([10, 5, 20, 3])
print(result1, result2)
