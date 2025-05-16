import subprocess
import tempfile
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend requests (CORS)

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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
                temp.write(code.encode('utf-8'))
                temp.flush()

                result = subprocess.run(
                    [
                        'docker', 'run', '--rm',
                        '-v', f"{temp.name}:/app/run_code.py:ro",
                        '--network', 'none',
                        '--memory', '100m',
                        '--cpus', '0.5',
                        'python-runner'
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )

            os.unlink(temp.name)

        elif language == 'cpp':
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as temp:
                temp.write(code.encode('utf-8'))
                temp.flush()

                result = subprocess.run(
                    [
                        'docker', 'run', '--rm',
                        '-v', f"{temp.name}:/app/main.cpp:ro",
                        '--network', 'none',
                        '--memory', '200m',
                        '--cpus', '0.5',
                        'cpp-runner'
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )

            os.unlink(temp.name)

        elif language == 'java':
            with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as temp:
                temp.write(code.encode('utf-8'))
                temp.flush()

                result = subprocess.run(
                    [
                        'docker', 'run', '--rm',
                        '-v', f"{temp.name}:/app/Main.java:ro",
                        '--network', 'none',
                        '--memory', '200m',
                        '--cpus', '0.5',
                        'java-runner'
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )

            os.unlink(temp.name)

        else:
            return jsonify({
                'language': language,
                'output': 'Unsupported language.'
            })

        return jsonify({
            'language': language,
            'output': result.stdout if result.returncode == 0 else result.stderr
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            'language': language,
            'output': 'Error: Code execution timed out.'
        })

    except Exception as e:
        return jsonify({
            'language': language,
            'output': f'Error: {str(e)}'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
