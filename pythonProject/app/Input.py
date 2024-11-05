import requests


def makeApiRequest():
    x = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
    text_content = x.text
    return  text_content



text_content = makeApiRequest()
MATRIX = []
rows = text_content.strip().split('\n')  # Split by newlines
for row in rows:
    number_row = [int(num) for num in row.strip().split()]
    MATRIX.append(number_row)



def getMatrix():
    return MATRIX


def printData():
    matrix = getMatrix()
    print("Height Map:")
    for row in matrix:
        for num in row:
            print(f"{num:4}", end=' ')
        print()
