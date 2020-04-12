class Solution:
    def reverse(self, x: int) -> int:
        x_str = str(x)
        
        int_max = 2**31 - 1;
        int_min = -2**31;
        
        if x_str[0] == '-':
            new_x_str = '-' + x_str[1:][::-1]
        else:
            new_x_str = x_str[::-1]
            
        new_x = int(new_x_str)
        
        if new_x > int_max or new_x < int_min:
            return 0
        else:
            return new_x
        
solution = Solution()

ret = solution.reverse(12345)
print(ret)

ret = solution.reverse(-654321)
print(ret)

ret = solution.reverse(12345678987654321)
print(ret)

ret = solution.reverse(-98765432123456789)
print(ret)