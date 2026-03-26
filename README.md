# TSG-CLI (Telegram Storage CLI)

A powerful CLI tool that transforms Telegram Saved Messages into a personal cloud storage system, providing a robust virtual file system entirely within Telegram.

---

## Features

**Virtual Folder System**
* **Path-based structure:** Implements a true virtual file system using absolute paths (e.g., `/anime/naruto/`, `/docs/work/`).
* **Folder creation:** `mkdir` command to initialize new virtual directories.
* **File organization:** `move` command to reliably shift files between virtual directories.
* **Direct upload:** Target specific directories on upload using the `--path` argument.
* **Navigation:** `ls` command to list contents of specific virtual directories.

**Upload System**
* Supports single file, batch file, and recursive folder uploads.
* Accept mixed input streams (files and directories simultaneously).
* Target specific virtual paths directly using `--path`.

**Download System**
* Single and batch downloading capabilities.
* Safe handling of large files.
* Built-in resume support with checkpoints.
* Automated retry logic for network instability.

**Metadata System**
* Apply tags for secondary grouping and categorization.
* Support for custom file renaming during upload.
* Local metadata tracking stored in `~/.tsg-cli/metadata.json`.

**Search System**
* Name-based search queries.
* Robust filtering by tags and file types.
* Clean, paginated results with sorting capabilities.

**CLI UX**
* Clean, structured table outputs for lists and searches.
* Real-time progress bars with upload/download speeds.
* Clear, structured success and error messaging.

**Backup & Restore**
* Securely backup the local metadata state (`metadata.json`) directly to Telegram.
* Seamlessly restore your file structure from Telegram backups to any new machine.

---

## Installation

### Prerequisites

You will need Python 3.9+ and your Telegram API credentials.

1. Go to [my.telegram.org](https://my.telegram.org) and log in.
2. Navigate to "API development tools" and fill out the form to create an application.
3. Save your `API_ID` and `API_HASH`.

### Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd tsg-cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your credentials when running the tool for the first time. The CLI will prompt you for your `API_ID`, `API_HASH`, and phone number to authenticate your Telegram session.

---

## Usage

Interact with the CLI by executing `main.py`.

### Virtual Folder Examples

**Create a new virtual folder:**
```bash
python main.py mkdir /documents/work
```

**Upload directly to a virtual folder:**
```bash
python main.py upload report.pdf --path /documents/work/
```

**List folder contents:**
```bash
python main.py ls /documents/work/
```

**Move an existing file into a folder:**
```bash
python main.py move file_id_123 /documents/archive/
```

### General Usage Examples

**Upload a single file with tags:**
```bash
python main.py upload my_video.mp4 --tags "video, holiday"
```

**Upload an entire local directory:**
```bash
python main.py upload ./my_photos/
```

**Search files by name:**
```bash
python main.py search "report"
```

**Download a file:**
```bash
python main.py download file_id_123
```

**Backup your metadata to Telegram:**
```bash
python main.py backup
```

**Restore metadata from Telegram:**
```bash
python main.py restore
```

---

## Architecture

TSG-CLI is designed with a robust, local-first architecture built entirely around the Telegram API, requiring no external databases.

* **CLI Layer:** Built with Typer for a clean, developer-friendly interface and input parsing.
* **Service Layer:** Handles core business logic, metadata parsing, and virtual path mapping.
* **Utils Layer:** Provides shared utilities for formatting, progress bars, and filesystem interactions.
* **Telegram Client Abstraction:** Manages the underlying connection and data transfer using Telethon/Pyrogram, abstracting the complexity of the MTProto protocol.

---

## Reliability

Designed to handle unreliable networks and massive files gracefully.

* **Retry Logic:** Automatic backoff and retry mechanisms for API rate limits and connection drops.
* **Resume Support:** Downloads can be safely paused and resumed.
* **Safe Interruption:** Gracefully handles `Ctrl+C` (SIGINT) to ensure metadata corruption is prevented.
* **Checkpoint System:** Chunked uploads and downloads track progress to avoid restarting large transfers from zero.

---

## Limitations

* **File Size Limits:** Bound by standard Telegram limitations (2GB for standard users, 4GB for Telegram Premium).
* **Manual Operation:** All uploads must be initiated manually via the CLI; it does not currently support automated folder syncing (e.g., watching a local folder for changes).

---

## Status

**Production-ready CLI (actively evolving)**

The core systems are stable and ready for daily use, but the project is under active development. Expect regular updates and new features.

---

## Contributing

Pull Requests are welcome! If you encounter an issue or have a feature request, please open an issue on the repository.

---

## License

This project is licensed under the MIT License.
