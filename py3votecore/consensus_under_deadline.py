import doctest

class ConsensusUnderDeadline():
    '''
        A class representing a model for group decision making under strict deadline, based on iterative process. Each alternative must be accept
        by unanimously.
        The model was presented by Marina Bannikova, Lihi Dery, Svetlana Obraztsova, Zinovi Rabinovich, Jeffrey S. Rosenschein (2019), 
        https://arxiv.org/abs/1905.07173

        Author: Raphael Suliman
    '''

    def __init__(self, voters: tuple, voters_type: tuple, alternatives: tuple, voters_preferences: list,
                default_alternative: str, voters_current_ballot: dict, remaining_rounds: int) -> int:
        '''
            Constructor for Consensus-Under-Deadline algorithm.

            Arguments:
                voters - all of the enlisted voters
                voters_type - whether the voter is an 'active' one, or 'lazy'. 1 - active, 0 - lazy
                alternatives - all of the optional choices to vote for 
                voters_preferences - the voters preferences of the alternatives in decreasing order
                default_alternative - an alternative that will be chosen upon disagreement 
                voters_current_ballot - voter's ballot in current round
                remaining_rounds - a threshold for the amount if rounds left until decision should be taken 
        '''
        self.voters = voters
        self.voters_type = voters_type
        self.alternatives = alternatives
        self.voters_preferences = voters_preferences
        self.default_alternative = default_alternative
        self.voters_current_ballot = voters_current_ballot
        self.remaining_rounds = remaining_rounds
    
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
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
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
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.deploy_algorithm())
            b

            No consensus reached example:
            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (0, 0, 0, 0, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 3
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.deploy_algorithm())
            null
        '''
        return 0
    
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
            >>> v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
            >>> t = 2
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.possible_winners())
            [a, b, c]

            >>> t = 1
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.possible_winners())
            []

            >>> v = (1, 2, 3, 4, 5)
            >>> v_type = (0, 0, 0, 0, 0)
            >>> alters = ('a', 'b', 'c', 'd')
            >>> df_alter = 'null'
            >>> v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            >>> vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
            >>> t = 4
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.possible_winners())
            [a, b, c]

            >>> t = 3
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.possible_winners())
            [a, b]

            >>> t = 2
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.possible_winners())
            [b]
        '''
        return 0

    def change_vote(self, voter: int, vote: str):
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
            >>> cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            >>> print(cud.voters_current_ballot)
            {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
            
            >>> cud.change_vote(1, 'b')
            >>> print(cud.voters_current_ballot)
            {1: 'b', 2:'a', 3:'b', 4:'b', 5:'c' }

            >>> cud.change_vote(2, 'b')
            >>> print(cud.voters_current_ballot)
            {1: 'b', 2:'b', 3:'b', 4:'b', 5:'c' }

            >>> cud.change_vote(4, 'd')
            >>> print(cud.voters_current_ballot)
            {1: 'b', 2:'a', 3:'b', 4:'d', 5:'c' }
        '''
        return 0

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
           {'a': 1, 'b': 1, 'c': 1 }

           >>> ballots = {1:'a', 2:'a', 3:'b', 4:'b', 5:'c'}
           >>> print(ConsensusUnderDeadline.votes_calculate(ballots))
           {'a': 2, 'b': 2, 'c': 1, 'd': 0 }

           >>> ballots = {1:'a', 2:'a', 3:'b', 4:'a', 5:'d'}
           >>> print(ConsensusUnderDeadline.votes_calculate(ballots))
           {'a': 3, 'b': 1, 'c': 0, 'd': 1 }
        '''
        return 0
    
    @staticmethod
    def choose_random_voter(voters: list) -> int:
        '''
            Random voter selection.

            Arguments:
                voters - all the voters who whish to change their ballot
            
            Returns:
                A voter who shall change is vote

            ---------------------------------TESTS--------------------------------- 
            Seed will be used for testing
            >>> v = [1, 2, 3]
            >>> print(ConsensusUnderDeadline.choose_random_voter(v))
            1

            >>> v = [1, 2, 3]
            >>> print(ConsensusUnderDeadline.choose_random_voter(v))
            2

            >>> v = [1, 2, 3]
            >>> print(ConsensusUnderDeadline.choose_random_voter(v))
            3

        '''
        return 0


if __name__ == '__main__':
    doctest.testmod()