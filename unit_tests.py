import unittest
from app import app  

class AppTestCases(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True

    def test_index(self):
        # Test that the index page can be accessed
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('players', str(response.data))

    def test_create_player(self):
        # Test creating a new player
        response = self.app.post('/players', data=dict(name='Steph Curry', position='Guard', team='Golden State Warriors'))
        self.assertEqual(response.status_code, 302)  # Redirect after POST should be 302

        response = self.app.get('/')
        self.assertIn('Steph Curry', str(response.data))

    def test_get_players(self):
        # Test retrieving all players
        response = self.app.get('/players')
        self.assertEqual(response.status_code, 202)  # As per your application logic
        self.assertIn('Steph Curry', str(response.data))  # Assuming Steph Curry has been added in a previous test

    def test_update_player(self):
        # Test updating an existing player
        # First, add a player to update
        self.app.post('/players', data=dict(name='Kevin Durant', position='Forward', team='Brooklyn Nets'))
        
        # Update the player (assuming he's at index 0)
        response = self.app.put('/players/0', data=dict(name='Kevin Durant', position='Forward', team='OKC Thunder'))
        self.assertEqual(response.status_code, 200)

        # Verify the update took place
        response = self.app.get('/players')
        self.assertIn('OKC Thunder', str(response.data))

    def test_delete_player(self):
         # Test deleting a player
        # First, ensure the player exists
        self.app.post('/players', data=dict(name='Kyrie Irving', position='Guard', team='Boston Celtics'))
        
        # Retrieve players to find the correct index
        get_response = self.app.get('/players')
        players_list = get_response.get_json()['players']
        player_index = next((index for (index, p) in enumerate(players_list) if p['name'] == 'Kyrie Irving'), None)
        
        # Delete the player
        if player_index is not None:
            delete_response = self.app.delete(f'/players/{player_index}')
            self.assertEqual(delete_response.status_code, 200)

            # Verify the deletion took place
            final_response = self.app.get('/players')
            self.assertNotIn('Kyrie Irving', str(final_response.data))
        else:
            self.fail("Player not found for deletion")

if __name__ == '__main__':
    unittest.main()