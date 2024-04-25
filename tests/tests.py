import unittest

from app import app
from app.database import get_db_connection


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test client for Flask app."""
        self.app = app.test_client()

    def test_missing_parameters(self):
        """Test for missing parameters in the request."""
        # Send a request with missing parameters
        response = self.app.get('/rates', json={'date_to': '2016-01-07', 'origin': 'CNGGZ',
                                                'destination': 'EETLL'})
        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        # Extract JSON data from the response
        data = response.get_json()
        # Check if the 'error' key exists in the response data
        self.assertIn('error', data)
        # Check if the error message is as expected
        self.assertEqual(data['error'], 'Missing required parameters')

    def test_database_works(self):
        """Test database connectivity and data retrieval."""
        # Establish a connection to the database
        conn = get_db_connection()
        # Check if the connection is successful
        self.assertIsNotNone(conn)

        try:
            # Execute a sample query to fetch a limited number of records from the database
            cursor = conn.cursor()
            query = "SELECT * FROM prices LIMIT 2"
            cursor.execute(query)
            # Fetch the results
            results = cursor.fetchall()
            # Assert that some records are retrieved
            self.assertGreater(len(results), 0)
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()


if __name__ == '__main__':
    unittest.main()
