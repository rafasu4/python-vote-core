from py3votecore.consensus_under_deadline import ConsensusUnderDeadline
import unittest

class TestConsensusUnderDeadline(unittest.TestCase):
    def setUp(self) -> None:
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 2
        self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
    
    def test_init_args(self) -> None:
        v = (1, 2, 3) 
        v_type = (1, 2, 3)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 2
        # voters character is binary
        with self.assertRaises(TypeError):
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = (1, 2, 3), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
        # each voter key must bey unique
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(voters=(1, 1, 1), voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            self.cud = ConsensusUnderDeadline(voters=(1, 1, 2), voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
        # each alternative key must bey unique
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=('a', 'a', 'c'), default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, alternatives=('a', 'c', 'c'), default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
        # number of voters and voter's type must be aligned
        with self.assertRaises(TypeError):
            self.cud = ConsensusUnderDeadline(voters=(1, 2, 3), voters_type = (1, 1), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
            self.cud = ConsensusUnderDeadline(voters=(1), voters_type = (0, 1), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot, remaining_rounds=t)
        # voters ballot must match the existing voters and alternative
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, voters_current_ballot={0: 'a', 2:'b', 3:'c'}, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t)
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, voters_current_ballot={1: 'a', 2:'t', 3:'c'}, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t)
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, voters_current_ballot={1: 'a', 2:'%', 3:'c'}, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t)
            self.cud = ConsensusUnderDeadline(voters=v, voters_type = v_type, voters_current_ballot={7: '&', 4:'^', 3:'c'}, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, remaining_rounds=t)
        # given time must be >= 0
        with self.assertRaises(ValueError):
            self.cud = ConsensusUnderDeadline(remaining_rounds=-1, voters=(1), voters_type = (0, 1), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
            self.cud = ConsensusUnderDeadline(remaining_rounds=-3, voters=(1), voters_type = (0, 1), alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        
    def test_deploy_algorithm_results(self) -> None:
        self.assertEqual(self.cud.deploy_algorithm(), 'b') # classic example
        self.cud.remaining_rounds = 0
        self.assertEqual(self.cud.deploy_algorithm(), 'null') # test case with no time to change the vote
        self.cud.voters_current_ballot = {1: 'a', 2:'a', 3:'a'}
        self.assertEqual(self.cud.deploy_algorithm(), 'a') # test case with unanimously on the start
        self.cud.remaining_rounds = 3
        self.cud.voters_preferences =[['a', 'b', 'c'], ['b', 'a', 'c'],['c', 'a', 'c']]
        self.assertEqual(self.cud.deploy_algorithm(), 'a') # voters have same pretty close preference

    def test_possible_winners(self) -> None:
        self.assertEqual(self.cud.possible_winners() ,['a', 'b', 'c'])
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        self.assertEqual(self.cud.possible_winners() ,[])
        self.cud = ConsensusUnderDeadline(remaining_rounds=4,voters=(1, 2, 3, 4, 5), voters_type = (0, 0, 0, 0, 0), alternatives=('a', 'b', 'c', 'd'), default_alternative=df_alter,voters_preferences={1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }, voters_current_ballot=v_cur_ballot)
        v = (1, 2, 3, 4, 5)
        v_type = (0, 0, 0, 0, 0)
        alters = ('a', 'b', 'c', 'd')
        v_cur_ballot = {1: 'a', 2:'a', 3:'b', 4:'b', 5:'c' }
        vp =[['a', 'b', 'c', 'd'], ['a', 'c', 'b', 'd'], ['b', 'c', 'a', 'd'], ['b', 'a', 'c', 'd'], ['c', 'b', 'd', 'a']]
        t = 4
        self.cud = ConsensusUnderDeadline(remaining_rounds=1,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        self.assertEqual(self.cud.possible_winners() ,['a', 'b', 'c'])
        t = 3
        self.cud = ConsensusUnderDeadline(remaining_rounds=1,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        self.assertEqual(self.cud.possible_winners() ,['a', 'b'])

    def test_change_vote_args(self):
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        # given voter isn't exist
        with self.assertRaises(ValueError):
            self.cud.change_vote(5, 'a')
            self.cud.change_vote(4, 'a')
        # given alternative isn't exist
        with self.assertRaises(ValueError):
            self.cud.change_vote(1, 'd')
            self.cud.change_vote(1, 'e')
        # user hasn't changed his ballot
        with self.assertRaises(ValueError):
            self.cud.change_vote(1, 'a')
            self.cud.change_vote(2, 'b')
    
    def test_change_vote_results(self):
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        self.cud.change_vote(1, 'c')
        self.assertEqual(self.cud.voters_current_ballot, {1: 'c', 2:'b', 3:'c'} )
        self.cud.change_vote(2, 'c')
        self.assertEqual(self.cud.voters_current_ballot, {1: 'c', 2:'c', 3:'c'} )
        self.cud.change_vote(3, 'a')
        self.assertEqual(self.cud.voters_current_ballot, {1: 'c', 2:'c', 3:'a'} )
    
    def test_votes_calculate_results(self):
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 1, 'b': 1, 'c': 1 })
        v = (1, 2, 3)
        v_type = (1, 1, 1)
        alters = ('a', 'b', 'c')
        df_alter = 'null'
        v_cur_ballot = {1: 'a', 2:'a', 3:'c'}
        vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        t = 1
        self.cud = ConsensusUnderDeadline(remaining_rounds=t,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 2, 'b': 0, 'c': 1 })
        v_cur_ballot = {1: 'a', 2:'a', 3:'a'}
        self.cud = ConsensusUnderDeadline(remaining_rounds=t,voters=v, voters_type = v_type, alternatives=alters, default_alternative=df_alter,voters_preferences=vp, voters_current_ballot=v_cur_ballot)
        self.assertEqual(ConsensusUnderDeadline.votes_calculate(self.cud.voters_current_ballot), {'a': 3, 'b': 0, 'c': 0 })

if __name__ == '__main__':
    unittest.main()