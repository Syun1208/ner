from typing import Dict
import dataclasses

@dataclasses.dataclass
class AlphaMetadata:
    user_id: str
    is_new_session: bool
    is_action: bool
    endpoint: str
    params: Dict
    response: str

    