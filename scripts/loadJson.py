import json
import os
import re

from bs4 import BeautifulSoup
from bs4.element import NavigableString

# All non-ascii chars: îźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ
# ÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉ

directorPattern = re.compile(
    r"((((St\.|Dr\.) )?(([A-ZÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉØ][a-zA-ZîźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ'\-]+|([A-ZÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉ]\.){1,3}|((and|of)( the| his)?)|(&)|(\"[a-zA-Z0-9îźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ'\- .]+\")) )*((de(l| la| los|lla|s)?|v(o|a)n( de(r|n)?)?|le|d(a|u|os|i)|the|af) )?(([A-ZÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉØÖ0-9]|d')[a-zA-ZîźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ'\-]+|[A-Z]), )|(J|S)r\., )*((((St\.|Dr\.) )?(([A-ZÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉØ][a-zA-ZîźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ'\-]+|([A-ZÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉ]\.){1,3}|((and|of)( the| his)?)|(&)|(\"[a-zA-Z0-9îźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ'\- .]+\")) )*((de(l| la| los|lla|s)?|v(o|a)n( de(r|n)?)?|le|d(a|u|os|i)|the|af) )?(([A-ZÊŽÈÑÀÕÓŚĐŠÅÜÁÔËÄÉØÖ0-9]|d')[a-zA-ZîźÊûêŽíÈõãÑÀøÕèňȧÓřäïØìéôàŚĐęñëŠçÅłπýßōÜćòšÁÔËâú×ŝåÄčÉá¢æžóöüÖ'\-]+|[A-Z])\. )|(J|S)r\. )"
)

# regex to check that date-country strings are of the form 2020-British-French
# dateCountryPattern = re.compile(r"(\d{4})(-[A-Z][a-zA-Z.]+)*")

# check that string ends in Jr. or Sr. (with space at end)
endJrPattern = re.compile(r"(J|S)r. $")

# match a space and a capital letter, for names like D. B. Cooper
spaceCapPattern = re.compile(r"( |^)[A-Z]$")

# find ; narrated by Person and the line
narratedPattern = re.compile(
    r"((; )((((opening )?narrat(ed|ion)|cameo|introduced) by|(uncredited |singing )?voice(s)? of|guest(s)?( stars| appearances by)?) [A-Z]))|(, voice(s)? of [A-Z])"
)

HALF_STAR_CODE = "PAUL_HALF_STAR"

STARS_DICT = {
    "../image/onestar.jpg": 1,
    "../image/twostar.jpg": 2,
    "../image/threestar.jpg": 3,
    "../image/fourstar.jpg": 4,
}

TOTAL = 0


def removeParentheses(wholeStr, occurrenceNum):
    """Removes everything inside parentheses present before the occurrenceNum-th period
    in wholeStr
    """
    dotCount = 0
    dotInd = 0
    insideParens = False
    for index, char in enumerate(wholeStr):
        if char == "(":
            insideParens = True
        elif char == ")":
            insideParens = False
        # don't count periods if they are inside parentheses
        elif char == "." and not insideParens:
            if index < 2:
                prev2 = "NO"
            else:
                prev2 = wholeStr[index - 2 : index]

            # only count periods if they aren't in Jr., D., etc.
            if prev2 not in ["Jr", "Sr", "Dr", "St"] and not spaceCapPattern.search(
                wholeStr[:index]
            ):
                dotCount += 1
                if dotCount == occurrenceNum:
                    dotInd = index + 1
                    break

    activeStr = wholeStr[:dotInd].replace(" (", "(")
    restStr = wholeStr[dotInd:]
    noParensStr = ""
    insideParens = False
    for char in activeStr:
        if char == "(":
            insideParens = True

        if not insideParens:
            noParensStr += char

        if char == ")":
            insideParens = False

    return noParensStr + restStr


def splitNames(nameStr):
    """split comma separated list of names into python list while accounting for Jr.s,
    etc.

    :nameStr: TODO
    :returns: TODO

    """
    if endJrPattern.search(nameStr):
        nameStr = nameStr.strip()
    else:
        nameStr = nameStr.strip(". ")

    # split string into each person's name
    nameList = []
    for name in nameStr.split(", "):
        if name not in ["Jr.", "Sr."]:
            nameList.append(name)
        else:
            nameList[-1] = f"{nameList[-1]}, {name}"

    return nameList


