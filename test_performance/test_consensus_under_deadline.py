from consensus_under_deadline import ConsensusUnderDeadline
import unittest

class TestConsensusUnderDeadline(unittest.TestCase):
    def setUp(self) -> None:
        self.v = (1, 2, 3)
        self.v_type = (1, 1, 1)
        self.alters = ('a', 'b', 'c')
        self.df_alter = 'null'
        self.v_cur_ballot = {1: 'a', 2:'b', 3:'c'}
        self.vp =[['a', 'b', 'c'], ['b', 'c', 'a'],['c', 'a', 'b']]
        self.t = 2
        self.cud = ConsensusUnderDeadline(voters=self.v, voters_type = self.v_type, alternatives=self.alters, default_alternative=self.df_alter,voters_preferences=self.vp, voters_current_ballot=self.v_cur_ballot, remaining_rounds=self.t)
    
    def test_prop(self) -> None:
        self.assertEqual(self.cud.voters, (1, 2, 3))

if __name__ == '__main__':
    unittest.main()