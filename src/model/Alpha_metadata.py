import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class Params:
    from_date: str
    to_date: str
    product: str
    product_detail: str
    level: str
    user: str
    
    def to_dict(self) -> Dict[str, str]:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class AlphaMetadata:
    user_id: str
    is_new_session: bool
    is_action: bool
    endpoint: str
    params: Optional[Params]
    response: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "is_new_session": self.is_new_session,
            "is_action": self.is_action,
            "endpoint": self.endpoint,
            "params": self.params.to_dict() if self.params is not None else None,
            "response": self.response,
        }
