# CleanIT! — Superiority Trace Remover 🧼

**CleanIT!** (Superiority Cleaner v1.0) is a specialized Windows utility engineered to quickly and comprehensively wipe all traces, files, registry entries, and forensic footprints left behind by the "Superiority" software.

Unlike generic drive wipers, it targets only critical system paths and specific forensic artifacts, completing a deep cleaning process within 2–3 minutes without touching unrelated user data.

---

## ✨ Features & What It Cleans

* 📂 **File System Scan:** Searches and recursively deletes files/folders containing the "superiority" pattern in critical directories:
* %APPDATA% & %LOCALAPPDATA%
* %TEMP%
* %ProgramFiles% & %ProgramFiles(x86)%
* %ProgramData%
* User Documents, Downloads, and Desktop


* 🔑 **Windows Registry:** Completely removes software hives and Autorun persistence:
* HKCU\Software\Superiority
* HKLM\Software\Superiority
* HKCU\Software\Classes\superiority
* Removes the Superiority value from the CurrentVersion Run key.


* 💾 **USN Journal Evasions:** Purges the NTFS USN (Update Sequence Number) Journal across drives C: through G: to eliminate filesystem-level forensic logs.
* 📊 **Event Log Purging:** Automatically clears specific Windows Event Logs (System, Security, Application, and Microsoft-Windows-NTFS/Operational).

---

## 🚀 Getting Started

### Requirements

* OS: Windows 10 or Windows 11
* Environment: Python 3.6+ installed and added to your system PATH.
* Privileges: Administrator Rights (the script will automatically trigger a UAC prompt for elevation).

### Installation & Execution

#### Method 1: Git Clone (Recommended)

# Clone the repository

git clone [https://github.com/atlasru/cleanit-superiority.git](https://github.com/atlasru/cleanit-superiority.git)

# Navigate to the directory and run the tool

cd cleanit-superiority
python "cLeanIT!.py"

#### Method 2: Quick PowerShell Execution

Open PowerShell as an Administrator and execute the following wrapper:

$url = "[https://raw.githubusercontent.com/atlasru/cleanit-superiority/main/cLeanIT!.py](https://raw.githubusercontent.com/atlasru/cleanit-superiority/main/cLeanIT!.py)"
$out = "$env:TEMP\cLeanIT!.py"
Invoke-WebRequest -Uri $url -OutFile $out
python $out

---

## ❓ Troubleshooting

* **"Python is not recognized as an internal or external command"**
* Fix: Download Python from python.org and make sure to check the box that says "Add Python to PATH" during installation.


* **Registry Keys or Files Access Denied**
* Fix: The script requests Admin rights automatically, but if it gets blocked, explicitly open your Command Prompt/PowerShell as Administrator and run the script from there.


* **USN Journal Error / Failure Messages**
* Note: This is completely normal if a targeted drive letter (e.g., E:, F:, G:) does not exist on your computer or uses a non-NTFS filesystem.



---

## 📜 Credits & License

* Developer: Recoded and ported to modern Windows Python environments by d9vh.
* Original Concept: Inspired by an original idea by sxbni. (https://github.com/funloverru)
* License: Free for any use. Provided "as-is" without explicit warranties.
