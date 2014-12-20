for i in range(0, len(col)):
    client.api.favorites.destroy.post(id=col[i]['id_str'])
    print('Removed index {}'.format(i))
