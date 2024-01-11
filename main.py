import sys

if __name__ == "__main__":

    base_port = 8000

    numbers = []
    temp = []

    for arg in sys.argv[1:]:
        if arg == '@':
            numbers.append(temp)
            temp = []
        else:
            temp.append(int(arg))
    if temp:
        numbers.append(temp)
