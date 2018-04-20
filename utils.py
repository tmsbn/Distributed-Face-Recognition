LOG = True


def log(message):
    if LOG:
        print(message)


def is_in_range(start, end, curr):

    # (start < end and start <= curr <= end) or (curr >= start or curr <= end)
    if start < end:
        return start <= curr <= end
    else:
        return curr >= start or curr <= end


def print_online_nodes(nodes):

    for curr_id, url in nodes.items():
        log(str(curr_id) + '\t' + url)