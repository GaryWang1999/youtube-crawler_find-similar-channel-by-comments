with open('related_url_set.txt') as f:
    lines = f.readlines()

for url in lines:
    print(url[:len(url)-2])
