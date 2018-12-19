import json

filepath = "D:/Python Coding/Discord Bots/Discord Tea/database/blacklist.json"

def check(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        blacklist = json.load(f)
        if user.id in blacklist['blacklist']:
            return True
        else: 
            return False

def blacklist_add(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        blacklist = json.load(f)
        blacklist['blacklist'].append(user.id)

    with open(filepath, encoding="utf-8", mode="w") as f:
        blacklist = json.dump(blacklist, f)

def blacklist_remove(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        blacklist = json.load(f)
        blacklist['blacklist'].remove(user.id)

    with open(filepath, encoding="utf-8", mode="w") as f:
        blacklist = json.dump(blacklist, f)