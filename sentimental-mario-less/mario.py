while True:
    try:
        # taking user input and making sure its a integer
        height = int(input("Height: "))
        # checking if the height is within the valid range
        if 1 <= height <= 8:
            break
        else:
            print("Height must be between 1 and 8.")
    except ValueError:
        # handling non-numeric input
        print("Invalid input.")

for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i)
