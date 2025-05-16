import subprocess
import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend calls

@app.route('/')
def home():
    return "Code Compiler API is running."

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')

    try:
        if language == 'python':
            return run_python(code)
        elif language == 'cpp':
            return run_cpp(code)
        elif language == 'java':
            return run_java(code)
        else:
            return jsonify({'output': 'Unsupported language'}), 400
    except Exception as e:
        return jsonify({'output': f'Error: {str(e)}'}), 500

# -------------------------------
# Execution Functions (no Docker)
# -------------------------------

def run_python(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
        temp.write(code.encode())
        temp.flush()

        result = subprocess.run(
            ['python3', temp.name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )

    os.unlink(temp.name)
    return jsonify({'output': result.stdout if result.returncode == 0 else result.stderr})

def run_cpp(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as source:
        source.write(code.encode())
        source.flush()

        output_file = source.name + ".out"

        compile_result = subprocess.run(
            ['g++', source.name, '-o', output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if compile_result.returncode != 0:
            os.unlink(source.name)
            return jsonify({'output': compile_result.stderr})

        run_result = subprocess.run(
            [output_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )

        os.unlink(source.name)
        os.unlink(output_file)

        return jsonify({'output': run_result.stdout if run_result.returncode == 0 else run_result.stderr})

def run_java(code):
    with tempfile.TemporaryDirectory() as temp_dir:
        source_path = os.path.join(temp_dir, "Main.java")
        with open(source_path, "w") as f:
            f.write(code)

        compile_result = subprocess.run(
            ['javac', source_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if compile_result.returncode != 0:
            return jsonify({'output': compile_result.stderr})

        run_result = subprocess.run(
            ['java', '-cp', temp_dir, 'Main'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )

        return jsonify({'output': run_result.stdout if run_result.returncode == 0 else run_result.stderr})

# -----------------------------

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
