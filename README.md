# 🐚 pyAlx  "Custom Python Shell"

A lightweight, feature-rich shell implemented in Python, designed to mimic the functionality of traditional Unix shells like `bash` or `zsh`, with additional advanced features and a GUI interface.

## 🌟 Features Implemented So Far

### 🔧 Core Functionalities
1. **Command Execution**:
   - Execute system commands like `ls`, `pwd`, `echo`, and more.
   - Supports commands with arguments (e.g., `ls -l /home`).
   
2. **I/O Redirection**:
   - **Output redirection**: `command > file.txt`
   - **Input redirection**: `command < file.txt`
   - **Append mode**: `command >> file.txt`
   - **Error redirection**: `command 2> error.log`

3. **Pipe Support**:
   - Chain multiple commands using `|` (e.g., `ls | grep .py`).

4. **Process Management**:
   - Run commands in the background using `&` (e.g., `sleep 5 &`).
   - Track and manage background processes.

5. **Built-in Commands**:
   - `cd`: Change directories.
   - `pwd`: Print the current working directory.
   - `ls`: List files in the directory.
   - `echo`: Print text to the terminal or redirect output to a file.
   - `history`: View previously entered commands.
   - `exit`: Quit the shell.

6. **Command History**:
   - View and reuse previously entered commands.

---

### 🎨 Terminal Interface Features
1. **Custom Prompt**:
   - Displays user info, hostname, and the current working directory.
   - Example: `[user@host:/home]$`

2. **Dark Theme**:
   - Aesthetic and user-friendly terminal appearance.

3. **Color Support**:
   - Uses ANSI color codes for syntax highlighting and UI customization:
     ```python
     ANSI_COLORS = {
       '30': '#000000',  # Black
       '31': '#FF0000',  # Red
       '32': '#00FF00',  # Green
       '33': '#FFFF00',  # Yellow
       '34': '#0000FF',  # Blue
       '35': '#FF00FF',  # Magenta
       '36': '#00FFFF',  # Cyan
       '37': '#FFFFFF',  # White
     }
     ```

4. **Scrollable Output**:
   - Allows viewing extensive outputs from commands.

---

### 🖥️ GUI Mode (In Progress)
1. **Command Input Area**:
   - A text box for entering shell commands.
   
2. **Output Display**:
   - Scrollable area to view command outputs.
   
3. **Status Bar**:
   - Displays process status and shell information.

4. **Syntax Highlighting**:
   - Highlight keywords, commands, and errors for better visibility.

---

## 🚀 Usage Guide

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Ali-Beg/pyAlx.git
   cd pyAlx
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Shell
- **CLI Mode**:
  ```bash
  python main.py
  ```
- **GUI Mode**:
  ```bash
  python main.py --gui
  ```

### Basic Commands
| Command           | Description                                  |
|-------------------|----------------------------------------------|
| `cd /path/to/dir` | Navigate to the specified directory.         |
| `pwd`             | Print the current working directory.         |
| `ls`              | List files in the current directory.         |
| `echo "text"`     | Print text to the console or a file.          |
| `command > file`  | Redirect command output to a file.           |
| `command &`       | Run a command in the background.             |
| `history`         | View previously entered commands.            |
| `exit`            | Exit the shell.                              |

---

## 🛠️ Advanced Features
1. **Pipelines**:
   - Chain commands using pipes (`|`), e.g., `ls | grep .py`.
   
2. **Error Handling**:
   - Redirect errors to a file using `2>`, e.g., `command 2> error.log`.
   
3. **Background Processing**:
   - Run processes in the background with `&`.

---

## 🧪 Testing
1. Run all tests:
   ```bash
   pytest tests/ -v
   ```
2. Check code coverage:
   ```bash
   pytest tests/ --cov=src
   ```

---

## 🐞 Known Issues
1. GUI text selection is limited.
2. History navigation has edge cases.
3. Handling complex pipe chains is still under development.

---

## 📈 Future Enhancements
- Command aliases (e.g., `ll` for `ls -l`).
- Shell scripting capabilities.
- Auto-suggestions for commands and arguments.
- Multi-tab GUI for running parallel sessions.
- Plugin system for extensibility.
- Configuration files for customization.

---

## 🤝 Contributing Guidelines
1. **Fork the repository**:  
   ```bash
   git clone https://github.com/Ali-Beg/pyAlx.git
   ```
2. **Create a feature branch**:  
```bash
git checkout -b feature-name
```
3. **Follow code style guidelines** and write tests for new features.
4. Submit a **pull request** with detailed explanations.

---

## 📋 License
This project is open-source under the [MIT License](LICENSE).

---

## 👨‍💻 Author
**Your Name**  
Contact: [mber937@gmail.com](mbeg937@gmail.com)

Feel free to reach out for suggestions, feedback, or contributions!

---

## ⭐ Acknowledgments
Special thanks to all contributors and the open-source community for inspiration and support!

