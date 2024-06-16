
cd /D "%~dp0"
dir

START /B C:\Users\Z\Projects\work-sessions-server\.venv\Scripts\pythonw.exe -m bottle -b 0.0.0.0 main 1>stdout.txt 2>stderr.txt