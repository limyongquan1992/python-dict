import sys, string, re

# dictionary-based content analysis
# command line arguments
dictfile = sys.argv[1]
textfile = sys.argv[2]

with open(textfile) as a:
     processing_data = a.read().split('\n') # lowercase the text
text = []
for single_data in processing_data:
    if len(single_data.split("\t")) == 2 and single_data.split("\t")[1] != "":
            text.append(single_data.split("\t")[0])
print(text)

with open(dictfile) as d:
     lines = d.readlines()

dic = {}
scores = {}
totalScore = {}

current_category = "Default_0"
scores[current_category] = 0
totalScore['Default'] = 0

# inhale the dictionary
for line in lines:
    if line[0:2] == '>>':
        current_category = line[2:].strip()
        splits = current_category.split('_')
        totalScore[splits[0]] = 0
        scores[current_category] = 0
    else:
        line = line.strip()
        if len(line) > 0:
            pattern = re.compile(line, re.IGNORECASE)
            dic[pattern] = current_category

logFile = open("log.txt", "w")
outFile = open("out.txt", "w")

# examine the text
for single_data in text:
    logFile.write(single_data + "\n")
    outFile.write(single_data + "\t")
    for token in single_data.split():
        for pattern in dic.keys():
            if pattern.match( token ):
                categ = dic[pattern]
                scores[categ] = scores[categ] + 1

    for key in scores.keys():
        splits = key.split('_')
        totalScore[splits[0]] += scores[key] * int(splits[1])
        logFile.write(key + " : " + str(scores[key]) + "\n")

    logFile.write("Total score = " + str(totalScore) + "\n")
    outFile.write(str(totalScore['cultural']) + '\n')
    logFile.flush()

    for key in scores.keys():
        scores[key] = 0
        splits = key.split('_')
        totalScore[splits[0]] = 0

logFile.close()