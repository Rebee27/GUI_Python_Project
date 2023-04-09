import os
from pathlib import Path


class MainModel:

    def __init__(self):
        self.user = os.path.basename(str(Path.home()))
