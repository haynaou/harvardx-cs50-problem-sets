from cs50 import get_float

def cash():
    ''' Function that calculates the minimum number of coins required to give a user change'''
    # Get Change from user
    change = 0
    while change <= 0:
        change = get_float("Change Owed: ")
        
    # Convert to dollars to cents
    cent = round(change * 100)
    
    # Coins counter
    counter = 0
    
    while cent != 0:
        if cent >= 25:
            cent -= 25
        elif cent >= 10:
            cent -= 10
        elif cent >= 5:
            cent -= 5
        elif cent >= 1:
            cent -= 1
        else:
            break
        counter += 1
    
    # Print the total number of coins
    print(f"{counter}")

cash()
