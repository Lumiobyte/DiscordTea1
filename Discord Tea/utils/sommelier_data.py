import json

filepath = "D:/Python Coding/Discord Bots/Discord Tea/database/sommeliers.json"

def check(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        sommeliers = json.load(f)
        if user.id in sommeliers['sommeliers']:
            return True
        else: 
            return False

def sommelier_add(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        sommeliers = json.load(f)
        sommeliers['sommeliers'].append(user.id)

    with open(filepath, encoding="utf-8", mode="w") as f:
        sommeliers = json.dump(sommeliers, f)

def sommelier_remove(user):
    with open(filepath, encoding="utf-8", mode="r") as f:
        sommeliers = json.load(f)
        sommeliers['sommeliers'].remove(user.id)

    with open(filepath, encoding="utf-8", mode="w") as f:
        sommeliers = json.dump(sommeliers, f)