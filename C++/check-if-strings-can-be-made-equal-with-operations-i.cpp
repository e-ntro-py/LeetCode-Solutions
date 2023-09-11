// Time:  O(1)
// Space: O(1)

// freq table
class Solution {
public:
    bool canBeEqual(string s1, string s2) {
        vector<vector<int>> lookup1(2, vector<int>(26)), lookup2(2, vector<int>(26));
        for (int i = 0; i < 2; ++i) {
            for (int j = i; j < size(s1); j += 2) {
                ++lookup1[i][s1[j] - 'a'];
            }
            for (int j = i; j < size(s1); j += 2) {
                ++lookup2[i][s2[j] - 'a'];
            }
        }
        return lookup1 == lookup2;
    }
};

// Time:  O(1)
// Space: O(1)
// brute force
class Solution2 {
public:
    bool canBeEqual(string s1, string s2) {
        return ((s1[0] == s2[0] && s1[2] == s2[2]) || (s1[0] == s2[2] && s1[2] == s2[0])) &&
               ((s1[1] == s2[1] && s1[3] == s2[3]) || (s1[1] == s2[3] && s1[3] == s2[1]));
    }
};
