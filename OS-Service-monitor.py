import psutil
import time
import SendMail
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]



def collect_workload():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

    return {
        'CPU': cpu_percent,
        'Memory': memory_percent,
        'Disk': disk_usage,
        'Network': network_usage
    }

def log_workload(workload):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    disk = workload["Disk"]
    cpu = workload["CPU"]
    memory = workload["Memory"]
    network = workload["Network"]
    return(f"Date-Time: {timestamp} \nCPU: {cpu}% \nDisk: {disk}% \nMemory: {memory}% \nNetwork usage: {network} bps \n")
 
      
def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    while True:
        workload = collect_workload()
        data = log_workload(workload)
        print(SendMail.gmail_send_message(creds, data))
        time.sleep(12*60*60) 

if __name__ == "__main__":
    main()
