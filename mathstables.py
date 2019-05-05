
def multiplication_table():

    # prints the top row
    string = ''
    topRowString = ''
    for column in range(1, 11):
        topRowString += '\t' + str(column)
    print(topRowString)
    string += topRowString + '\n'


    for row in range(1, 11):
        rowString = str(row)
        for column in range(1, 11):
            rowString += '\t' + str(row * column)
        print(rowString)
        string += rowString + '\n'
    return string


multiplication_table()