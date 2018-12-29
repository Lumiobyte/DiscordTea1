import json

filepath = "D:/Python Coding/Discord Bots/Discord Tea/database/ratings.json"

def add_rating(rating):
    with open(filepath, encoding='utf-8', mode='r') as f:
        ratings = json.load(f)

    ratings[str(rating)] += 1

    with open(filepath, encoding='utf-8', mode='w') as f:
        ratings = json.dump(ratings, f)


def get_average():
    with open(filepath, encoding='utf-8', mode='r') as f:
        ratings = json.load(f)
        total = 0
        counter = 0

        for i in range(1, 6):
            for x in range(0, ratings[str(i)]):
                total += i
                counter += 1

    average = total / counter
    return average