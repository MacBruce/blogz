# I am aware that this isn't the pythonic way but I believe in writing small composable functions
# than importing them into the program

def isEmpty(str):
    if str == "":
        return True

def lessThan(str, int):
    if len(str) < int:
        return True

def greaterThan(str, int):
    if len(str) > 20:
        return True

def isSpace(str):
    if ' ' in str:
        return True