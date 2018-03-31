class Config:
    def __init__(self, _dict = None):
        self.config = _dict if _dict is not None else {}

    def __getitem__(self,data):
        try:
            return self.config[data]
        except KeyError:
            return None