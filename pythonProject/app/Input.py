import requests

# Make request
x = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')

# Parse the text content into a 2D array of numbers
text_content = x.text
rows = text_content.strip().split('\n')
data = [[int(num) for num in row.strip().split()] for row in rows]
matrix = [[int(num) for num in row.strip().split()] for row in rows]

print(matrix)

def printData():
    for row in data:
        for num in row:
            print(f"{num:4}", end=' ')
        print()

def getMatrix():
    return matrix