from py3votecore.consensus_under_deadline import ConsensusUnderDeadline, mdvr
import unittest

class TestConsensusUnderDeadline(unittest.TestCase):
    def setUp(self) -> None:
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 2
        self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp,  remaining_rounds=t, random_selection=False)
    
    def test_init_args(self) -> None:
        v = (1, 2, 3) 
        v_type = (0, 0, 0)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 2
        # voters character is binary
        with self.assertRaises(TypeError):
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = (1, 2, 3), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
        # each voter key must bey unique
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(voters=(1, 1, 1), voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            self.cud = ConsensusUnderDeadline(voters=(1, 1, 2), voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
        # each alternative key must bey unique
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=('a', 'a', 'c'), default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=('a', 'c', 'c'), default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
        # number of voters and voter's type must be aligned
        with self.assertRaises(TypeError):
            self.cud = ConsensusUnderDeadline(voters=(1, 2, 3), voters_type = (1, 1), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
            self.cud = ConsensusUnderDeadline(voters=(1), voters_type = (0, 1), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
        # given time must be >= 0
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(remaining_rounds=-1, voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, random_selection=False)
            self.cud = ConsensusUnderDeadline(remaining_rounds=-3, voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, random_selection=False)

    def test_possible_winners(self) -> None:
        self.assertEqual(self.cud.possible_winners() ,['a', 'b', 'c'])
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 0
        self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False)
        self.assertEqual(self.cud.possible_winners() ,['null'])
        self.cud = ConsensusUnderDeadline(voters=(1, 2, 3, 4, 5), voters_type = (0, 0, 0, 0, 0), alternatives=('a', 'b', 'c', 'd'), voters_preferences=[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']], default_alternative=df_alter,remaining_rounds=4, random_selection=False)
        v = (1, 2, 3, 4, 5)
        v_type = (0, 0, 0, 0, 0)
        alters = ('a', 'b', 'c', 'd')
        vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
        self.cud = ConsensusUnderDeadline(remaining_rounds=4,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, random_selection=False)
        self.assertEqual(self.cud.possible_winners() ,['a', 'b', 'c', 'd'])
        self.cud = ConsensusUnderDeadline(remaining_rounds=3,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, random_selection=False)
        self.assertEqual(self.cud.possible_winners() ,['a', 'b', 'c'])

    def test_change_vote_args(self):
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t, random_selection=False,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp)
        # given voter isn't exist
        with self.assertRaises(ValueError):
            self.cud.change_vote(5, 'a', 'a')
            self.cud.change_vote(4, 'a', 'a')
        # given alternative isn't exist
        with self.assertRaises(ValueError):
            self.cud.change_vote(1, 'd', 'b')
            self.cud.change_vote(1, 'e', 'd')
        # user hasn't changed his ballot
        with self.assertRaises(ValueError):
            self.cud.change_vote(1, 'a', 'a')
            self.cud.change_vote(2, 'b', 'b')
    
    def test_change_vote_results(self):
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t, random_selection=False,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp)
        self.cud.change_vote(1, 'c', 'a')
        self.assertEqual(self.cud.voters_current_ballot, {1: 'c', 2:'b', 3:'c'} )
        self.cud.change_vote(2, 'c', 'b')
        self.assertEqual(self.cud.voters_current_ballot, {1: 'c', 2:'c', 3:'c'} )
        self.cud.change_vote(3, 'a', 'c')
        self.assertEqual(self.cud.voters_current_ballot, {1: 'c', 2:'c', 3:'a'} )
    
    def test_votes_calculate_results(self):
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 1, 'b': 1, 'c': 1 })
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t, random_selection=False,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp)
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 1, 'b': 1, 'c': 1 })
        vp =[['a', 'b', 'c'], ['a', 'b', 'a'],['c', 'a', 'b']]
        self.cud = ConsensusUnderDeadline(remaining_rounds=t, random_selection=False,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp)
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 2, 'c': 1 })
        vp =[['a', 'b', 'c'], ['a', 'b', 'a'],['a', 'c', 'b']]
        self.cud = ConsensusUnderDeadline(remaining_rounds=t, random_selection=False,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp)
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 3 })
    
    def test_mdvr(self) -> None:
        v = (1, 2, 3, 4, 5)
        v_type = (0, 0, 0, 0, 0)
        alters = ('a', 'b', 'c', 'd')
        df_alter = 'null'
        vp = [['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
        t = 4
        self.assertEqual(mdvr(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t, random_selection=False), 'b') # classic example
        self.assertEqual(mdvr(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=0, random_selection=False), 'null') # test case with no time to change the vote
        self.cud.voters_current_ballot = {1: 'a', 2:'a', 3:'a'}
        self.assertEqual(mdvr(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['a', 'c', 'b', 'd'], ['a', 'b', 'c', 'd'], ['a', 'b', 'd', 'c']], remaining_rounds=t, random_selection=False), 'a') # test case with unanimously on the start

if __name__ == '__main__':
    unittest.main()