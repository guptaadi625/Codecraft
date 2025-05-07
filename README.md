# 🚀 CodeCraft – Real-Time Online Code Compiler

**CodeCraft** is a modern, interactive, and secure real-time code compiler that supports **Python**, **C++**, and **Java**. Built with a beautiful and responsive frontend, CodeCraft features syntax highlighting, language-specific autosave, dark mode, and secure backend code execution powered by Docker.

---

## 🌟 Features

- ⚡ Real-time code execution for Python, C++, and Java
- 🎨 Sleek, responsive UI with dark mode toggle
- 💾 Auto-save code per language in local storage
- ⌨️ Run code with `Ctrl + Enter`
- 🔒 Secure backend execution with Docker containers
- 🌐 Frontend deployed on Vercel | Backend on Render

---

## 🔧 Tech Stack

| Layer     | Tech                             |
|-----------|----------------------------------|
| Frontend  | HTML, CSS, JavaScript, CodeMirror |
| Backend   | Python (Flask), Flask-CORS        |
| Execution | Docker (isolated language runners) |
| Deployment| Vercel (frontend), Render (backend) |

---

## 📂 Project Structure

CodeCraft/
├── backend/

│ ├── app.py

│ ├── requirements.txt
│ └── docker/
│ ├── python_executor/
│ │ └── Dockerfile
│ ├── cpp_executor/
│ │ └── Dockerfile
│ └── java_executor/
│ └── Dockerfile
├── index.html
├── style.css
└── script.js
└── README.md


---

## 🛠 Getting Started Locally

### 🔙 Backend

```bash
cd backend
pip install -r requirements.txt
python app.py

docker build -t python-runner ./docker/python_executor
docker build -t cpp-runner ./docker/cpp_executor
docker build -t java-runner ./docker/java_executor


cd frontend
# Open index.html in a browser OR deploy to Vercel
🌍 Live Demo


🙌 Author
Aditya Kumar Gupta


📜 License
This project is open-source and available under the MIT License.

