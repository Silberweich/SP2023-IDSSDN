import hashlib
from pathlib import Path
import requests
import syslog
import dotenv
import os

HASH_LOC = "/etc/ryuhash/rules.hash"
HASH_DIR = "/etc/ryuhash/"

## Use with cron "*/1 * * * * /path/to/ryuhash.py"
## .env format
# MISP_API =
# MISP_API_TOKEN = 
# SURICATA-ADDRESSES = 192.168.0.1:192.168.0.2:...

# rb for read only, wb+ for creating new file if not exists
def rule_hash_write(mode:str, h:hashlib.sha256) -> bool:
    with open("/etc/ryuhash/rules.hash", mode) as f:
        if f.read() == h.hexdigest().encode('utf-8'):
            syslog.syslog(syslog.LOG_INFO, "Ryu Hash Check: No changes in the rules file")
        else:
            syslog.syslog(syslog.LOG_INFO, "Ryu Hash Check: Changes in the rules file, informing suricata...")
            # Inform Suricata about the changes
            for i in os.getenv("SURICATA-ADDRESSES").split(":"):
                print(f"http://{i}:8080/fetch-rules")
                requests.get(f"http://{i}:8080/fetch-rules", verify=False)
            # Write the new hash to the file
            with open("/etc/ryuhash/rules.hash", "w", encoding="utf-8") as f:
                f.write(h.hexdigest())
                f.flush()

if __name__ == "__main__":
    # Load environment variables
    dotenv.load_dotenv()
    # Create a hash of the rules file
    h = hashlib.sha256()
    # Create hash file if not exists
    Path(HASH_DIR).mkdir(parents=True, exist_ok=True)

    header = {"Authorization": os.getenv('MISP_API_TOKEN'),
              "Accept": "*/*",
              "Accept-Encoding": "gzip, deflate",
              "Connection": "keep-alive",
              "Content-Type": "application/json",
              "User-Agent": "python-requests/2.25.1"}
    try:
        with requests.get(f"http://{os.getenv('MISP_API')}/events/nids/suricata/download", headers=header, verify=False) as response:
            h.update(response.text.encode('utf-8')) 
            print(">>>", h.hexdigest())
            if Path(HASH_LOC).exists():
                rule_hash_write("rb", h)
            else:
                rule_hash_write("wb+", h)

    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Ryu Hash Check Error: {e}")