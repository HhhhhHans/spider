import json

with open('movie.json', 'r', encoding='utf-8') as file:
    p = 1
    data_index = 0
    data = json.load(file)
    for i in range(25):
        file = open("data\\out" + str(i) + ".json", 'w', encoding='utf-8')
        file.write('[')
        data_index = i * 10
        movie = data[data_index]
        line = json.dumps(dict(movie), ensure_ascii=False)  # 将 item 转换为 JSON 格式字符串
        file.write(line)
        for data_index in range(i * 10 + 1, i * 10 + 10):
            file.write(',')
            movie = data[data_index]
            line = json.dumps(dict(movie), ensure_ascii=False)  # 将 item 转换为 JSON 格式字符串
            file.write(line)
        file.write(']')
        file.close()
