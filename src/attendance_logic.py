from src.calculate_embeddings import generate
from vector_dbs.store_faculty import retrieve_from_db
import mysql.connector
from datetime import datetime
import pytz
import time

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Faculty_database"
)
cursor = db.cursor()


def add_faculty_if_not_exists(faculty_id, name, deptt):
    """Add a new faculty to the faculty table if not already present"""
    cursor.execute("SELECT * FROM faculty WHERE faculty_id=%s", (faculty_id,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO faculty (faculty_id, name, deptt) VALUES (%s, %s, %s)",
            (faculty_id, name, deptt),
        )
        db.commit()


def get_faculty_info_from_sql(faculty_id):
    """Retrieve faculty information from SQL database"""
    try:
        cursor.execute(
            """
            SELECT f.faculty_id, f.name, f.deptt, 
                   a.attendance_status, a.attendance_time
            FROM faculty f
            LEFT JOIN attendance a ON f.faculty_id = a.faculty_id 
                AND a.attendance_date = CURDATE()
            WHERE f.faculty_id = %s
            """,
            (faculty_id,)
        )
        result = cursor.fetchone()
        
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "deptt": result[2],
                "status": result[3],  # Can be None if not marked today
                "time": result[4]     # Can be None if not marked today
            }
        return None
        
    except Exception as e:
        print(f"[ERROR] Failed to retrieve faculty info: {e}")
        return None


def in_attendance(img):
    """Mark attendance - shows SQL data after marking"""
    emb = generate(img)
    
    # Handle empty embeddings
    if not emb or len(emb) == 0:
        return {"status": None, "status_text": "NoOneIsFacingCamera"}
    
    results = retrieve_from_db(emb)

    if results == "No matching result found.":
        return {"status": None, "status_text": "NotFound"}
    if results is None:
        return {"status": None, "status_text": "NoOneIsFacingCamera"}
    if results == "No matching faces found above similarity threshold (0.7).":
        return {"status": None, "status_text": "NoRelevantPersonIsFound"}
    
    tz = pytz.timezone("Asia/Karachi")
    now = datetime.now(tz)
    today = now.date()
    current_hour = now.hour

    for result in results:
        if result['Present'] != "Person is found":
            continue

        faculty_id = result['id']
        metadata = result['metadata']
        name = metadata['name']
        deptt = metadata['deptt']
        role = metadata.get('role', 'Faculty')

        # Add faculty if not already in faculty table
        add_faculty_if_not_exists(faculty_id, name, deptt)

        # Check if attendance already marked today
        cursor.execute(
            "SELECT attendance_status FROM attendance WHERE faculty_id=%s AND attendance_date=%s",
            (faculty_id, today),
        )
        record = cursor.fetchone()

        if record:
            # Already marked today - retrieve info from SQL
            sql_info = get_faculty_info_from_sql(faculty_id)
            
            if sql_info:
                if record[0] == 0 and 7 <= current_hour < 11:
                    # Previously absent, now present → update
                    cursor.execute(
                        """
                        UPDATE attendance
                        SET attendance_status=%s, attendance_time=%s
                        WHERE faculty_id=%s AND attendance_date=%s
                        """,
                        (1, now, faculty_id, today),
                    )
                    db.commit()
                    
                    # Get updated info from SQL
                    sql_info = get_faculty_info_from_sql(faculty_id)
                    
                    return {
                        "id": sql_info['id'],
                        "name": sql_info['name'],
                        "role": role,
                        "deptt": sql_info['deptt'],
                        "status": sql_info['status'],
                        "time": sql_info['time'],
                        "status_text": "UpdatedToPresent",
                    }
                else:
                    # Return info from SQL database
                    return {
                        "id": sql_info['id'],
                        "name": sql_info['name'],
                        "role": role,
                        "deptt": sql_info['deptt'],
                        "status": sql_info['status'],
                        "time": sql_info['time'],
                        "status_text": "AlreadyMarked",
                    }
            else:
                # Fallback to vector DB info if SQL retrieval fails
                return {
                    "id": faculty_id,
                    "name": name,
                    "role": role,
                    "deptt": deptt,
                    "status": record[0],
                    "status_text": "AlreadyMarked",
                }

        # Not yet marked today → check attendance window
        if 7 <= current_hour < 14:
            cursor.execute(
                """
                INSERT INTO attendance (faculty_id, attendance_date, attendance_time, attendance_status)
                VALUES (%s, %s, %s, %s)
                """,
                (faculty_id, today, now, 1),
            )
            db.commit()
            
            # Get info from SQL after inserting
            sql_info = get_faculty_info_from_sql(faculty_id)
            
            if sql_info:
                return {
                    "id": sql_info['id'],
                    "name": sql_info['name'],
                    "role": role,
                    "deptt": sql_info['deptt'],
                    "status": sql_info['status'],
                    "time": sql_info['time'],
                    "status_text": "MarkedNow",
                }
            else:
                # Fallback to vector DB info
                return {
                    "id": faculty_id,
                    "name": name,
                    "role": role,
                    "deptt": deptt,
                    "status": 1,
                    "status_text": "MarkedNow",
                }
        else:
            return {"status": None, "status_text": "CannotMark"}


