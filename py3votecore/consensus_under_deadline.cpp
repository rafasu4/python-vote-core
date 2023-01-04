#include <vector>
#include <map>
#include <algorithm>
#include <string>

using namespace std;

map<string, int> votesCalculate(map<int, string> ballots)
{
    map<string, int> ans;
    for_each(ballots.begin(), ballots.end(), [&](const auto p)
             { ans[p.second]++; });
    return ans;
}

vector<string> possibleWinners(const map<int, string> currentVotes, const int remainingRounds, const int unanimously)
{
    map<string, int> currentBallot = votesCalculate(currentVotes);
    vector<string> ans;
    for_each(currentBallot.begin(), currentBallot.end(), [&](const auto p)
             {
        if(p.second + remainingRounds + 1 >= unanimously){
            ans.push_back(p.first);
        } });
    return ans;
}