def parseDirectors(postRatingStr, movieObject):
    """TODO: Docstring for parseDirectors.

    :postRatingStr: TODO
    :movieObject: this is passed in as a reference variable! This function alters it
    directly
    :returns: rest of string not including directors if directors were successfully
    parsed, False otherwise

    """
    # acceptable director starts: D:, D., Compiled by
    # (make sure to strip whitespace after them too)
    goodTitle = False
    for start in ["D:", "D.", "Compiled by"]:
        if postRatingStr.startswith(start):
            postRatingStr = postRatingStr.removeprefix(start).strip()
            goodTitle = True
            break

    # delete all parentheses before second period (since one after directors, one after
    # actors)
    postRatingStr = removeParentheses(postRatingStr, 2)

    if goodTitle:
        # .match only matches at the very beginning of the string, so this already
        # checks that postRatingStr.startswith(thematch)
        directors = directorPattern.match(postRatingStr)
        try:
            # get just string of directors
            lastInd = directors.span()[1]
            directorStr = postRatingStr[:lastInd]
            restStr = postRatingStr[lastInd:]

            movieObject["directors"] = splitNames(directorStr)
        # if director pattern not found in postRatingStr
        except AttributeError:
            # indicate that directors weren't found, so I shouldn't parse rest of
            # movie
            movieObject["directors"] = ["NO_DIRECTORS_FOUND"]
            movieObject["actors"] = []
            movieObject["review"] = postRatingStr
            return False
    elif postRatingStr.startswith("No director credited. "):
        movieObject["directors"] = []
        restStr = postRatingStr.removeprefix("No director credited. ")
    else:
        # dummy JSON object with searchable string in it to let me go through
        # these manually later on
        movieObject["directors"] = ["NO_DIRECTORS_FOUND"]
        movieObject["actors"] = []
        movieObject["review"] = postRatingStr
        return False

    return restStr


def parseActorsReview(postDirStr, movieObject):
    """TODO: Docstring for parseActorsReview.

    :postDirStr: TODO
    :movieObject: this is passed in as a reference variable! This function alters it
    directly
    :returns: TODO

    """
    actorReviewStr = removeParentheses(postDirStr, 1)

    # delete first occurrence of "; narrated by X", etc.
    try:
        narStart, narEnd = narratedPattern.search(actorReviewStr).span()
        actorReviewStr = actorReviewStr[:narStart] + ", " + actorReviewStr[narEnd - 1 :]
    except AttributeError:
        pass

    actors = directorPattern.match(actorReviewStr)

    if actors:
        lastInd = actors.span()[1]
        actorStr = actorReviewStr[:lastInd]
        restStr = actorReviewStr[lastInd:]
        movieObject["actors"] = splitNames(actorStr)
        movieObject["review"] = restStr
    # checks if first 4 words are title case (so like 2 actor names), which means
    # that a probably legit parse failed (like actors are actually listed)
    elif all([a[0].isupper() for a in actorReviewStr.split()[:4]]):
        movieObject["actors"] = ["NO_ACTORS_FOUND"]
        movieObject["review"] = actorReviewStr
    else:
        # this basically means that actors weren't listed since the
        # previous elif statement checks that the first four words are
        # title case
        movieObject["actors"] = []
        movieObject["review"] = actorReviewStr


