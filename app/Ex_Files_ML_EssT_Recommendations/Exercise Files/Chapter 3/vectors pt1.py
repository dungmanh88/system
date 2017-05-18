ratings = [
    5,
    2,
    3,
    3,
    4,
    5,
    5,
    1,
    5,
    1,
    3,
    4
]

for i, value in enumerate(ratings):
    print("Updating rating {}".format(i))
    ratings[i] = value * 2

print(ratings)