from static import AIOGRAM_CONFIG
from rich import print
import os
import json

class ConfigParser:
    def __init__(self):
        path = os.path.join(AIOGRAM_CONFIG)
        if not os.path.exists(path):
            path = os.path.join("..", path)
            
        if not os.path.exists(path):
            print(f"[bold red] Config file does not exists [{AIOGRAM_CONFIG}][\bold red]")
            exit(0)
        
        with open(path, "r", encoding='utf-8') as read_stream:
            data = read_stream.read()
            
        try:
            self.data = json.loads(data)
        except:
            print(f"[bold red] Config file has critical syntax errors [{AIOGRAM_CONFIG}][\bold red]")
            exit(0)
            return
        
    @property
    def token(self):
        return self.data['TOKEN']