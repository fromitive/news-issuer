def getContents():
    items = []
    with open("news.txt", "r", encoding="utf-8", errors="ignore") as f:
        while True:
            content = f.readline()
            print(content)
            if not content:
                break
            item = {"title": "", "link": ""}
            content = content.split("||")
            item = {"title": content[0], "link": content[1]}
            items.append(item)

    return items
