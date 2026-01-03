<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Attendance System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 60px 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: fadeInDown 0.8s ease;
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h1 {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .subtitle {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 30px;
        }

        .badges {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .badge {
            padding: 8px 16px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }

        .section {
            background: white;
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            animation: fadeInUp 0.8s ease;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h2 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h3 {
            color: #764ba2;
            font-size: 1.5em;
            margin: 25px 0 15px 0;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .feature-card {
            padding: 25px;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        }

        .feature-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }

        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
        }

        .tech-item {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 25px;
            font-weight: 600;
            transition: transform 0.3s ease;
        }

        .tech-item:hover {
            transform: scale(1.1);
        }

        .tree-structure {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 25px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            margin-top: 20px;
            position: relative;
        }

        .tree-structure::before {
            content: "📁 Project Structure";
            display: block;
            color: #4ec9b0;
            font-weight: bold;
            margin-bottom: 15px;
            font-size: 1.1em;
        }

        .command-box {
            background: #2d2d2d;
            color: #00ff00;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            border-left: 4px solid #667eea;
            position: relative;
            cursor: pointer;
        }

        .command-box:hover {
            background: #3d3d3d;
        }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #667eea;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background 0.3s ease;
        }

        .copy-btn:hover {
            background: #764ba2;
        }

        .steps-container {
            counter-reset: step-counter;
        }

        .step {
            position: relative;
            padding-left: 60px;
            margin-bottom: 30px;
        }

        .step::before {
            counter-increment: step-counter;
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }

        .warning-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .error-box {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .success-box {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .info-box {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .author-card {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px;
            margin-top: 20px;
        }

        .author-avatar {
            width: 80px;
            height: 80px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2em;
        }

        .tab-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .tab-btn {
            padding: 12px 24px;
            background: #f5f7fa;
            border: 2px solid #667eea;
            color: #667eea;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .tab-btn.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .metadata-code {
            background: #2d2d2d;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
        }

        .keyword {
            color: #c586c0;
        }

        .string {
            color: #ce9178;
        }

        .limitation-card {
            background: #f8f9fa;
            border-left: 4px solid #6c757d;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        }

        .limitation-card h4 {
            color: #6c757d;
            margin-bottom: 10px;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }

            .features-grid {
                grid-template-columns: 1fr;
            }

            .section {
                padding: 20px;
            }
        }

        .scroll-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s ease;
            font-size: 1.5em;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .scroll-top.visible {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎓 Smart Attendance System</h1>
            <p class="subtitle">Face Recognition Based Attendance Management</p>
            <div class="badges">
                <span class="badge">Python 3</span>
                <span class="badge">OpenCV</span>
                <span class="badge">ChromaDB</span>
                <span class="badge">MySQL</span>
                <span class="badge">Streamlit</span>
            </div>
        </header>

        <div class="section">
            <h2>📌 Key Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🎥</div>
                    <h3>Real-time Detection</h3>
                    <p>Instant face detection and embedding extraction from live camera feed</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <h3>Vector Search</h3>
                    <p>Fast similarity search using ChromaDB vector database</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔐</div>
                    <h3>Secure Matching</h3>
                    <p>Accurate faculty identity verification with threshold-based matching</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💾</div>
                    <h3>MySQL Storage</h3>
                    <p>Reliable attendance records stored in structured database</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🖥️</div>
                    <h3>Interactive UI</h3>
                    <p>User-friendly Streamlit interface for easy interaction</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🧩</div>
                    <h3>Modular Design</h3>
                    <p>Reusable components and clean project structure</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🧠 Tech Stack</h2>
            <div class="tech-stack">
                <span class="tech-item">Python 3</span>
                <span class="tech-item">OpenCV</span>
                <span class="tech-item">Deep Learning</span>
                <span class="tech-item">128-D Face Embeddings</span>
                <span class="tech-item">ChromaDB</span>
                <span class="tech-item">MySQL</span>
                <span class="tech-item">Streamlit</span>
                <span class="tech-item">XAMPP</span>
            </div>
        </div>

        <div class="section">
            <h2>📁 Project Structure</h2>
            <div class="tree-structure">smartattendancesystem2/
│
├── src/
│   ├── attendance_logic.py
│   ├── calculate_embeddings.py
│   └── smart_attendance.py
│
├── vector_dbs/
│   ├── create_vector_db.py
│   ├── add_members.py
│   └── store_faculty.py
│
├── database/
│   ├── database.py
│   └── add_faculty_member_to_db.py
│
├── main.py
├── requirements.txt
└── README.md</div>
        </div>

        <div class="section">
            <h2>🚀 Installation & Setup</h2>
            
            <div class="tab-container">
                <button class="tab-btn active" onclick="switchTab('setup1')">Vector DB Setup</button>
                <button class="tab-btn" onclick="switchTab('setup2')">MySQL Setup</button>
                <button class="tab-btn" onclick="switchTab('setup3')">Run Application</button>
            </div>

            <div id="setup1" class="tab-content active">
                <div class="steps-container">
                    <div class="step">
                        <h3>Create ChromaDB Vector Store</h3>
                        <p>Initialize the persistent vector database for storing face embeddings.</p>
                        <div class="command-box" onclick="copyCommand(this)">
                            <button class="copy-btn">Copy</button>
                            <code>PYTHONPATH=. python3 vector_dbs/create_vector_db.py</code>
                        </div>
                        <div class="success-box">
                            ✅ This creates a persistent ChromaDB and collection for faculty face embeddings
                        </div>
                    </div>

                    <div class="step">
                        <h3>Configure Faculty Data</h3>
                        <p>Update <code>vector_dbs/add_members.py</code> with faculty information:</p>
                        <ul>
                            <li><strong>image_path</strong> → Path to faculty photo</li>
                            <li><strong>faculty_id</strong> → Unique identifier (CRITICAL)</li>
                            <li><strong>faculty_meta_data</strong> → Personal information</li>
                        </ul>
                        
                        <div class="warning-box">
                            ⚠️ <strong>Metadata Rules (STRICT)</strong><br>
                            Your metadata must contain these exact key names:
                        </div>
                        
                        <div class="metadata-code">
<span class="keyword">faculty_meta_data</span> = {
    <span class="string">"name"</span>: <span class="string">"Faculty Name"</span>,
    <span class="string">"deptt"</span>: <span class="string">"Department Name"</span>,
    <span class="string">"role"</span>: <span class="string">"Designation"</span>
}</div>
                        
                        <div class="error-box">
                            ❌ Wrong key names will break retrieval<br>
                            ✅ Keys must be exactly: <code>"name"</code>, <code>"deptt"</code>, <code>"role"</code>
                        </div>
                    </div>

                    <div class="step">
                        <h3>Add Faculty to Vector DB</h3>
                        <div class="command-box" onclick="copyCommand(this)">
                            <button class="copy-btn">Copy</button>
                            <code>PYTHONPATH=. python3 vector_dbs/add_members.py</code>
                        </div>
                        <p><strong>Expected output:</strong></p>
                        <div class="success-box">
                            [SUCCESS] Faculty '3' added successfully.
                        </div>
                        <div class="warning-box">
                            📌 <strong>IMPORTANT:</strong> Remember this <code>faculty_id</code>! You'll need it for the MySQL database.
                        </div>
                    </div>
                </div>
            </div>

            <div id="setup2" class="tab-content">
                <div class="steps-container">
                    <div class="step">
                        <h3>Start XAMPP (Linux)</h3>
                        <p>Make sure XAMPP is installed and start the MySQL service.</p>
                        <div class="command-box" onclick="copyCommand(this)">
                            <button class="copy-btn">Copy</button>
                            <code>cd /opt/lampp<br>sudo ./lampp start</code>
                        </div>
                        <div class="success-box">
                            ✅ Ensure MySQL is running before proceeding
                        </div>
                    </div>

                    <div class="step">
                        <h3>Create Database & Tables</h3>
                        <div class="command-box" onclick="copyCommand(this)">
                            <button class="copy-btn">Copy</button>
                            <code>cd database<br>python3 database.py</code>
                        </div>
                        <p>This will create:</p>
                        <ul>
                            <li>✅ Attendance database</li>
                            <li>✅ All required tables</li>
                            <li>✅ Proper schema structure</li>
                        </ul>
                    </div>

                    <div class="step">
                        <h3>Add Faculty to MySQL Database</h3>
                        <p>Update <code>add_faculty_member_to_db.py</code> with:</p>
                        <ul>
                            <li>Same <code>faculty_id</code> used in vector DB</li>
                            <li>Faculty name, department, role</li>
                            <li>Additional details</li>
                        </ul>
                        <div class="command-box" onclick="copyCommand(this)">
                            <button class="copy-btn">Copy</button>
                            <code>python3 add_faculty_member_to_db.py</code>
                        </div>
                        <div class="error-box">
                            ⚠️ The <code>faculty_id</code> MUST match between vector DB and MySQL!
                        </div>
                    </div>
                </div>
            </div>

            <div id="setup3" class="tab-content">
                <div class="steps-container">
                    <div class="step">
                        <h3>Launch Streamlit Application</h3>
                        <p>From the project root directory, run:</p>
                        <div class="command-box" onclick="copyCommand(this)">
                            <button class="copy-btn">Copy</button>
                            <code>PYTHONPATH=. streamlit run main.py</code>
                        </div>
                    </div>

                    <div class="step">
                        <h3>Use the System</h3>
                        <ol style="margin-left: 20px;">
                            <li>Open the Streamlit URL in your browser</li>
                            <li>Click <strong>Start Camera</strong></li>
                            <li>The system will automatically:
                                <ul style="margin-left: 20px; margin-top: 10px;">
                                    <li>🎥 Detect faces in real-time</li>
                                    <li>🔍 Match embeddings with vector DB</li>
                                    <li>✅ Mark attendance if similarity threshold is met</li>
                                    <li>💾 Store attendance records in MySQL</li>
                                </ul>
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>⚠️ Current Limitations</h2>
            
            <div class="limitation-card">
                <h4>🎥 Single Camera Support Only</h4>
                <p>The system is currently tested and designed for laptop webcam input only. Multiple camera feeds or CCTV camera integration is not yet implemented.</p>
            </div>

            <div class="limitation-card">
                <h4>🔄 No Threading or Parallel Processing</h4>
                <p>The application processes one camera feed at a time without multi-threading support. Concurrent camera handling is part of future development.</p>
            </div>

            <div class="limitation-card">
                <h4>🚫 Limited Testing Environment</h4>
                <p>Due to the unavailability of a second camera during development, multi-camera functionality and CCTV integration testing could not be performed. The system has been validated only with standard laptop webcams.</p>
            </div>

            <div class="info-box">
                💡 <strong>Note:</strong> These limitations are acknowledged and will be addressed in future versions of the system. See the Future Improvements section below for planned enhancements.
            </div>
        </div>

        <div class="section">
            <h2>🚀 Future Improvements</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">📹</div>
                    <h3>CCTV Integration</h3>
                    <p>Deploy system in real-time using CCTV camera footage with proper scaling and load balancing</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔄</div>
                    <h3>Multi-Threading Support</h3>
                    <p>Implement parallel processing to handle multiple camera feeds simultaneously</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3>Multiple Camera Handling</h3>
                    <p>Support for concurrent processing of multiple camera sources with thread-safe operations</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Scalable Architecture</h3>
                    <p>Design system to scale horizontally for large-scale deployments across multiple locations</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👁️</div>
                    <h3>Liveness Detection</h3>
                    <p>Prevent spoofing attacks using photo or video replay</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">☁️</div>
                    <h3>Cloud Deployment</h3>
                    <p>Deploy on AWS, Azure, or GCP with edge computing support</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔑</div>
                    <h3>Role-based Access Control</h3>
                    <p>Implement admin and user permission levels with secure authentication</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>Mobile Interface</h3>
                    <p>Responsive design for mobile devices and tablets</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <h3>Analytics Dashboard</h3>
                    <p>Comprehensive attendance analytics with visualization and reporting</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>👨‍💻 Author</h2>
            <div class="author-card">
                <div class="author-avatar">👨‍💻</div>
                <div>
                    <h3 style="color: white; margin: 0;">Muneer Ahmed</h3>
                    <p style="margin: 5px 0;">BS Computer Science (AI)</p>
                    <p style="margin: 5px 0;"><strong>Focus:</strong> Computer Vision, Deep Learning, Smart Surveillance Systems</p>
                </div>
            </div>
        </div>
    </div>

    <div class="scroll-top" onclick="scrollToTop()">↑</div>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function copyCommand(element) {
            const code = element.querySelector('code').innerText;
            navigator.clipboard.writeText(code).then(() => {
                const btn = element.querySelector('.copy-btn');
                btn.textContent = 'Copied!';
                setTimeout(() => {
                    btn.textContent = 'Copy';
                }, 2000);
            });
        }

        window.addEventListener('scroll', () => {
            const scrollTop = document.querySelector('.scroll-top');
            if (window.pageYOffset > 300) {
                scrollTop.classList.add('visible');
            } else {
                scrollTop.classList.remove('visible');
            }
        });

        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('click', function() {
                this.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 200);
            });
        });
    </script>
</body>
</html>
