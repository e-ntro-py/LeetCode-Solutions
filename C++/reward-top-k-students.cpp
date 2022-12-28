// Time:  O(pf * l + nf * l + n * l + klogk)
// Space: O(pf * l + nf * l + n)

// partial sort
class Solution {
public:
    vector<int> topStudents(vector<string>& positive_feedback, vector<string>& negative_feedback, vector<string>& report, vector<int>& student_id, int k) {
        unordered_set<string> pos(cbegin(positive_feedback), cend(positive_feedback));
        unordered_set<string> neg(cbegin(negative_feedback), cend(negative_feedback));
        vector<pair<int, int>> arr;
        for (int i = 0; i < size(report); ++i) {
            int score = 0;
            for (int j = 0, k = 0; j < size(report[i]); ++j) {
                if (j + 1 == size(report[i]) || report[i][j + 1] == ' ') {
                    const auto& w = report[i].substr(k, j - k + 1);
                    score += pos.count(w) ? 3 : neg.count(w) ? -1 : 0;
                    k = j + 2;
                }
            }
            arr.emplace_back(-score, student_id[i]);
        }
        partial_sort(begin(arr), begin(arr) + k, end(arr));
        vector<int> result;
        transform(begin(arr), begin(arr) + k, back_inserter(result), [](const auto& x) {
            return x.second;
        });
        return result;
    }
};
