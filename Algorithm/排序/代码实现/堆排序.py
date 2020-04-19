def heap_sort(list_in):
    """基于大顶堆的排序
    """
    l = len(list_in)
    from_index = int(l/2 - 1)
    for i in range(from_index, -1, -1):
        adjust_heap(list_in, i, l)
        
    for i in range(l - 1, -1, -1):
        list_in[0],list_in[i] = list_in[i],list_in[0]
        adjust_heap(list_in, 0, i)


def adjust_heap(list_in, i, length):
    """调整堆过程，i是要调整的堆顶点的索引；
    length指的是list_in的长度。
    """
    left = 2*i + 1
    max_index = i
    while left < length:
        if list_in[left] > list_in[i]:
            max_index = left
        
        if left + 1 < length and list_in[left+1] > list_in[max_index]:
            max_index = left + 1
        
        if max_index == i:
            break
        else:
            list_in[i],list_in[max_index] = list_in[max_index],list_in[i]
            i = max_index
            left = 2*i + 1
    

test = [3,6,2,6,1,8]
heap_sort(test)
print(test)

test = [3,6,8,10,11,21,2,6,1,8]
heap_sort(test)
print(test)

test = [3,6,9,8,10,16,19,14,2,6,1,8]
heap_sort(test)
print(test)