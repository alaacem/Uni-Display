import subprocess
import time

def start_scraper():
    process = subprocess.Popen(["python", "scrapping.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def stop_scraper(process):
    process.terminate()
    process.wait()

if __name__=='__main__':
    scraper_process = start_scraper()