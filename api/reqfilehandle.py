from pathlib import PurePath, Path
from typing import List
import requests
import os
import subprocess, re


class RequestFileHandler():
    def __init__(self, MISP_API: str, MISP_API_TOKEN: str, RULES_PATH: str, RULES_TEMP_PATH: str):
        self.api = f"http://{MISP_API}/events/nids/suricata/download"
        self.token = MISP_API_TOKEN
        self.storage_path = Path(os.path.join(PurePath(RULES_PATH), "suricata-misp.rules"))
        self.temp_storage_path = Path(os.path.join(PurePath(RULES_TEMP_PATH), "suricata-misp.tmp.rules"))

        print(">>>", self.getParams())
        print(">>>", os.getcwd())

        # Path(self.storage_path).mkdir(parents=True, exist_ok=True)
        # Path(self.temp_storage_path).mkdir(parents=True, exist_ok=True)

        self.file = open(self.storage_path, "w+", encoding="utf-8")
        self.temp = open(self.temp_storage_path, "w+", encoding="utf-8")

    def getParams(self) -> dict:
        return {k:v for k,v in self.__dict__.items()}
    
    def get_rules(self) -> bool:
        try:
            response = self.__req_rules()
            self.__write_rules(response)
            return self.__verify_rules() and self.__reload_rules()
        except Exception as e:
            print(">>>", e)
            return False 

    def __req_rules(self) -> requests.request:
        header = {"Authorization": self.token,
              "Accept": "*/*",
              "Accept-Encoding": "gzip, deflate",
              "Connection": "keep-alive",
              "Content-Type": "application/json",
              "User-Agent": "python-requests/2.25.1"}

        return requests.get(self.api, headers=header, verify=False)

    def __write_rules(self, response: requests.request) -> bool:
        try:
            self.file.write(response.text)
            self.temp.write(response.text)

            self.file.flush()
            self.temp.flush()
        except Exception as e:
            print(">>>", e)
            return False

        return True
    
    def __reload_rules(self) -> bool:
        cmd = ['kill', "-USR2", "$(pidof suricata)"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()

        if e:
            print(">>>", e)
            return False

        return True
    
    def __filter_rules(self, line: str, signatures: List[any]) -> bool:
        # Check if the line contains 8 or more consecutive spaces
        if re.search(r' {8,}', line):
            return False
        for signature in signatures:
            if signature in line:
                return False
        return True
    
    def __verify_rules(self) -> bool:
        error_pattern = r'Error: detect.*parsing signature "([^"]*)"'
        error_messages, filtered_lines = None, None
        cmd = ['suricata', '-T', '-c', '/etc/suricata/suricata.yaml', '-v']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            o, e = proc.communicate()
            suricata_errors = e.decode('utf-8')

            with open('rules_error.txt', 'w') as f:
                f.write(suricata_errors)

            with open('rules_error.txt', 'w') as f:
                error_messages = f.read()

            signatures = re.findall(error_pattern, error_messages)

            with open('suricata.rules', 'r') as f:
                lines = f.readlines()
                filtered_lines = filter(self.__filter_rules, lines, signatures)
            
            with open('cleaned.rules', 'w') as f:
                f.writelines(filtered_lines)
        
        except Exception as e:
            print(">>>", e)
            return False

        return True
    