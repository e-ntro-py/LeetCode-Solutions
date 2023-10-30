# Time:  O(nlogn)
# Space: O(n)

from sortedcontainers import SortedList


# prefix sum, sorted list, binary search, mono stack
class Solution(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """
        NEG_INF = float("-inf")

        right = [NEG_INF]*len(prices)
        sl = SortedList()
        for i in reversed(xrange(len(prices))):
            j = sl.bisect_left((-prices[i],))
            if j-1 >= 0:
                right[i] = sl[j-1][1]
            if not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((-prices[i], profits[i]))
            j = sl.bisect_left((-prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        result = NEG_INF
        sl = SortedList()
        for i in xrange(len(prices)):
            j = sl.bisect_left((prices[i],))
            if j-1 >= 0:
                result = max(result, sl[j-1][1]+profits[i]+right[i])
            if not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((prices[i], profits[i]))
            j = sl.bisect_left((prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        return result if result != NEG_INF else -1


# Time:  O(nlogn)
# Space: O(n)
from sortedcontainers import SortedList


# prefix sum, sorted list, binary search, mono stack
class Solution2(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """
        NEG_INF = float("-inf")

        left = [NEG_INF]*len(prices)
        sl = SortedList()
        for i in xrange(len(prices)):
            j = sl.bisect_left((prices[i],))
            if j-1 >= 0:
                left[i] = sl[j-1][1]
            if j < len(sl) and sl[j][0] == prices[i]:
                if not (sl[j][1] < profits[i]):
                    continue
                del sl[j]
            elif not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        right = [NEG_INF]*len(prices)
        sl = SortedList()
        for i in reversed(xrange(len(prices))):
            j = sl.bisect_left((-prices[i],))
            if j-1 >= 0:
                right[i] = sl[j-1][1]
            if j < len(sl) and -sl[j][0] == prices[i]:
                if not (sl[j][1] < profits[i]):
                    continue
                del sl[j]
            elif not (j-1 < 0 or sl[j-1][1] < profits[i]):
                continue
            sl.add((-prices[i], profits[i]))
            while j+1 < len(sl) and sl[j+1][1] <= sl[j][1]:
                del sl[j+1]
        result = max(left[i]+profits[i]+right[i] for i in xrange(len(profits)))
        return result if result != NEG_INF else -1


# Time:  O(nlogn)
# Space: O(n)
# prefix sum, segment tree
class Solution3(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """
        NEG_INF = float("-inf")
        # Range Maximum Query
        class SegmentTree(object):
            def __init__(self, N,
                         build_fn=lambda _: None,
                         query_fn=lambda x, y: max(x, y),
                         update_fn=lambda x, y: max(x, y)):
                self.tree = [None]*(2*2**((N-1).bit_length()))
                self.base = len(self.tree)//2
                self.query_fn = query_fn
                self.update_fn = update_fn
                for i in xrange(self.base, self.base+N):
                    self.tree[i] = build_fn(i-self.base)
                for i in reversed(xrange(1, self.base)):
                    self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

            def update(self, i, h):
                x = self.base+i
                self.tree[x] = self.update_fn(self.tree[x], h)
                while x > 1:
                    x //= 2
                    self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])

            def query(self, L, R):
                if L > R:
                    return None
                L += self.base
                R += self.base
                left = right = None
                while L <= R:
                    if L & 1:
                        left = self.query_fn(left, self.tree[L])
                        L += 1
                    if R & 1 == 0:
                        right = self.query_fn(self.tree[R], right)
                        R -= 1
                    L //= 2
                    R //= 2
                return self.query_fn(left, right)

        price_to_idx = {x:i for i, x in enumerate(sorted(set(prices)))}
        right = [NEG_INF]*len(prices)
        st = SegmentTree(len(price_to_idx))
        for i in reversed(xrange(len(prices))):
            right[i] = st.query(price_to_idx[prices[i]]+1, len(price_to_idx)-1)
            st.update(price_to_idx[prices[i]], profits[i])
        result = NEG_INF
        st = SegmentTree(len(price_to_idx))
        for i in xrange(len(prices)):
            left = st.query(0, price_to_idx[prices[i]]-1)
            if left is not None and right[i] is not None:
                result = max(result, left+profits[i]+right[i])
            st.update(price_to_idx[prices[i]], profits[i])
        return result if result != NEG_INF else -1


# Time:  O(nlogn)
# Space: O(n)
# prefix sum, segment tree
class Solution4(object):
    def maxProfit(self, prices, profits):
        """
        :type prices: List[int]
        :type profits: List[int]
        :rtype: int
        """
        NEG_INF = float("-inf")
        # Range Maximum Query
        class SegmentTree(object):
            def __init__(self, N,
                         build_fn=lambda _: None,
                         query_fn=lambda x, y: max(x, y),
                         update_fn=lambda x, y: max(x, y)):
                self.tree = [None]*(2*2**((N-1).bit_length()))
                self.base = len(self.tree)//2
                self.query_fn = query_fn
                self.update_fn = update_fn
                for i in xrange(self.base, self.base+N):
                    self.tree[i] = build_fn(i-self.base)
                for i in reversed(xrange(1, self.base)):
                    self.tree[i] = query_fn(self.tree[2*i], self.tree[2*i+1])

            def update(self, i, h):
                x = self.base+i
                self.tree[x] = self.update_fn(self.tree[x], h)
                while x > 1:
                    x //= 2
                    self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])

            def query(self, L, R):
                if L > R:
                    return None
                L += self.base
                R += self.base
                left = right = None
                while L <= R:
                    if L & 1:
                        left = self.query_fn(left, self.tree[L])
                        L += 1
                    if R & 1 == 0:
                        right = self.query_fn(self.tree[R], right)
                        R -= 1
                    L //= 2
                    R //= 2
                return self.query_fn(left, right)

        price_to_idx = {x:i for i, x in enumerate(sorted(set(prices)))}
        left = [NEG_INF]*len(prices)
        st = SegmentTree(len(price_to_idx))
        for i in xrange(len(prices)):
            left[i] = st.query(0, price_to_idx[prices[i]]-1)
            st.update(price_to_idx[prices[i]], profits[i])
        right = [NEG_INF]*len(prices)
        st = SegmentTree(len(price_to_idx))
        for i in reversed(xrange(len(prices))):
            right[i] = st.query(price_to_idx[prices[i]]+1, len(price_to_idx)-1)
            st.update(price_to_idx[prices[i]], profits[i])
        result = NEG_INF
        for i in xrange(len(profits)):
            if left[i] is not None and right[i] is not None:
                result = max(result, left[i]+profits[i]+right[i])
        return result if result != NEG_INF else -1