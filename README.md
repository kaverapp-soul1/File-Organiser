
---

# 📁 File-Organiser

**Streamlit-based prototype application for organizing and managing files and folders on your local system.**

---

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Organize files by type, size, age, and more
- Detect and manage duplicate files
- Generate detailed disk usage and file distribution reports
- Interactive Streamlit UI for easy operation
- Security features: file integrity checks and optional encryption
- Customizable file categories and rules
- Export organization reports and visualize with charts

---

## Screenshots

<!-- Add screenshots here -->
<p align="center">
  <img src="screenshots/main_ui.png" width="600"/>
  <img src="screenshots/report_example.png" width="600"/>
</p>

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kaverapp-soul1/File-Organiser.git
   cd File-Organiser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or use Docker:
   ```bash
   docker build -t file-organiser .
   docker run -p 8501:8501 file-organiser
   ```

---

## Usage

1. **Run with Streamlit**
   ```bash
   streamlit run server.py
   ```

2. **Access the web UI**
   - Open your browser and go to [http://localhost:8501](http://localhost:8501)

3. **Organize your files**
   - Select the directory
   - Choose organization options
   - View reports and visualizations

---

## Configuration

- Adjust file categories and rules in `app/config/FileOrganiserConfig.py`
- Log files are stored in the `logs/` directory
- Security and encryption options are managed via `app/core/SecurityManager.py`

---

## Project Structure

```
file_organiser/
│
├── app/
│   ├── config/                # Configuration files
│   ├── core/                  # Core logic (utils, logging, analysis, security)
│   ├── interface/             # Streamlit UI interface
│   └── __init__.py
├── logs/                      # Log files
├── scripts/                   # Main organizing script
├── server.py                  # Streamlit entry point
├── Dockerfile
├── requirements.txt
├── README.md
```

---

## Development

- Code style: [PEP8](https://pep8.org/)
- Please add docstrings and type annotations to new code.
- Run linting before committing:
  ```bash
  flake8 .
  black .
  ```

- To run tests (if available):
  ```bash
  pytest
  ```

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and how to get started.

---

## License

[MIT License](LICENSE)

---




