import unittest
from unittest.mock import patch, mock_open
from vote_counter import VoteCounter  

class TestVoteCounterTies(unittest.TestCase):
    def setUp(self):
        # Setup mock prints collector
        self.printed_lines = []
        self.print_patcher = patch('builtins.print')
        self.mock_print = self.print_patcher.start()
        self.mock_print.side_effect = self.printed_lines.append

    def tearDown(self):
        self.print_patcher.stop()
        
    # T1. Basic test  bt two  
    def test_exact_tie_two_candidates(self):
        mock_csv = """city,candidate,votes
City1,Alice,100
City2,Bob,100"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv")
            results, winners = counter.count_votes()
            

            self.assertEqual(len(winners), 2)
            self.assertEqual(results["Alice"], 100)
            self.assertEqual(results["Bob"], 100)
            self.assertIn("Empate entre: Alice, Bob", self.printed_lines)

    # T2. empate con votos inválidos 
    def test_tie_with_invalid_votes(self):
        mock_csv = """city,candidate,votes
City1,Alice,100
City2,Bob,invalid
City3,Bob,100"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv")
            results, winners = counter.count_votes()
            

            self.assertEqual(len(winners), 2)
            self.assertEqual(results["Alice"], 100)
            self.assertEqual(results["Bob"], 100)
            self.assertIn("Empate entre: Alice, Bob", self.printed_lines)

    # T3 tres candidatos 
    def test_tie_multiple_candidates(self):
        mock_csv = """city,candidate,votes
City1,Alice,100
City2,Bob,100
City3,Charlie,100"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv")
            results, winners = counter.count_votes()
            
            # Verifica empate triple
            self.assertEqual(len(winners), 3)
            self.assertEqual(set(winners), {"Alice", "Bob", "Charlie"})
            self.assertIn("Empate entre: Alice, Bob, Charlie", self.printed_lines)

    # T4 Test de empate con múltiples ciudades 
    def test_tie_multiple_cities(self):
        mock_csv = """city,candidate,votes
City1,Alice,50
City2,Alice,50
City1,Bob,75
City2,Bob,25"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv")
            results, winners = counter.count_votes()
            
            # Verifica que la suma de votos por ciudad resulte en empate
            self.assertEqual(len(winners), 2)
            self.assertEqual(results["Alice"], 100)
            self.assertEqual(results["Bob"], 100)
            self.assertIn("Empate entre: Alice, Bob", self.printed_lines)

    # T5 Test de empate con valores extremos 
    def test_tie_edge_values(self):
        mock_csv = """city,candidate,votes
City1,Alice,0
City2,Bob,0
City3,Charlie,0"""
        
        with patch("builtins.open", mock_open(read_data=mock_csv)):
            counter = VoteCounter("votes.csv")
            results, winners = counter.count_votes()
            

            self.assertEqual(len(winners), 3)
            self.assertTrue(all(votes == 0 for votes in results.values()))
            self.assertIn("Empate entre: Alice, Bob, Charlie", self.printed_lines)

if __name__ == '__main__':
    unittest.main()