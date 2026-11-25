import json
from pathlib import Path
from datetime import date

class StatisticsManager:
    def __init__(self):
        self.file_path = Path(__file__).resolve().parent.parent / "data" / "statistics.json"
        self.stats = self.load()

    def load(self):
        pass