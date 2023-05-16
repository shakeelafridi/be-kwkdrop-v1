def paginate(query, extract, start_index, length):
    try:
        total = query.count()
    except:
        total = len(query)

    upper_limit = min(total, start_index + length)
    iteration = 0

    items = []
    for item in query[start_index:upper_limit]:
        iteration = iteration + 1
        ext = extract(item)
        if ext is not None:
            items.append(ext)

    return {
        'recordsTotal': total,
        'data': items
    }
