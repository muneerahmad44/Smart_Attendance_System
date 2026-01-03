import streamlit as st
from src.smart_attendance import SmartAttendanceSystem
import cv2
import numpy as np
from PIL import Image
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .info-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }
    .status-success {
        color: #00ff00;
        font-weight: bold;
        font-size: 24px;
    }
    .status-warning {
        color: #ffaa00;
        font-weight: bold;
        font-size: 24px;
    }
    .status-error {
        color: #ff0000;
        font-weight: bold;
        font-size: 24px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    h1 {
        color: white;
        text-align: center;
        padding: 20px;
    }
    h3 {
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'system' not in st.session_state:
    st.session_state.system = SmartAttendanceSystem()
if 'attendance_log' not in st.session_state:
    st.session_state.attendance_log = []
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
if 'successful_scans' not in st.session_state:
    st.session_state.successful_scans = 0

def process_frame_with_circle(frame):
    """Process frame and overlay on circular mask with gradient background"""
    # Create gradient background
    height, width = 1080, 1920
    background = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create purple gradient background
    for i in range(height):
        ratio = i / height
        r = int(102 + (118 - 102) * ratio)  # 667eea to 764ba2
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)
        background[i, :] = [b, g, r]
    
    # Circle parameters
    xc, yc = 580, 600
    r = 330
    x1, y1 = xc - r, yc - r
    x2, y2 = xc + r, yc + r
    
    frame_background = background.copy()
    frame_resized = cv2.resize(frame, (x2 - x1, y2 - y1))
    
    # Create circular mask
    mask = np.zeros((y2 - y1, x2 - x1, 3), dtype=np.uint8)
    cv2.circle(mask, (r, r), r, (255, 255, 255), -1)
    circular_frame = cv2.bitwise_and(frame_resized, mask)
    bg_region = frame_background[y1:y2, x1:x2]
    bg_cleared = cv2.bitwise_and(bg_region, 255 - mask)
    final_region = cv2.add(bg_cleared, circular_frame)
    frame_background[y1:y2, x1:x2] = final_region
    
    return frame_background

def add_text_to_frame(frame, results):
    """Add attendance information to frame - text overlay removed"""
    # Text overlay removed - information now displayed only in Streamlit UI
    return frame

# Header
st.markdown("<h1>📸 Smart Attendance System</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    camera_source = st.selectbox("Camera Source", [0, 1, 2], index=0)
    show_processed = st.checkbox("Show Processed Frame", value=True)
    record_video = st.checkbox("Record Video", value=False)
    
    st.markdown("---")
    st.header("📊 Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h2>{st.session_state.total_scans}</h2>
                <p>Total Scans</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h2>{st.session_state.successful_scans}</h2>
                <p>Successful</p>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("🔄 Reset Statistics"):
        st.session_state.total_scans = 0
        st.session_state.successful_scans = 0
        st.session_state.attendance_log = []
        if hasattr(st.session_state, 'last_detected_name'):
            delattr(st.session_state, 'last_detected_name')
        st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Camera Feed")
    video_placeholder = st.empty()
    
with col2:
    st.subheader("👤 Attendance Information")
    info_placeholder = st.empty()
    
    st.markdown("---")
    st.subheader("📝 Recent Attendance Log")
    log_placeholder = st.empty()

# Control buttons
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    start_button = st.button("▶️ Start Camera", width='stretch')
with col_btn2:
    stop_button = st.button("⏹️ Stop Camera", width='stretch')
with col_btn3:
    snapshot_button = st.button("📸 Take Snapshot", width='stretch')

# Camera processing
if start_button:
    st.session_state.camera_running = True

if stop_button:
    st.session_state.camera_running = False

if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False

if st.session_state.camera_running:
    cap = cv2.VideoCapture(camera_source)
    
    if record_video:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = cv2.VideoWriter(
            f'attendance_recording_{timestamp}.mp4',
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (1920, 1080)
        )
    
    while st.session_state.camera_running:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera")
            break
        
        # Process attendance
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = st.session_state.system.in_mark_attendance(img_rgb)
        
        # Only increment total scans when we get a valid detection
        if isinstance(results, dict):
            st.session_state.total_scans += 1
        
        # Process frame
        if show_processed:
            processed_frame = process_frame_with_circle(frame)
            processed_frame = add_text_to_frame(processed_frame, results)
            display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        else:
            display_frame = img_rgb
        
        # Display video
        video_placeholder.image(display_frame, channels="RGB", width='stretch')
        
        # Display information
        if isinstance(results, dict):
            # Only increment successful scans if this is a new unique detection
            current_name = results.get('name', 'Unknown')
            if not hasattr(st.session_state, 'last_detected_name') or st.session_state.last_detected_name != current_name:
                st.session_state.successful_scans += 1
                st.session_state.last_detected_name = current_name
            
            status_class = "status-success" if "success" in results.get('status_text', '').lower() else "status-warning"
            
            info_placeholder.markdown(f"""
                <div class="info-card">
                    <h3>Student Details</h3>
                    <p><strong>ID:</strong> {results.get('id', 'N/A')}</p>
                    <p><strong>Name:</strong> {results.get('name', 'N/A')}</p>
                    <p><strong>Class:</strong> {results.get('role', 'N/A')}</p>
                    <p class="{status_class}">Status: {results.get('status_text', 'N/A')} {results.get('status', '')}</p>
                    <p><small>Time: {datetime.now().strftime('%H:%M:%S')}</small></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Add to log
            log_entry = {
                "time": datetime.now().strftime('%H:%M:%S'),
                "name": results.get('name', 'Unknown'),
                "id": results.get('id', 'N/A'),
                "status": results.get('status_text', 'N/A')
            }
            
            # Check if this exact entry already exists
            entry_exists = any(
                entry['name'] == log_entry['name'] and 
                entry['id'] == log_entry['id'] and 
                entry['time'] == log_entry['time']
                for entry in st.session_state.attendance_log
            )
            
            if not entry_exists:
                st.session_state.attendance_log.insert(0, log_entry)
                if len(st.session_state.attendance_log) > 10:
                    st.session_state.attendance_log.pop()
        else:
            info_placeholder.markdown(f"""
                <div class="info-card">
                    <p class="status-warning">{results}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Display log
        if st.session_state.attendance_log:
            log_container = ""
            for entry in st.session_state.attendance_log:
                log_container += f"""
**{entry['time']}**  
**{entry['name']}** ({entry['id']})  
<span style='color: #00ff00;'>{entry['status']}</span>

---
"""
            log_placeholder.markdown(log_container, unsafe_allow_html=True)
        
        if record_video:
            out.write(processed_frame if show_processed else frame)
        
        time.sleep(0.03)  # ~30 FPS
    
    cap.release()
    if record_video:
        out.release()
        st.success("Video recording saved!")
else:
    video_placeholder.info("Click 'Start Camera' to begin attendance marking")
    info_placeholder.markdown("""
        <div class="info-card">
            <h3>👋 Welcome to Smart Attendance System</h3>
            <p>Position yourself in front of the camera to mark your attendance.</p>
            <p>The system will automatically detect and verify your identity.</p>
        </div>
    """, unsafe_allow_html=True)