def jsonifyMovie(movieTag):
    """TODO: Docstring for jsonifyMovie.

    :movieTag: TODO
    :returns: TODO

    """
    movieDict = {}
    tagText = movieTag.get_text()
    strongList = movieTag.find_all("strong", recursive=False)

    if "SEE" not in tagText:
        # all the movies with no SEE and < 2 strong tags are useless (shows, usually)
        if len(strongList) >= 2:
            # this is where you want to add movies
            movieDict["title"] = strongList[0].get_text().strip()
            # should parse this more to separate color info from length
            runtimeTag = strongList[1]
            movieDict["runtime"] = runtimeTag.get_text().strip()
            dateStr = strongList[0].next_sibling.strip("() ")
            dateCountries = dateStr.split("-")
            movieDict["date"] = dateCountries.pop(0)
            movieDict["countries"] = dateCountries

            oneStars = movieTag.find_all("img", src="image/star.png")
            if len(oneStars):
                movieDict["rating"] = len(oneStars) + int(HALF_STAR_CODE in tagText) / 2
                paragraph = oneStars[-1].next_sibling
            else:
                starsTag = movieTag.find("img", class_="star")
                try:
                    movieDict["rating"] = (
                        STARS_DICT[starsTag["src"]] + int(HALF_STAR_CODE in tagText) / 2
                    )
                    paragraph = starsTag.parent.next_sibling
                except TypeError:
                    if "BOMB" in tagText:
                        paragraph = runtimeTag.next_sibling
                        movieDict["rating"] = 1.0
                    else:
                        print("\nShould set a breakpoint here, rating not found\n")

            # make paragraphStr all the text in the <p> tag after the rating
            paragraphStr = ""
            while True:
                # break if no more next_siblings (end of tag reached)
                if paragraph is None:
                    break
                elif isinstance(paragraph, NavigableString):
                    paragraphStr += str(paragraph)
                elif paragraph.name in ["em", "strong"]:
                    paragraphStr += paragraph.get_text().strip()

                paragraph = paragraph.next_sibling

            # remove trailing rating stuff
            paragraphStr = (
                paragraphStr.strip()
                .removeprefix(HALF_STAR_CODE)
                .removeprefix("BOMB")
                .strip()
            )

            # parse out directors and return string starting with actors list
            actorReviewStr = parseDirectors(paragraphStr, movieDict)

            # only try to parse actors if directors were successfully found
            if actorReviewStr:
                actorReviewStr = (
                    actorReviewStr.removeprefix("Voices of ")
                    .removeprefix("Narrated by ")
                    .replace(", many others.", ".", 1)
                    .replace(", others.", ".", 1)
                )
                # this adds the actors and review keys to the JSON object
                parseActorsReview(actorReviewStr, movieDict)
    else:
        # this is for movies that are "SEE" references

        # not sure if this is the best solution but leaving it for now
        movieDict["rating"] = "SEE_ENTRY"
        # title is the title that you would look up in alphabetical order
        movieDict["title"] = strongList[0].get_text().strip()
        # review is name of movie that the entry refers to (the part after the SEE:)
        try:
            movieDict["review"] = strongList[1].get_text().strip()
        except IndexError:
            movieDict["review"] = (
                movieTag.find("span", class_="BOLD-ITAL").get_text().strip()
            )

    return movieDict


def extractJson(filePath):
    """TODO: Docstring for extractJson.

    :filePath: TODO
    :returns: TODO

    """
    with open(filePath) as f:
        fCont = f.read()

    soupObj = BeautifulSoup(fCont, "lxml")
    moviesDiv = soupObj.select_one("html > body > div")
    allMovies = moviesDiv.find_all("p", recursive=False)

    movieObjs = []

    for movieTag in allMovies:
        movieObj = jsonifyMovie(movieTag)
        # only add non-empty dictionaries to the list
        if movieObj:
            movieObjs.append(movieObj)

    return movieObjs


if __name__ == "__main__":
    dirPaths = ["../classicGuide/xhtml/", "../2015Guide/xhtml/"]
    jsonFile = "../allMovies.json"
    totalMovies = 0
    bigList = []

    for dirPath in dirPaths:
        # loop through each non-dotfile in each directory
        for fpath in os.listdir(dirPath):
            if not fpath.startswith("."):
                basePath = dirPath[: dirPath.rindex("/") + 1]
                listFromFile = extractJson(basePath + fpath)
                totalMovies += len(listFromFile)
                bigList.extend(listFromFile)

    with open(jsonFile, "w") as f:
        json.dump(bigList, f, indent=4, ensure_ascii=False)

    print(f"{totalMovies} movies written to {jsonFile}.")
