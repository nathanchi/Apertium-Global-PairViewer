"""
Python script used to filter out the pairs in pairs.json.txt that do not contain
languages with coordinates in the tsv file
"""

import json


def filterPairs(filename, languages, altCodes):
    pairFile = open(filename, "r")
    filtered = []
    for line in pairFile:
        line = line.strip().split()
        lang1 = line[3][1:4]
        lang2 = line[1][1:4]
        if (
            lang1 in languages or (
                lang1 in altCodes and altCodes[lang1] in languages
                )
            ) and (
            lang2 in languages or (
                lang2 in altCodes and altCodes[lang2] in languages
                )
            ):
            # Getting rid of last comma
            line[-1] = line[-1][:-1]
            joined = " ".join(line)
            filtered.append(joined)

    pairFile.close()
    return filtered


def getLanguagesWithCoords(filename):
    langFile = open(filename, "r")
    langDict = {}
    for line in langFile:
        line = line.strip().split(",")
        lat, lon = float(line[1]), float(line[2])
        langDict[line[0]] = [lon, lat]
    langFile.close()
    return langDict


def getAlternateCodes(filename):
    codeFile = open(filename, 'r')
    codeStr = codeFile.read()
    codeFile.close()
    return json.loads(codeStr)

if __name__ == "__main__":
    langDict = getLanguagesWithCoords("apertium-languages.tsv")
    altCodes = getAlternateCodes('codes.json')
    filtered = filterPairs("pairs.json.txt", langDict, altCodes)
    apertiumFile = open("apertiumPairs.json", "w")

    apertiumFile.write("{\n")
    apertiumFile.write('"type": "FeatureCollection",\n')
    apertiumFile.write('"pairs": [\n')
    for line in filtered[:-1]:
        apertiumFile.write("\t"+line+"\n")
        apertiumFile.write(",\n")

    apertiumFile.write("\t"+filtered[-1]+"\n")

    apertiumFile.write("]\n")
    apertiumFile.write("}")

    apertiumFile.close()

    apertiumFile2 = open("apertiumPoints.json", "w")
    apertiumFile2.write("{\n")
    apertiumFile2.write('"type": "FeatureCollection",\n')

    # Writing point coordinates
    apertiumFile2.write('"point_data": [\n')
    langArr = []
    for code in sorted(langDict.keys()):
        langArr.append([code, langDict[code]])

    for lang in langArr[:-1]:
        string = '{"type": "Feature", "tag": "' + lang[0] + '", ' + '"geometry": { "type": "Point", ' + '"coordinates": ' + str(lang[1]) + "} }\n"
        apertiumFile2.write("\t"+string)
        apertiumFile2.write(",\n")

    string = '{"type": "Feature", "tag": "' + langArr[-1][0] + '", ' + '"geometry": { "type": "Point", ' + '"coordinates": ' + str(langArr[-1][1]) + "} }\n"
    apertiumFile2.write("\t"+string)

    apertiumFile2.write("]\n")
    apertiumFile2.write("}")

    apertiumFile2.close()
