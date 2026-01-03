import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Faculty_database"
)
cursor = db.cursor()

def add_faculty(faculty_id, name, deptt):
    """
    Adds a new faculty member to the faculty table.
    Checks if faculty_id already exists to avoid duplicates.
    
    Args:
        faculty_id (str): Unique ID of the faculty
        name (str): Faculty name
        deptt (str): Department name
    Returns:
        str: Status message
    """
    # Check if faculty already exists
    cursor.execute("SELECT * FROM faculty WHERE faculty_id=%s", (faculty_id,))
    existing = cursor.fetchone()
    
    if existing:
        return f"Faculty {faculty_id} already exists."
    
    # Insert new faculty
    insert_query = "INSERT INTO faculty (faculty_id, name, deptt) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (faculty_id, name, deptt))
    db.commit()
    
    return f"Faculty {faculty_id} added successfully."


# # Example usage
print(add_faculty("3", "Mumtaz", "Computer Science"))

