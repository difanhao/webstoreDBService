from typing import Dict

class VipUser:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)

    def to_dict(self):
        return self.__dict__