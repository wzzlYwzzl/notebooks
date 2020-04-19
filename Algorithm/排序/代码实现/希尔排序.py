def shell_sort(in_list):
    """这种写法是基于交换的
    """
    
    l = len(in_list)
    group = int(l/2)
    
    while group > 0:
        for i in range(group, l):
            j = i
            k = j - group
            while k >= 0 and in_list[k] > in_list[j]:
                # 这个位置使用了交换数据的代码
                in_list[k],in_list[j] = in_list[j],in_list[k]
                j = k
                k = j - group
        group = int(group/2)
        
    return in_list


def shell_sort_shift(in_list):
    """基于移动的排序
    """
    l = len(in_list)
    group = int(l/2)
    
    while group > 0:
        for i in range(group, l):
            j = i
            k = j - group
            tmp = in_list[j]
            while k >= 0 and in_list[k] >= in_list[j]:
                # 这个位置使用了移动数据的代码
                in_list[j] = in_list[k]
                j = k
                k = j - group
            in_list[j] = tmp
        group = int(group/2)
        
    return in_list

in_list = [1,7,6,9]
out_list = shell_sort(in_list)
print(out_list)

in_list = [1,7,6,9,11,4,13,15,18,5,4,3,11,17,19,21]
out_list = shell_sort(in_list)
print(out_list)

in_list = [1,7,6,9]
out_list = shell_sort_shift(in_list)
print(out_list)

in_list = [1,7,6,9,11,4,13,15,18,5,4,3,11,17,19,21]
out_list = shell_sort_shift(in_list)
print(out_list)