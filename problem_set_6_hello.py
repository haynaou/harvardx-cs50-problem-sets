from cs50 import get_string

def print_hello():
    
    ''' Function that takes username and prints a greeting '''
    user_name = get_string("What's your name?:\n")
    print(f"hello, {user_name}")
        
    
print_hello()
    
