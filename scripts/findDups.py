import json


def findOtherThanReviewDups(movieList, experFields):
    """find movies that have the same title, date, runtime,
    and rating but something else about them is different
    """

    expToAll = []

    for obj in movieList:
        if "actors" in obj.keys():
            allFields = [
                "title",
                "date",
                "runtime",
                "rating",
                "countries",
                "directors",
                "actors",
                "review",
            ]
            reducedDict = {field: obj[field] for field in experFields}
            allDict = {field: obj[field] for field in allFields}
            expObj = json.dumps(reducedDict, ensure_ascii=False)
            allObj = json.dumps(allDict, ensure_ascii=False)

            expToAll.append((expObj, allObj))

    justExp = [ob[0] for ob in expToAll]
    counter = 0
    diffs = []

    for index, key in enumerate(justExp):
        sameKeys = []
        for newKey, newVal in expToAll:
            if key == newKey:
                sameKeys.append(newVal)
        if len(set(sameKeys)) > 1:
            diffs.append(key)
            counter += 1
        if index % 1000 == 0:
            print(f"Done {index}")

    print(f"Total {counter} diffs")
    diffs = list(set(diffs))

    return diffs


def removeDuplicates(movieList, dupFields):
    """Remove duplicates based on the fields specified in dupFields. Oh, and also
    convert those pesky years into integers

    :movieList: TODO
    :dupFields: TODO
    :returns: TODO

    """
    # TRY TO TAKE THE LONGEST REVIEW WHEN THERE IS A DUPLICATE
    # ok so remove duplicates based on title, date, runtime, rating (so 2 movies with
    # those same 4 fields but different actors or review, etc. become the same movie)
    fieldsDict = {}
    uniqueList = []
    counter = 0

    for movie in movieList:
        if movie["rating"] != "SEE_ENTRY":
            # basically make a hash representing the relevant fields of the movie so
            # that it can be used as a dictionary key
            reducedStr = "".join(str(movie[field]) for field in dupFields)

            if reducedStr not in fieldsDict:
                # assign the movie's index in uniqueList to the dictionary with the
                # movie "hash" as key
                fieldsDict[reducedStr] = counter
                movie["date"] = int(movie["date"])
                uniqueList.append(movie)
                counter += 1
            else:
                listInd = fieldsDict[reducedStr]
                # overwrite the duplicate entry if the new one has a longer review
                if len(uniqueList[listInd]["review"]) < len(movie["review"]):
                    uniqueList[listInd] = movie
        else:
            # make a hash of the entire object if it is a SEE entry and only add it to
            # uniqueList if it's not already in there (only check for full duplicates)
            reducedStr = "".join(
                str(movie[field]) for field in ["rating", "title", "review"]
            )
            if reducedStr not in fieldsDict:
                fieldsDict[reducedStr] = True
                uniqueList.append(movie)
                counter += 1

    # sort list for niceness
    return sorted(uniqueList, key=lambda movie: movie["title"])


if __name__ == "__main__":
    outputFile = "../uniqueMovies.json"
    dupFields = ["title", "date", "runtime", "rating"]

    with open("../allMovies.json") as f:
        data = json.load(f)

    newList = removeDuplicates(data, dupFields)

    with open(outputFile, "w") as f:
        json.dump(newList, f, ensure_ascii=False, indent=4)

    print(f"{len(newList)} movies written to {outputFile}.")
