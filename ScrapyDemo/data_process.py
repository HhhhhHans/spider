import json

with open("finaldata/finalData.json", 'w', encoding='utf-8') as finalFile:
    finalFile.write('[')
    for i in range(25):
        with open("finaldata/out" + str(i) + ".json", 'r', encoding='utf-8') as file:
                data = json.load(file)
                for comment in data:
                    if len(comment['like']) != 0:
                        line = json.dumps(dict(comment), ensure_ascii=False)
                        newLine = line.replace("\\n","")
                        finalFile.write(newLine)
                        finalFile.write(',')



