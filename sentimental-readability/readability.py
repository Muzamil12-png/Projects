# taking user input
text = input("Text: ")

# initializing counts for input
letters = 0
words = 1  # starting at 1 because the last word won't have a space after it
sentences = 0

# analyzing the text
for char in text:
    if char.isalpha():
        letters += 1
    elif char == " ":
        words += 1
    elif char in ".!?":
        sentences += 1

# calculating the Coleman-Liau index
L = (letters / words) * 100
S = (sentences / words) * 100
index = 0.0588 * L - 0.296 * S - 15.8

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")
