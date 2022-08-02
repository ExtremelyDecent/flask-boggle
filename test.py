from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Set up before testing"""
        self.client = app.test_client()
        app.config ['TESTING'] = True
    
    def test_home(self):
        """ Makes sure board, nplay, highscore, score and timer are in session and"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplay'))
    
    def test_valid_word(self):
        """Tests for word validity by modifying the session board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["B", "A", "T", "T", "T"], 
                                 ["R", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=bat')
        self.assertEqual(response.json['result'], 'ok')
        response = self.client.get('/check-word?word=rat')
        self.assertEqual(response.json['result'], 'ok')
        
    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')