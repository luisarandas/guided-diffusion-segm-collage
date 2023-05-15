

# luis arandas 15-05-2023
# main executor

import argparse
from src.module1 import function1, function2

def main(string_arg, int_arg):
    print(f"The result of function1 is {function1(string_arg, string_arg)}")
    print(f"The result of function2 is {function2(int_arg, int_arg)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('string_arg', type=str, help='a string argument')
    parser.add_argument('int_arg', type=int, help='an integer argument')
    
    args = parser.parse_args()
    
    main(args.string_arg, args.int_arg)