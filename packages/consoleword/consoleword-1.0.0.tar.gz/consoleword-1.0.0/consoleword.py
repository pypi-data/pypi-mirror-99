import os

def create():
    print("Welcome!")

    text = input("Enter text: ")

    usertext = open("yourtext.txt", "w")

    usertext.write(text)
    print("View new file: \"yourtext.txt\"")