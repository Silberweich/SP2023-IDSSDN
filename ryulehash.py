import hashlib
from pathlib import Path
import requests
import syslog
import dotenv
import os

## Use with cron "*/1 * * * * /path/to/ryuhash.py"

if __name__ == "__main__":

    # Load environment variables
    dotenv.load_dotenv()
    # Create a hash of the rules file
    h = hashlib.sha256()
    # Create hash file if not exists
    Path("/etc/ryuhash/rules.hash").mkdir(parents=True, exist_ok=True)

    header = {"Authorization": os.getenv('MISP_API_TOKEN'),
              "Accept": "*/*",
              "Accept-Encoding": "gzip, deflate",
              "Connection": "keep-alive",
              "Content-Type": "application/json",
              "User-Agent": "python-requests/2.25.1"}
    try:
        with requests.get(f"http://{os.getenv('MISP_API')}/events/nids/suricata/download", header = header, verify=False) as response:
            h.update(response.text.encode('utf-8')) 
            print(h.hexdigest())

            # Compare the hash with the previous hash
            with open("/etc/ryuhash/rules.hash", "rb", encoding="utf-8") as f:
                if f.read() == h.hexdigest().encode('utf-8'):
                    syslog.syslog(syslog.LOG_INFO, "Ryu Hash Check: No changes in the rules file")
                else:
                    syslog.syslog(syslog.LOG_INFO, "Ryu Hash Check: Changes in the rules file, informing suricata...")
                    # Inform Suricata about the changes
                    for i in os.getenv("SURICATA-ADDRESSES").split(":"):
                        requests.get(f"http://{i}/fetch-rules", verify=False)
                    # Write the new hash to the file
                    with open("/etc/ryuhash/rules.hash", "w", encoding="utf-8") as f:
                        f.write(h.hexdigest())
                        f.flush()
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Ryu Hash Check Error: {e}")