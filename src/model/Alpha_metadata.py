import dataclasses

@dataclasses.dataclass
class Params:
    from_date: str
    to_date: str
    product: str
    product_detail: str
    level: str
    user: str
    
@dataclasses.dataclass
class AlphaMetadata:
    user_id: str
    is_new_session: bool
    is_action: bool
    endpoint: str
    params: Params
    response: str