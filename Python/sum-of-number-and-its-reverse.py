# Time:  O(2^(log10(n)/2)) = O(n^(1/(2*log2(10))))
# Space: O(log10(n))

# backtracking
class Solution(object):
    def sumOfNumberAndReverse(self, num):
        """
        :type num: int
        :rtype: bool
        """
        def backtracking(num, total):
            if num == 0:
                return True
            if total == 1:
                return False
            if num <= 18:
                return (num%2 == 0) or (num == 11 and total == 0)
            if total == 2:
                return False
            for x in (num%10, 10+num%10):
                if not (1 <= x <= 18):
                    continue
                if total:
                    base = total
                else:
                    base = 11
                    if not (x*base <= num):
                        continue
                    while x*((base-1)*10+1) <= num:
                        base = (base-1)*10+1
                if base <= num//x and backtracking((num-x*base)//10, base//100+1):
                    return True
            return False

        return backtracking(num, 0)


# Time:  O(nlogn)
# Space: O(1)
# brute force
class Solution2(object):
    def sumOfNumberAndReverse(self, num):
        """
        :type num: int
        :rtype: bool
        """
        def reverse(n):
            result = 0
            while n:
                result = result*10 + n%10
                n //= 10            
            return result

        return any(x+reverse(x) == num for x in xrange(num//2, num+1))


# Time:  O(nlogn)
# Space: O(logn)
# brute force
class Solution3(object):
    def sumOfNumberAndReverse(self, num):
        """
        :type num: int
        :rtype: bool
        """
        return any(x+int(str(x)[::-1]) == num for x in xrange(num//2, num+1))