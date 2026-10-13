
@echo off
cd /d "D:\Data Analyst 2026\Automated Analytics Pipeline(Capstone -2)\Automated_Analytics_Pipeline"
call "venv\Scripts\activate.bat"
python main.py >> "logs\scheduler_output.log" 2>&1
