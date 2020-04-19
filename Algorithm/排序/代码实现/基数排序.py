def radix_sort(list_in :list):
    """基数排序
    """
    l = len(list_in)
    buckets = [0] * l
    
    m_bit = max_bit(list_in)
    for i in range(1, m_bit + 1):

        m1 = 10 ** i
        m2 = 10 ** (i-1)
        count = [0] * 10
        for v in list_in:
            bit_value = int(v % m1 / m2)
            count[bit_value] += 1
        
        # 计算不同数值的截止offset
        for j in range(1,10):
            count[j] += count[j-1]
        
        # 这里之所以取反，是因为count存放的位置是反向的
        for k in range(l-1, -1, -1):
            v = list_in[k]
            bit_value = int(v % m1 / m2)
            buckets[count[bit_value] - 1] = v
            count[bit_value] -= 1

        list_in, buckets = buckets, list_in
    return list_in


def max_bit(list_in):
    """计算list_in中最大数值对应的位数
    """
    max_value = max(list_in)
    i = 1
    v = max_value / 10
    while v > 1:
        v = v / 10
        i += 1
        
    return i

test = [1,3,8,5,3,4,3]
test = radix_sort(test)
print(test)


test = [1,8,34,567,23,1,43,999,67]
test = radix_sort(test)
print(test)