import sys

# Access arguments
print("Script Name:", sys.argv[0])
if len(sys.argv) > 1:
    print("Arguments:", sys.argv[1:])
    print("Arg1[1]:", sys.argv[1])
else:
    print("No arguments provided.")
