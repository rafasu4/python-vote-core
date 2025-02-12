import doctest
import random
import logging
from collections import Counter
import cppyy
from cppyy.gbl import std

cppyy.include("consensus_under_deadline.cpp")


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def mdvr(voters: tuple, voters_type: tuple, alternatives: tuple, voters_preferences: list,
         default_alternative: str, remaining_rounds: int, random_selection: bool):
    '''
    Runs the algorithm 'Consensus Under Deadline' to determine the winning result.

    Returns:
        The winner alternative

    ---------------------------------TESTS---------------------------------
    Classic example:
    Since 3 different votes were chosen, we'll assume that all 3 voters will want to change their ballot (to prevent default option)
    using seed in random, voter 1 will be chosen as an example, as all voters active
    >>> v = (1, 2, 3)
    >>> v_type = (1, 1, 1)
    >>> alters = ('a', 'b', 'c')
    >>> df_alter = 'null'
    >>> v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
    >>> vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
    >>> t = 2
    >>> print(mdvr(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False))
    b

    Lazy voter example:
    >>> v = (1, 2, 3, 4, 5)
    >>> v_type = (1, 1, 1, 1, 0)
    >>> alters = ('a', 'b', 'c', 'd')
    >>> df_alter = 'null'
    >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
    >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
    >>> t = 4
    >>> print(mdvr(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False))
    b

    No consensus reached example:
    >>> v = (1, 2, 3, 4, 5)
    >>> v_type = (0, 0, 0, 0, 0)
    >>> alters = ('a', 'b', 'c', 'd')
    >>> df_alter = 'null'
    >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
    >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
    >>> t = 2
    >>> print(mdvr(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False))
    null
'''
    cud = ConsensusUnderDeadline(voters, voters_type, alternatives, voters_preferences,
                                 default_alternative, remaining_rounds, random_selection)
    return cud.deploy_algorithm()


