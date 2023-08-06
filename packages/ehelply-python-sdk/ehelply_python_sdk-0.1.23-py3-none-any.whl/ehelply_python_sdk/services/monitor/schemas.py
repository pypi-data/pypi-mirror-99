from ehelply_python_sdk.services.service_schemas import *


class GetProjectResponse(HTTPResponse):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool


class UpdateProject(BaseModel):
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth


class UpdateProjectResponse(HTTPResponse):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool
    group_m_p: str  # Group UUID that joins members to partition/project
    group_p_c: str  # Group UUID that joins partition/project to eHelply Cloud


class SearchProjectItem(BaseModel):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool


class UsageTypeUnitPrice(BaseModel):
    min_quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth
    max_quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth
    unit_price: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth


class SearchUsageTypeItem(BaseModel):
    key: str
    name: str
    summary: str
    category: str
    service: str
    unit_prices: List[UsageTypeUnitPrice]


class GetUsageResponse(HTTPResponse):
    usage: List[SearchUsageTypeItem]

    def __init__(self, *args, **data: Any) -> None:
        usage: List[SearchUsageTypeItem] = []

        for arg_usage in args:
            usage.append(SearchUsageTypeItem(**arg_usage))

        super().__init__(*args, **data, usage=usage)
