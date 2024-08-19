

def years(start, year0, inputend):
    if start == 0:
        start = 1

    if start == 1:
        year0 += 5
        if year0 == int(inputend):
            start = 2
        if year0 > int(inputend-5):
            start = 2



    return start, year0


def years_sum(start, yeart, inputend):
    if start == 0:
        start = 1

    if start == 1:
        yeart += 1
        if yeart == int(inputend):
            start = 2

    return start, yeart
