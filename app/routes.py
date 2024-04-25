import psycopg2
from flask import request, jsonify
from app import app
from app.database import get_db_connection


@app.route('/rates', methods=['GET'])
def get_rates():
    """
    Retrieves average prices for a given date range and route.
    Expects the following parameters in the URL query string:
    - date_from: Start date (YYYY-MM-DD)
    - date_to: End date (YYYY-MM-DD)
    - origin: Origin airport code or region slug
    - destination: Destination airport code or region slug
    Returns:
        JSON response containing average prices for each day in the date range.
    """
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    if not all([date_from, date_to, origin, destination]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Establish a connection to the database
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # SQL query to retrieve average prices
        query = """
                    SELECT day, AVG(price) AS average_price
                        FROM prices
                            JOIN ports AS orig ON prices.orig_code = orig.code OR prices.orig_code = orig.parent_slug
                            JOIN ports AS dest ON prices.dest_code = dest.code OR prices.dest_code = dest.parent_slug
                        WHERE day BETWEEN %s AND %s
                            AND (orig.code = %s OR orig.parent_slug = %s)
                            AND (dest.code = %s OR dest.parent_slug = %s)
                            GROUP BY day
                      HAVING COUNT(price) >= 3;
        """

        # Execute the query with parameters
        cursor.execute(query, (date_from, date_to, origin, origin, destination, destination))

        # Fetch all rows of the result
        results = cursor.fetchall()
    except psycopg2.Error as e:
        # Handle database query failure
        print("Database query failed:", str(e))
        return jsonify({"error": "Database query failed"}), 500
    finally:
        # Close the cursor and database connection
        cursor.close()
        conn.close()

    # Prepare response data
    rates = [{'day': str(result['day']),
              'average_price': float(result['average_price']) if result['average_price'] is not None else None}
             for result in results]
    return jsonify(rates)
