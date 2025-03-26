import pymysql

def get_connection():
    """Establish a connection to MySQL database."""
    try:
        conn = pymysql.connect(
            host='localhost',     # Your MySQL host (usually localhost)
            user='root',          # Use 'root' or your MySQL username
            password='utsab',          # Your MySQL password (leave blank if no password)
            database='Online_Taxi_Booking_System',  # Your database name
            port=3306             # Default MySQL port
        )
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None