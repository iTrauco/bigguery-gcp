import subprocess
import schedule
import time

def check_dependencies():
    print("Checking for outdated dependencies...")
    result = subprocess.run(['pip', 'list', '--outdated'], capture_output=True, text=True)
    if result.stdout:
        print("Outdated packages:")
        print(result.stdout)
    else:
        print("All packages are up to date.")

if __name__ == "__main__":
    schedule.every().day.at("09:00").do(check_dependencies)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
