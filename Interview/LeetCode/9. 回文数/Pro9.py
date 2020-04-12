class Solution:
    def isPalindrome(self, x: int) -> bool:
        """字符串解法
        """
        
        x_str = str(x)
        l = len(x_str)
        
        i,j = 0,l-1
        
        while i < l and j > 0 and i < j:
            if x_str[i] != x_str[j]:
                return False
            i += 1
            j -= 1
            
        return True
    
    def isPalindromeByInt(self, x: int) -> bool:
        """非字符串方法
        """
        
        if x < 0:
            return False
        
        x_copy = x
        y = 0
        
        while x > 0:
            remainder = x % 10
            x = int(x/10)
            y = y*10 + remainder
            
        if y == x_copy:
            return True
        else:
            return False
    
s = Solution()
print(s.isPalindrome(0))
print(s.isPalindromeByInt(0))

print(s.isPalindrome(123))
print(s.isPalindromeByInt(123))

print(s.isPalindrome(10))
print(s.isPalindromeByInt(10))

print(s.isPalindrome(12321))
print(s.isPalindromeByInt(12321))

print(s.isPalindrome(-12321))
print(s.isPalindromeByInt(-12321))