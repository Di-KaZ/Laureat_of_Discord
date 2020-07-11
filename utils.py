def format_tab(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return table

def numerate_categories(categories):
    num_cat = []
    for i, categorie in enumerate(categories):
        num_cat.append((i, categorie))
    return num_cat