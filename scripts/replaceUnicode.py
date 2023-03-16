import os


def findNonAscii(path):
    """return dictionary of non-ascii characters present in files in path and their
    frequencies
    """
    nonUnicode = {}
    basePath = path[: path.rindex("/") + 1]
    for fname in [basePath + fi for fi in os.listdir(path) if not fi.startswith(".")]:
        with open(fname) as f:
            data = f.read()
        for char in data:
            if not char.isascii():
                if char in nonUnicode:
                    nonUnicode[char] += 1
                else:
                    nonUnicode[char] = 1

    return nonUnicode


def replaceBadSpaces(path):
    """Loop through all non-dotfiles in path and replace weird \xa0 unicode character
    with space or not, depending on if it's in a name or ellipses
    """
    basePath = path[: path.rindex("/") + 1]
    for fname in [basePath + fi for fi in os.listdir(path) if not fi.startswith(".")]:
        print(f"Converting {fname}")
        with open(fname) as f:
            lines = f.read()
        lines = lines.replace("\xa0.\xa0.\xa0.\xa0", "...")
        lines = lines.replace("\xa0.\xa0.\xa0.", "...")
        lines = lines.replace(".\xa0.\xa0.", "...")
        lines = lines.replace("\xa0", " ")
        with open(fname, "w") as f:
            f.write(lines)


if __name__ == "__main__":
    paths = ["../2015Guide/xhtml/", "../classicGuide/xhtml/"]
    print(findNonAscii(paths[0]))

    for p in paths:
        replaceBadSpaces(p)
