import schedule
import time
from crypto import export_to_csv  # Change 'your_main_module'!

def job():
    export_to_csv()

schedule.every().day.at("00:00").do(job)

if __name__ == "__main__":
    print("Scheduler started. Web scraping will run daily at 00:00.")
    while True:
        schedule.run_pending()  # Check if it's time to run the job
        time.sleep(60)          # Wait a minute