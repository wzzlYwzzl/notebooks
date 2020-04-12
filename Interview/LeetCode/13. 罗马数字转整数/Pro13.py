class Solution:
    def romanToInt(self, s: str) -> int:
        
        unit_map = {
            'M': 1000,
            'D': 500,
            'C': 100,
            'L': 50,
            'X': 10,
            'V': 5,
            'I': 1
        }
        
        l = len(s)
        ret = unit_map[s[l-1]]
        
        i = l - 2
        while i >=0:
            v0 = unit_map[s[i]]
            v1 = unit_map[s[i+1]]
            if v1 > v0:
                ret -= v0
            else:
                ret += v0
            i -= 1
                
        return ret
    
    def romanToInt(self, s: str) -> int:
        """题解中看到的方法
        """
        d = {'I':1, 'IV':3, 'V':5, 'IX':8, 'X':10, 'XL':30, 'L':50, 'XC':80, 'C':100, 'CD':300, 'D':500, 'CM':800, 'M':1000}
        return sum(d.get(s[max(i-1, 0):i+1], d[n]) for i, n in enumerate(s))
    
s = Solution()
print(s.romanToInt("III"))

print(s.romanToInt("IV"))

print(s.romanToInt("IX"))

print(s.romanToInt("LVIII"))

print(s.romanToInt("MCMXCIV"))