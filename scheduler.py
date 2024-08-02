import schedule
import time
import subprocess
import os

# Correct paths using raw strings
venv = r"C:/Users/dipak/Downloads/clg module/info retrival/assignment_coding/search_engine_project/venv/Scripts/activate"
file_path = r"C:/Users/dipak/Downloads/clg module/info retrival/assignment_coding/search_engine_project/search_engine/search_app/scrapping.py"

command = f"cmd /c \"{venv} & python {file_path}\""

schedule.every(1).minute.do(lambda: subprocess.run(command, shell=True))
# schedule.every().sunday.at("00:00").do(lambda: subprocess.run(command, shell=True))

while True:
    schedule.run_pending()
    # time.sleep(1)
