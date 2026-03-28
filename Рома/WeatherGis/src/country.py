from typing import Dict, Any


class Country:   
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name
    
    def to_dict(self) -> Dict[str, Any]:
        return {'code': self.code, 'name': self.name}
