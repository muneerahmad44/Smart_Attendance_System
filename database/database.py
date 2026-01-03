import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""   # XAMPP default
)

cursor = conn.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS Faculty_database")
cursor.execute("USE Faculty_database")

# ----------------------------
# Create faculty table
# ----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    deptt VARCHAR(50) NOT NULL,
    PRIMARY KEY (faculty_id)
)
""")

# ----------------------------
# Create attendance table
# ----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    faculty_id VARCHAR(20) NOT NULL,
    attendance_date DATE NOT NULL,
    attendance_time DATETIME NOT NULL,
    attendance_status TINYINT(1) NOT NULL,
    UNIQUE KEY unique_faculty_date (faculty_id, attendance_date),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
""")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("Database and tables created successfully.")