def mark_absent_camera(img):
    """Mark absent - shows SQL data after marking"""
    emb = generate(img)
    
    # Handle empty embeddings
    if not emb or len(emb) == 0:
        return {"status": None, "status_text": "NoOneIsFacingCamera"}
    
    results = retrieve_from_db(emb)

    if results == "No matching result found.":
        return {"status": None, "status_text": "NotFound"}
    if results is None:
        return {"status": None, "status_text": "NoOneIsFacingCamera"}
    if results == "No matching faces found above similarity threshold (0.7).":
        return {"status": None, "status_text": "NoRelevantPersonIsFound"}

    tz = pytz.timezone("Asia/Karachi")
    now = datetime.now(tz)
    today = now.date()
    current_hour = now.hour

    for result in results:
        if result['Present'] != "Person is found":
            continue

        faculty_id = result['id']
        metadata = result['metadata']
        name = metadata['name']
        deptt = metadata['deptt']
        role = metadata.get('role', 'Faculty')

        # Add faculty if not already in faculty table
        add_faculty_if_not_exists(faculty_id, name, deptt)

        # Check if already marked today
        cursor.execute(
            "SELECT attendance_status FROM attendance WHERE faculty_id=%s AND attendance_date=%s",
            (faculty_id, today),
        )
        record = cursor.fetchone()

        if record:
            # Already marked today - retrieve info from SQL
            sql_info = get_faculty_info_from_sql(faculty_id)
            
            if sql_info:
                if current_hour >= 16:
                    # After 4 PM - day completed
                    return {
                        "id": sql_info['id'],
                        "name": sql_info['name'],
                        "role": role,
                        "deptt": sql_info['deptt'],
                        "status": sql_info['status'],
                        "time": sql_info['time'],
                        "status_text": "DayCompleted",
                    }
                else:
                    # Update to absent
                    cursor.execute(
                        """
                        UPDATE attendance
                        SET attendance_status=%s, attendance_time=%s
                        WHERE faculty_id=%s AND attendance_date=%s
                        """,
                        (0, now, faculty_id, today),
                    )
                    db.commit()
                    
                    # Get updated info from SQL
                    sql_info = get_faculty_info_from_sql(faculty_id)
                    
                    return {
                        "id": sql_info['id'],
                        "name": sql_info['name'],
                        "role": role,
                        "deptt": sql_info['deptt'],
                        "status": sql_info['status'],
                        "time": sql_info['time'],
                        "status_text": "MarkedAbsent",
                    }
            else:
                # Fallback to vector DB info
                if current_hour >= 16:
                    return {
                        "id": faculty_id,
                        "name": name,
                        "role": role,
                        "deptt": deptt,
                        "status": record[0],
                        "status_text": "DayCompleted",
                    }
                else:
                    cursor.execute(
                        """
                        UPDATE attendance
                        SET attendance_status=%s, attendance_time=%s
                        WHERE faculty_id=%s AND attendance_date=%s
                        """,
                        (0, now, faculty_id, today),
                    )
                    db.commit()
                    return {
                        "id": faculty_id,
                        "name": name,
                        "role": role,
                        "deptt": deptt,
                        "status": 0,
                        "status_text": "MarkedAbsent",
                    }

        # Not yet marked today → mark absent if before 4 PM
        if current_hour < 16:
            cursor.execute(
                """
                INSERT INTO attendance (faculty_id, attendance_date, attendance_time, attendance_status)
                VALUES (%s, %s, %s, %s)
                """,
                (faculty_id, today, now, 0),
            )
            db.commit()
            
            # Get info from SQL after inserting
            sql_info = get_faculty_info_from_sql(faculty_id)
            
            if sql_info:
                return {
                    "id": sql_info['id'],
                    "name": sql_info['name'],
                    "role": role,
                    "deptt": sql_info['deptt'],
                    "status": sql_info['status'],
                    "time": sql_info['time'],
                    "status_text": "MarkedAbsent",
                }
            else:
                # Fallback to vector DB info
                return {
                    "id": faculty_id,
                    "name": name,
                    "role": role,
                    "deptt": deptt,
                    "status": 0,
                    "status_text": "MarkedAbsent",
                }
        else:
            # After 4 PM - retrieve from SQL if exists
            sql_info = get_faculty_info_from_sql(faculty_id)
            
            if sql_info:
                return {
                    "id": sql_info['id'],
                    "name": sql_info['name'],
                    "role": role,
                    "deptt": sql_info['deptt'],
                    "status": sql_info['status'],
                    "time": sql_info['time'],
                    "status_text": "DayCompleted",
                }
            else:
                return {
                    "id": faculty_id,
                    "name": name,
                    "role": role,
                    "deptt": deptt,
                    "status": None,
                    "status_text": "DayCompleted",
                }


def get_attendance_summary(date=None):
    """Get attendance summary for a specific date"""
    try:
        if date is None:
            date = datetime.now(pytz.timezone("Asia/Karachi")).date()
        
        cursor.execute(
            """
            SELECT f.faculty_id, f.name, f.deptt, 
                   COALESCE(a.attendance_status, -1) as status,
                   a.attendance_time
            FROM faculty f
            LEFT JOIN attendance a ON f.faculty_id = a.faculty_id 
                AND a.attendance_date = %s
            ORDER BY f.name
            """,
            (date,)
        )
        
        results = cursor.fetchall()
        
        summary = {
            "date": date,
            "total": len(results),
            "present": 0,
            "absent": 0,
            "not_marked": 0,
            "faculty": []
        }
        
        for row in results:
            status = row[3]
            if status == 1:
                summary["present"] += 1
                status_text = "Present"
            elif status == 0:
                summary["absent"] += 1
                status_text = "Absent"
            else:
                summary["not_marked"] += 1
                status_text = "Not Marked"
            
            summary["faculty"].append({
                "id": row[0],
                "name": row[1],
                "deptt": row[2],
                "status": status,
                "status_text": status_text,
                "time": row[4]
            })
        
        return summary
        
    except Exception as e:
        print(f"[ERROR] Failed to get attendance summary: {e}")
        return None