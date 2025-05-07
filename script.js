// Initialize CodeMirror editor
let editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: "python",
    theme: "default"
});

const languageDropdown = document.getElementById('language');
const runButton = document.getElementById('run-btn');
const toggleBtn = document.getElementById('theme-toggle');
let darkMode = false;

// Load saved code on page load
window.addEventListener('DOMContentLoaded', () => {
    const lang = languageDropdown.value;
    const savedCode = localStorage.getItem(lang) || '';
    editor.setValue(savedCode);
});

// Save code as user types
editor.on("change", () => {
    const lang = languageDropdown.value;
    localStorage.setItem(lang, editor.getValue());
});

// Helper to get language key from CodeMirror mode
function getLangKeyFromMode(mode) {
    switch (mode) {
        case 'text/x-c++src': return 'cpp';
        case 'text/x-java': return 'java';
        case 'python': return 'python';
        default: return 'python';
    }
}

// Change language and load corresponding code
languageDropdown.addEventListener('change', function () {
    // Save current code
    const currentLang = editor.getOption('mode');
    const langKey = getLangKeyFromMode(currentLang);
    localStorage.setItem(langKey, editor.getValue());

    // Switch to new language mode
    const lang = this.value;
    let mode = 'python';
    if (lang === 'cpp') mode = 'text/x-c++src';
    if (lang === 'java') mode = 'text/x-java';
    editor.setOption("mode", mode);

    // Load saved code
    const newCode = localStorage.getItem(lang) || '';
    editor.setValue(newCode);
});

// Run code function
function runCode() {
    const language = languageDropdown.value;
    const code = editor.getValue();

    fetch('http://127.0.0.1:5000/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language, code })
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById('result').textContent = result.output;
    })
    .catch(err => {
        document.getElementById('result').textContent = 'Request failed: ' + err;
    });
}

// Run code on button click
runButton.addEventListener('click', runCode);

// Dark mode toggle
toggleBtn.addEventListener('click', () => {
    darkMode = !darkMode;
    document.body.classList.toggle('dark-mode');
    editor.setOption('theme', darkMode ? 'dracula' : 'default');
    toggleBtn.textContent = darkMode ? '☀️ Light Mode' : '🌙 Dark Mode';
});

// Run code on Ctrl + Enter
editor.addKeyMap({
    'Ctrl-Enter': () => {
        runCode();
    }
});
