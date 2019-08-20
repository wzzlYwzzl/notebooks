def kmp(str_root, pattern):
    next_list = next(pattern)

    i = 0
    j = 0

    l_i = len(str_root)
    l_j = len(pattern)
    while i < l_i and j < l_j:
        if j == -1 or str_root[i] == pattern[j]:
            j += 1
            i += 1
        else:
            j = next_list[j]
    if j == l_j:
        return i - j
    else:
        return -1


def next(pattern):
    """根据pattern构建next数组
    """
    length = len(pattern)
    output = [0] * length
    output[0] = -1

    k = -1
    j = 0

    while j < length - 1:
        if k == -1 or pattern[j] == pattern[k]:
            j += 1
            k += 1
            if pattern[j] == pattern[k]:
                output[j] = output[k]
            else:
                ouput[j] = k
        else:
            k = output[k]

    return output
