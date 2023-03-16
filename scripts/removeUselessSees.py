import json

# this script removes SEE entries that just say to see the classic movie guide and that
# already have another movie in the JSON file with the same title, which means that the
# SEE entry is redundant

with open("../uniqueMovies.json") as f:
    movList = json.load(f)

notSeeTitles = [mov["title"] for mov in movList if not mov["see"]]

goodMovies = []

for mov in movList:
    if not (
        mov["see"]
        and mov["review"] == "Leonard Maltin's Classic Movie Guide"
        and mov["title"] in notSeeTitles
    ):
        goodMovies.append(mov)

print(len(movList))
print(len(goodMovies))

with open("../usefulSeesMovies.json", "w") as f:
    movList = json.dump(goodMovies, f, ensure_ascii=False, indent=4)
