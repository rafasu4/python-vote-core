

class ConsensusUnderDeadline():
    '''
        A class representing a model for group decision making under strict deadline, based on iterative process. The model was
        presented by Marina Bannikova, Lihi Dery, Svetlana Obraztsova, Zinovi Rabinovich, Jeffrey S. Rosenschein (2019), 
        https://arxiv.org/abs/1905.07173
    '''

    def __init__(self, voters: tuple, alternatives: tuple, voters_preferences: list, default_alternative: int, alternative_scores: dict, remaining_rounds: int) -> int:
        '''
            Constructor for Consensus-Under-Deadline algorithm.

            Arguments:
                voters - all of the enlisted voters
                alternatives - all of the optional choices to vote for 
                voters_preferences - the voters preferences of the votes
                default_alternative - an alternative that will be chosen upon disagreement 
                alternative_scores - the number of votes for each alternative, updated in each round
                remaining_rounds - a threshold for the amount if rounds left until decision should be taken 
            
            Returns:
                The winner alternative
        '''
        pass

    def votes_calculate(self, ballots: dict) -> dict:
        '''
            Taken the given votes, return the total score for each ballot.
            
            Arguments:
                ballots - the voter's preferences for current round

            Returns:
                A dictionary of scores for each alternative
        '''
        pass

    def possible_winners(self) -> list:
        '''
            Returns the alternatives who are possibly win consider their scores and remaining time. 

            Returns:
                List of alternatives with a chance to win
        '''
        pass

    def choose_random_voter(voters: tuple) -> int:
        '''
            Random voter selection.

            Arguments:
                voters - all the voters who whish to change their ballot
            
            Returns:
                A voter who shall change is vote
        '''
        pass

    def change_vote(self, voter: int, vote: str):
        '''
            Change voters ballot.

            Arguments:
                voter - the voter who shall change his vote
                vote - the voter's new preferred alternative 
        '''
        pass

if __name__ == '__main__':
    pass