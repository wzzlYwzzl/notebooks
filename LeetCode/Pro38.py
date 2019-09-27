"""
报数序列是一个整数序列，按照其中的整数的顺序进行报数，得到下一个数。其前五项如下：

1.     1
2.     11
3.     21
4.     1211
5.     111221
1 被读作  "one 1"  ("一个一") , 即 11。
11 被读作 "two 1s" ("两个一"）, 即 21。
21 被读作 "one 2",  "one 1" （"一个二" ,  "一个一") , 即 1211。

给定一个正整数 n（1 ≤ n ≤ 30），输出报数序列的第 n 项。

注意：整数顺序将表示为一个字符串。

示例 1:

输入: 1
输出: "1"
示例 2:

输入: 4
输出: "1211"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/count-and-say
"""

class Solution:
    def countAndSay(self, n: int) -> str:
        i = 1
        ret = '1'
        while i < n:
            s = ret
            ret = ''
            count = 1
            j = 0
            for j in range(1,len(s)):
                if s[j] == s[j-1]:
                    count += 1
                else:
                    ret += '{}{}'.format(count, s[j-1])
                    count = 1
            ret += '{}{}'.format(count, s[j])
            i += 1
        return ret

solution = Solution()

ret = solution.countAndSay(1)
print(ret)

ret = solution.countAndSay(4)
print(ret)

ret = solution.countAndSay(5)
print(ret)

ret = solution.countAndSay(6)
'312211'
print(ret)

ret = solution.countAndSay(7)
'13112221'
print(ret)