import requests


def getMatrix():

    response = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
    text_content = response.text


    matrix = []
    rows = text_content.strip().split('\n')
    for row in rows:
        number_row = [int(num) for num in row.strip().split()]
        matrix.append(number_row)

    return matrix


def printData():
    matrix = getMatrix()
    print("Height Map:")
    for row in matrix:
        for num in row:
            print(f"{num:4}", end=' ')
        print()


# Optional: for testing
if __name__ == "__main__":
    printData()