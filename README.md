# 🎓 Smart Attendance System (Face Recognition Based)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)

A computer vision–based smart attendance system that automatically detects faculty members using face recognition, matches them against a ChromaDB vector database, and records attendance in a MySQL database.

</div>

---

## 📌 Key Features

- 🎥 **Real-time Face Detection** - Instant face detection and embedding extraction from live camera feed
- 🔍 **Vector Similarity Search** - Fast similarity search using ChromaDB vector database
- 🔐 **Secure Identity Matching** - Accurate faculty identity verification with threshold-based matching
- 💾 **MySQL Storage** - Reliable attendance records stored in structured database
- 🖥️ **Interactive UI** - User-friendly Streamlit interface for easy interaction
- 🧩 **Modular Design** - Reusable components and clean project structure

---

## 🧠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core programming language |
| **OpenCV** | Computer vision and image processing |
| **Deep Learning** | 128-D face embeddings generation |
| **ChromaDB** | Vector database for face embeddings |
| **MySQL** | Relational database for attendance records |
| **Streamlit** | Web-based user interface |
| **XAMPP** | Local MySQL database server |

---

## 📁 Project Structure

```
smartattendancesystem2/
|
|__ flow diagrams

|
|__ tested videos
│
├── src/
│   ├── attendance_logic.py          # Core attendance marking logic
│   ├── calculate_embeddings.py      # Face embedding computation
│   └── smart_attendance.py          # Main attendance system module
│
├── vector_dbs/
│   ├── create_vector_db.py          # Initialize ChromaDB
│   ├── add_members.py               # Add faculty to vector DB
│   └── store_faculty.py             # Faculty storage utilities
│
├── database/
│   ├── database.py                  # Database schema creation
│   └── add_faculty_member_to_db.py  # Add faculty to MySQL
│
├── main.py                          # Streamlit application entry point
├── requirements.txt                 # Python dependencies
└── README.md                        # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- XAMPP (for MySQL)
- Webcam/Camera device

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/smartattendancesystem2.git
cd smartattendancesystem2
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📊 Vector Database Setup

### 1️⃣ Create ChromaDB Vector Store

Initialize the persistent vector database for storing face embeddings:

```bash
PYTHONPATH=. python3 vector_dbs/create_vector_db.py
```

**✅ This creates:**
- Persistent ChromaDB instance
- Collection for faculty face embeddings

### 2️⃣ Configure Faculty Data

Update `vector_dbs/add_members.py` with faculty information:

```python
# Required parameters
image_path = "path/to/faculty/photo.jpg"
faculty_id = "unique_faculty_id"  # VERY IMPORTANT

# Metadata (use exact key names)
faculty_meta_data = {
    "name": "Faculty Name",
    "deptt": "Department Name",
    "role": "Designation"
}
```

> ⚠️ **CRITICAL:** Metadata keys must be exactly `"name"`, `"deptt"`, and `"role"` - wrong key names will break retrieval!

### 3️⃣ Add Faculty to Vector DB

```bash
PYTHONPATH=. python3 vector_dbs/add_members.py
```

**Expected output:**
```
[SUCCESS] Faculty '3' added successfully.
```

> 📌 **IMPORTANT:** Remember the `faculty_id` - you'll need it for MySQL database setup!

---

## 💾 MySQL Database Setup

### 1️⃣ Start XAMPP (Linux)

```bash
cd /opt/lampp
sudo ./lampp start
```

Ensure MySQL is running before proceeding.

### 2️⃣ Create Database & Tables

```bash
cd database
python3 database.py
```

**This creates:**
- ✅ Attendance database
- ✅ All required tables
- ✅ Proper schema structure

### 3️⃣ Add Faculty to MySQL Database

Update `add_faculty_member_to_db.py` with:
- Same `faculty_id` used in vector DB
- Faculty name, department, role
- Additional details

```bash
python3 add_faculty_member_to_db.py
```

> ⚠️ The `faculty_id` MUST match between vector DB and MySQL!

---

## 🎯 Running the Application

### Launch Streamlit Application

From the project root directory:

```bash
PYTHONPATH=. streamlit run main.py
```

### Using the System

1. **Open Browser** - Navigate to the Streamlit URL (usually `http://localhost:8501`)
2. **Start Camera** - Click the "Start Camera" button
3. **Automatic Processing:**
   - 🎥 Detects faces in real-time
   - 🔍 Matches embeddings with vector DB
   - ✅ Marks attendance if similarity threshold is met
   - 💾 Stores attendance records in MySQL

---

## ⚠️ Current Limitations

### 🎥 Single Camera Support Only
The system is currently tested and designed for **laptop webcam input only**. Multiple camera feeds or CCTV camera integration is not yet implemented.

### 🔄 No Threading or Parallel Processing
The application processes **one camera feed at a time** without multi-threading support. Concurrent camera handling is part of future development.

### 🚫 Limited Testing Environment
Due to the **unavailability of a second camera** during development, multi-camera functionality and CCTV integration testing could not be performed. The system has been validated only with standard laptop webcams.

> 💡 **Note:** These limitations are acknowledged and will be addressed in future versions. See the [Future Improvements](#-future-improvements) section for planned enhancements.

---

## 🚀 Future Improvements

### High Priority

- 📹 **CCTV Integration** - Deploy system in real-time using CCTV camera footage with proper scaling and load balancing
- 🔄 **Multi-Threading Support** - Implement parallel processing to handle multiple camera feeds simultaneously
- 🎯 **Multiple Camera Handling** - Support for concurrent processing of multiple camera sources with thread-safe operations
- 📊 **Scalable Architecture** - Design system to scale horizontally for large-scale deployments across multiple locations

### Additional Enhancements

- 👁️ **Liveness Detection** - Prevent spoofing attacks using photo or video replay
- ☁️ **Cloud Deployment** - Deploy on AWS, Azure, or GCP with edge computing support
- 🔑 **Role-based Access Control** - Implement admin and user permission levels with secure authentication
- 📱 **Mobile Interface** - Responsive design for mobile devices and tablets
- 📈 **Analytics Dashboard** - Comprehensive attendance analytics with visualization and reporting
- 🔔 **Notification System** - Real-time alerts for attendance events
- 📤 **Data Export** - Export attendance reports in CSV, PDF, and Excel formats

---

## 🛠️ Technical Details

### Face Embeddings
- **Dimension:** 128-D vectors
- **Model:** Deep learning-based face recognition
- **Similarity Metric:** Cosine similarity with threshold-based matching

### Database Schema
- **Vector DB:** ChromaDB for fast similarity search
- **Relational DB:** MySQL for structured attendance records
- **Data Integrity:** Foreign key constraints between faculty and attendance tables

### Performance
- **Real-time Processing:** Real time processing on processor corei5 gen 7 Lenovo
- **Accuracy:** Threshold-based matching with configurable similarity scores
- **Scalability:** Designed for institutional deployment

---


### Database Connection
Update MySQL credentials in `database/database.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'attendance_system'
}
```



## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Muneer Ahmed**

- 🎓 BS Computer Science (AI)
- 🔬 Focus: Computer Vision, Deep Learning, Smart Surveillance Systems
- 💼 Specialization: Face Recognition, Real-time Video Processing

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please feel free to reach out at muneerahmed.dev@gmail.com!

---

## 🌟 Acknowledgments

- Thanks to the ChromaDB team for the excellent vector database
- OpenCV community for comprehensive computer vision tools
- Streamlit for the intuitive web framework

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ by Muneer Ahmed

</div>
