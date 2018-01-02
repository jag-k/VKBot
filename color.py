def color(text='', *attributes, to_normal_end=True):
    """
        attributes
    0 - normal
    1 - thumbnail
    4 - underline
    5 - flashing
    7 - inverted colors
    8 - invisible

        text color
    30 - black
    31 - red
    32 - green
    33 - yellow
    34 - blue
    35 - purple
    36 - light-blue
    37 - white

        background color
    40 - black
    41 - red
    42 - green
    43 - yellow
    44 - blue
    45 - purple
    46 - light-blue
    47 - white
    """
    if not all(map(lambda x: type(x) is int, attributes)):
        raise TypeError("attribute takes only 'int' arguments")
    elif not all(map(lambda x: x in [0, 1, 4, 5, 7, 9]+list(range(30, 38))+list(range(40, 48)), attributes)):
        raise ValueError("the values ​​of 'attribute' are not in the values ​​of the table")
    return '\x1b['+';'.join(sorted(map(str, attributes)))+'m'+str(text)+('\x1b[0m' if to_normal_end else '')


if __name__ == '__main__':
    print(color('test', 1, 32))