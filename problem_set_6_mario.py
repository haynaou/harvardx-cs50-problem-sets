from cs50 import get_int

def pyramid():
    '''Function that gets user input height to build a pyramid'''
    
    height = 0
    while height <= 0 or height > 8:
        height = get_int("Enter a positive integer between 1 and 8: ")
        
    for row in range(height):
        # Print spaces
        print(" " * (height - row -1), end ="")
        # Print Hashes
        print("#" * (row + 1))
    
pyramid()
