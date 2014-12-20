col = []
while True:
    r = client.api.favorites.list.get(count=200, max_id=col[-1]['id']-1)
    if not r.data:
        break
    col = col + r.data
    print(len(col))
