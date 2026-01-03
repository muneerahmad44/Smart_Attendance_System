# 📸 Smart Attendance System

A face recognition-based attendance management system built with Python, Streamlit, and ChromaDB. This system enables automated attendance tracking using facial recognition technology with a modern, user-friendly interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Real-time Face Recognition**: Instant faculty/student identification through camera
- **Automated Attendance Marking**: Automatic attendance logging with timestamp
- **Time-based Validation**: Configurable attendance windows (7 AM - 9 AM for marking present)
- **Duplicate Prevention**: Smart detection to prevent multiple entries for the same person
- **Modern UI**: Beautiful gradient-based Streamlit interface with live statistics
- **Video Recording**: Optional recording of attendance sessions
- **Attendance Logs**: Real-time display of recent attendance records
- **MySQL Database Integration**: Persistent storage of attendance records
- **Vector Database**: ChromaDB for efficient face embedding storage and retrieval

## 🎯 System Architecture

```
┌─────────────────┐
│  Camera Input   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Face Detection  │
│  & Embedding    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ChromaDB      │
│ Vector Search   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MySQL Database │
│ Attendance Log  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Streamlit UI    │
└─────────────────┘
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Face Recognition**: face_recognition library (dlib-based)
- **Vector Database**: ChromaDB
- **Relational Database**: MySQL
- **Computer Vision**: OpenCV
- **Embeddings**: 128-dimensional face encodings

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server
- Webcam/Camera
- 4GB RAM minimum (8GB recommended)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
```

**macOS:**
```bash
brew install cmake
```

### 5. Setup MySQL Database

```sql
CREATE DATABASE Faculty_database;

USE Faculty_database;

CREATE TABLE facultyinfo (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    deptt VARCHAR(100),
    role VARCHAR(50),
    attendance_status INT DEFAULT 0,
    attendance_time DATETIME,
    last_attendance_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Configure Database Connection

Update the database credentials in `attendance_logic.py`:

```python
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="Faculty_database"
)
```

## 📦 Dependencies

Create a `requirements.txt` file with:

```txt
streamlit>=1.28.0
opencv-python>=4.8.0
face-recognition>=1.3.0
chromadb>=0.4.0
mysql-connector-python>=8.1.0
numpy>=1.24.0
Pillow>=10.0.0
pytz>=2023.3
```

## 🎮 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Adding Faculty Members

```python
from smart_attendance import SmartAttendanceSystem
import cv2

system = SmartAttendanceSystem()

# Load faculty image
img = cv2.imread("faculty_photo.jpg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Add to system
system.add_member(
    create_db=False,  # Set True only for first time
    add_faculty=True,
    img=img_rgb,
    faculty_id="F001",
    faculty_metadata={
        "name": "John Doe",
        "role": "Professor",
        "deptt": "Computer Science"
    }
)
```

### Marking Attendance

1. Click **"Start Camera"** button
2. Position yourself in front of the camera
3. System automatically detects and marks attendance
4. View real-time status in the right panel

### Viewing Attendance Records

```python
# Query database for attendance records
SELECT * FROM facultyinfo 
WHERE last_attendance_date = CURDATE();
```

## ⚙️ Configuration

### Attendance Time Windows

Edit in `attendance_logic.py`:

```python
# Present marking window (default: 7 AM - 9 AM)
if 7 <= current_hour < 9:
    attendance_status = 1  # Present

# Absent marking cutoff (default: 4 PM)
if current_hour < 16:
    attendance_status = 0  # Absent
```

### Face Recognition Threshold

Edit in `store_faculty.py`:

```python
# Similarity threshold (default: 0.7)
if similarity >= 0.7:
    matched_faces.append({...})
```

### Camera Settings

In Streamlit sidebar:
- **Camera Source**: Select camera device (0, 1, 2)
- **Show Processed Frame**: Toggle circular overlay
- **Record Video**: Enable/disable video recording

## 📊 Database Schema

### facultyinfo Table

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR(50) | Unique faculty ID (Primary Key) |
| name | VARCHAR(100) | Faculty name |
| deptt | VARCHAR(100) | Department |
| role | VARCHAR(50) | Position/Role |
| attendance_status | INT | 0=Absent, 1=Present |
| attendance_time | DATETIME | Time of attendance marking |
| last_attendance_date | DATE | Date of last attendance |
| created_at | TIMESTAMP | Record creation time |

## 🔒 Status Codes

| Status Text | Description |
|-------------|-------------|
| MarkedNow | Successfully marked present |
| AlreadyMarked | Already marked for today |
| UpdatedToPresent | Updated from absent to present |
| MarkedAbsent | Marked as absent |
| NotFound | Face not recognized in database |
| NoOneIsFacingCamera | No face detected |
| DayCompleted | Outside marking hours |
| CannotMark | Outside attendance window |

## 🎨 UI Features

- **Live Camera Feed**: Circular masked video display
- **Statistics Dashboard**: 
  - Total Scans Counter
  - Successful Scans Counter
  - Reset Statistics Button
- **Attendance Information Panel**:
  - ID, Name, Department, Role
  - Color-coded status indicators
  - Timestamp
- **Recent Attendance Log**: Last 10 attendance records

## 🐛 Troubleshooting

### Camera Not Opening
```bash
# Check available cameras
ls /dev/video*

# Test camera
ffplay /dev/video0
```

### Face Recognition Issues
- Ensure proper lighting
- Face should be clearly visible
- Remove glasses/masks if possible
- Minimum image size: 640x480

### Database Connection Error
```python
# Test connection
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Faculty_database"
)
print("Connected!" if db.is_connected() else "Failed")
```

### ChromaDB Errors
```bash
# Delete and recreate database
rm -rf chroma_db/
python -c "from smart_attendance import SmartAttendanceSystem; s = SmartAttendanceSystem(); s.add_member(True, False)"
```

## 📈 Performance Optimization

- **Image Resizing**: Faces are scaled to 0.25x for faster processing
- **Embedding Caching**: Face embeddings stored in ChromaDB
- **Frame Rate**: Limited to ~30 FPS for optimal performance
- **Batch Processing**: Multiple faces can be processed simultaneously

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- face_recognition library by Adam Geitgey
- Streamlit for the amazing framework
- ChromaDB for vector database
- OpenCV community

## 📧 Contact

For questions or support, please open an issue or contact: your.email@example.com

## 🔮 Future Enhancements

- [ ] Multi-camera support
- [ ] Mobile app integration
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Export attendance reports (PDF/Excel)
- [ ] Face mask detection
- [ ] Temperature screening integration
- [ ] Cloud deployment guide
- [ ] Docker containerization
- [ ] REST API endpoints

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)

### Attendance Marking
![Attendance](screenshots/attendance_marking.png)

### Statistics Dashboard
![Dashboard](screenshots/dashboard.png)

---

⭐ If you find this project useful, please consider giving it a star!

**Made with ❤️ using Python and Streamlit**