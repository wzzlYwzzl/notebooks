def edit_distance(str_i, str_j):
    len_i = len(str_i)
    len_j = len(str_j)
    
    m = [0] * ((len_i + 1) * (len_j + 1))

    for j in range(0, len_j+1):
        m[j] = j

    for i in range(0, len_i + 1):
        m[(len_j + 1) * i] = i

    for i in range(1, len_i + 1):
        for j in range(1, len_j + 1):
            if str_i[i-1] == str_j[j-1]:
                m[(len_j+1)*i + j] = m[(len_j+1)*(i-1) + j - 1]
            else:
                tmp_1 = m[(len_j+1)*(i - 1) + j] + 1
                tmp_2 = m[(len_j+1)*i + j - 1] + 1
                tmp_3 = m[(len_j+1)*(i - 1) + j - 1] + 1
                m[(len_j+1)*i + j] = min(tmp_1,tmp_2,tmp_3)

    return m[(len_i+1)*(len_j+1) - 1]

str_i = 'osailn'
str_j = 'ofailing'


edit = edit_distance(str_i, str_j)
print(edit)