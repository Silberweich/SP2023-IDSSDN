from pathlib import PurePath, Path
import requests
import os

class RequestFileHandler():
    def __init__(self, MISP_API: str, MISP_API_TOKEN: str, RULES_PATH: str, RULES_TEMP_PATH: str):
        self.api = f"http://{MISP_API}/events/nids/suricata/download"
        self.token = MISP_API_TOKEN
        self.storage_path = Path(os.path.join(PurePath(RULES_PATH), "suricata-misp.rules"))
        self.temp_storage_path = Path(os.path.join(PurePath(RULES_TEMP_PATH), "suricata-misp.tmp.rules"))

        print(self.getParams())
        print(os.getcwd())

        self.file = open(self.storage_path, "w+", encoding="utf-8")
        self.temp = open(self.temp_storage_path, "w+", encoding="utf-8")

    def getParams(self) -> dict:
        return {k:v for k,v in self.__dict__.items()}
    
    def get_rules(self) -> bool:
        try:
            response = self.__req_rules()
            self.__write_rules(response)
            return True
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
        except Exception as e:
            print(">>>", e)
            return False
        
        self.file.flush().close()
        self.temp.flush().close()

        return True