class ConsensusUnderDeadline():
    '''
        A class representing a model for group decision making under strict deadline, based on iterative process. Each alternative must be accept
        by unanimously.
        The model was presented by Marina Bannikova, Lihi Dery, Svetlana Obraztsova, Zinovi Rabinovich, Jeffrey S. Rosenschein (2019),
        https://arxiv.org/abs/1905.07173

        Author: Raphael Suliman
    '''

    def __init__(self, voters: tuple, voters_type: tuple, alternatives: tuple, voters_preferences: list,
                 default_alternative: str, remaining_rounds: int, random_selection: bool) -> int:
        '''
            Constructor for Consensus-Under-Deadline algorithm.

            Arguments:
                voters - all of the enlisted voters
                voters_type - whether the voter is an 'active' one, or 'lazy'. 1 - active, 0 - lazy
                alternatives - all of the optional choices to vote for
                voters_preferences - the voters preferences of the alternatives in decreasing order
                default_alternative - an alternative that will be chosen upon disagreement
                remaining_rounds - a threshold for the amount if rounds left until decision should be taken
                random_selection - whether the selection of voter for changing their ballot. If False - the smallest voter's number will be selected
        '''
        logger.info('ConsensusUnderDeadline object created')
        if len(tuple(set(voters))) != len(voters):
            raise ValueError('each voter must have unique id')
        self.voters = voters
        flag = False
        flag = [True for type in voters_type if (1 < type or type < 0)]
        if flag:
            raise TypeError('voter type can only be presented with 1 or 0')
        self.voters_type = voters_type
        if len(tuple(set(alternatives))) != len(alternatives):
            raise ValueError('each alternative must have unique id')
        if len(voters) != len(voters_preferences):
            raise TypeError('length of voters and preference must be the same')
        self.alternatives = alternatives
        self.voters_preferences = voters_preferences
        self.default_alternative = default_alternative
        # initiate first ballot for each voter by their top preference
        self.voters_current_ballot = {i + 1: voters_preferences[i][0]
                                      for i in range(len(voters_preferences))}
        if remaining_rounds < 0:
            raise ValueError(f'''time can't be negative''')
        self.remaining_rounds = remaining_rounds
        self.random_selection = random_selection

    def deploy_algorithm(self):
        '''
            Runs the algorithm 'Consensus Under Deadline' to determine the winning result.

            Returns:
                The winner alternative

            ---------------------------------TESTS---------------------------------
            Classic example:
            Since 3 different votes were chosen, we'll assume that all 3 voters will want to change their ballot (to prevent default option)
            using seed in random, voter 1 will be chosen as an example, as all voters active
            >>> v = (1, 2, 3)
            >>> v_type = (1, 1, 1)
            >>> alters = ('a', 'b', 'c')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
            >>> vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
            >>> t = 2
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.deploy_algorithm())
            b

            Lazy voter example:
            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (1, 1, 1, 1, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 4
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.deploy_algorithm())
            b

            No consensus reached example:
            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (0, 0, 0, 0, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 2
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.deploy_algorithm())
            null
        '''
        logger.info('deploying algorithm')
        # the required score for an alternative to win
        unanimously = len(self.voters)
        logger.debug('required votes for unanimously: %g', unanimously)
        logger.debug('round number: %g', self.remaining_rounds)
        while self.remaining_rounds >= 0:
            logger.debug('voters have cast their ballots')
            self.round_passed()  # mark this round as passed

            # cppyy function call
            currentVotesMap = std.map[int, str]()
            for voter, ballot in self.voters_current_ballot.items():
                currentVotesMap[voter] = ballot
            current_votes_score = dict(
                cppyy.gbl.votesCalculate(currentVotesMap))
            for key, value in current_votes_score.items():
                if value == unanimously:
                    return key
            # all the alternative who's possible to be elected
            possible_winners = list(cppyy.gbl.possibleWinners(
                currentVotesMap, self.remaining_rounds, unanimously))
            logger.debug('round number: %g', self.remaining_rounds)
            # if no alternative is eligible to win - no need to keep iterating
            if possible_winners == [self.default_alternative]:
                logger.debug(
                    'possible winners: %s. Algorithm is finished with no winner', self.default_alternative)
                break
            # if only one option is valid
            elif len(possible_winners) == 1:
                return possible_winners[0]
            voters_candidate = []  # candidate voters to change their ballot
            # select voters to change their ballot base on their type and selected alternative
            for voter_index in range(len(self.voters)):
                voter = self.voters[voter_index]
                voter_type = self.voters_type[voter_index]
                # if voter's current vote isn't eligible to win - mark him as wishes to change ballot
                if self.voters_current_ballot.get(voter_index + 1) not in possible_winners:
                    voters_candidate.append(voter)
                    logger.debug('voter %g wishes to change his ballot', voter)
                # if voter is active and he has more winners candidate alternatives to vote for
                elif voter_type == 1 and len(possible_winners) != 1:
                    voters_candidate.append(voter)
                    logger.debug('voter %g wishes to change his ballot', voter)
            if len(voters_candidate) != 0:
                ballot_change_voter = self.choose_random_voter(
                    voters_candidate)
                ballot_change_voter_preference = self.voters_preferences[ballot_change_voter - 1]
                voter_current_ballot = self.voters_current_ballot[ballot_change_voter]
                # voter chooses to change his ballot to the top possible alternative (besides his current)
                for preference in ballot_change_voter_preference:
                    if preference in possible_winners and preference != voter_current_ballot:
                        self.change_vote(
                            ballot_change_voter, preference, voter_current_ballot)
                        break
        # if unanimously hasn't reached - return default alternative
        return self.default_alternative

    def round_passed(self):
        '''
            Lower round by one - symbolize a passing iteration.

            ---------------------------------TESTS---------------------------------
            >>> v = {1, 2, 3}
            >>> v_type = {1, 1, 1}
            >>> alters = {'a', 'b', 'c'}
            >>> df_alter = 'null'
            >>> vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
            >>> t = 2
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter, voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.remaining_rounds)
            2
        '''
        self.remaining_rounds -= 1

    def possible_winners(self) -> list:
        '''
            Returns the alternatives who are possibly to win, consider their scores and the remaining time.

            Returns:
                List of alternatives with a chance to win

            ---------------------------------TESTS---------------------------------
            >>> v = {1, 2, 3}
            >>> v_type = {1, 1, 1}
            >>> alters = {'a', 'b', 'c'}
            >>> df_alter = 'null'
            >>> vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
            >>> t = 2
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter, voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.possible_winners())
            ['a', 'b', 'c']

            >>> t = 1
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.possible_winners())
            ['a', 'b', 'c']

            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (0, 0, 0, 0, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 4
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.possible_winners())
            ['a', 'b', 'c', 'd']

            >>> t = 3
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter, voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.possible_winners())
            ['a', 'b', 'c']

            >>> t = 2
            >>> vp =[['b', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter, voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.possible_winners())
            ['b']
        '''
        logger.info('calculating possible winners alternatives')
        unanimously = len(
            self.voters)  # the amount of votes needed to reach consensus
        current_votes_score = ConsensusUnderDeadline.votes_calculate(
            self.voters_current_ballot)
        # add all alternatives who haven't been voted for - cover the case where alternative with 0 votes can still be a winner
        for alter in self.alternatives:
            if alter not in current_votes_score:
                current_votes_score[alter] = 0
        possible_winners_alters = []
        logger.debug('total votes: %g', unanimously)
        logger.debug('current vote scores: %s', current_votes_score)
        for alt, score in current_votes_score.items():
            # if an alternative has a chance to get the remaining votes in the remaining time
            if (score + self.remaining_rounds + 1) >= unanimously:
                possible_winners_alters.append(alt)
                logger.debug(
                    'alternative %s nominate as a winner candidate', alt)
        # if none of the alternatives has a chance to be chosen - return default alternative
        if len(possible_winners_alters) == 0:
            return [self.default_alternative]
        logger.debug('possible winners: %s', possible_winners_alters)
        return possible_winners_alters

    def change_vote(self, voter: int, new_vote: str, current_vote: str):
        '''
            Change voters ballot.

            Arguments:
                voter - the voter who shall change his vote
                vote - the voter's new preferred alternative

            ---------------------------------TESTS---------------------------------
            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (0, 0, 0, 0, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 4
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> print(cud.voters_current_ballot)
            {1: 'a', 2: 'a', 3: 'b', 4: 'b', 5: 'c'}

            >>> cud.change_vote(1, 'b', 'a')
            >>> print(cud.voters_current_ballot)
            {1: 'b', 2: 'a', 3: 'b', 4: 'b', 5: 'c'}

            >>> cud.change_vote(2, 'b', 'a')
            >>> print(cud.voters_current_ballot)
            {1: 'b', 2: 'b', 3: 'b', 4: 'b', 5: 'c'}

            >>> cud.change_vote(4, 'd', 'b')
            >>> print(cud.voters_current_ballot)
            {1: 'b', 2: 'b', 3: 'b', 4: 'd', 5: 'c'}
        '''
        if voter not in self.voters:
            raise ValueError(f'''voter doesn't exist''')
        if new_vote not in self.alternatives or current_vote not in self.alternatives:
            raise ValueError(f'''given alternative doesn't exist''')
        if new_vote == current_vote:
            raise ValueError(
                f'''voter can't change his ballot to current one''')
        self.voters_current_ballot[voter] = new_vote
        logger.info('voter %s changed his vote from %s to %s',
                    voter, current_vote, new_vote)

    def choose_random_voter(self, voters: list) -> int:
        '''
            Random voter selection.

            Arguments:
                voters - all the voters who whish to change their ballot

            Returns:
                A voter who shall change is vote

            ---------------------------------TESTS--------------------------------- 
            random_selection true for testing 
            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (0, 0, 0, 0, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 4
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            >>> v = [1, 2, 3]
            >>> print(cud.choose_random_voter(v))
            1

            >>> v = [2, 3, 4]
            >>> print(cud.choose_random_voter(v))
            2

            >>> v = [3, 4, 5, 6]
            >>> print(cud.choose_random_voter(v))
            3
        '''
        ans = random.choice(voters) if self.random_selection else min(voters)
        logger.info('voter %s has been chosen for changing ballot', ans)
        return ans

    @staticmethod
    def votes_calculate(ballots: dict) -> dict:
        '''
            Taken the given votes, return the total score for each ballot.

            Arguments:
                ballots - the voter's preferences for current round

            Returns:
                A dictionary of scores for each alternative

           ---------------------------------TESTS--------------------------------- 
           >>> ballots = {1:'a', 2:'b', 3:'c'}
           >>> print(ConsensusUnderDeadline.votes_calculate(ballots))
           {'a': 1, 'b': 1, 'c': 1}

           >>> ballots = {1:'a', 2:'a', 3:'b', 4:'b', 5:'c'}
           >>> print(ConsensusUnderDeadline.votes_calculate(ballots))
           {'a': 2, 'b': 2, 'c': 1}

           >>> ballots = {1:'a', 2:'a', 3:'b', 4:'a', 5:'d'}
           >>> print(ConsensusUnderDeadline.votes_calculate(ballots))
           {'a': 3, 'b': 1, 'd': 1}
        '''
        return dict(Counter(ballots.values()))


if __name__ == '__main__':
    doctest.testmod()
