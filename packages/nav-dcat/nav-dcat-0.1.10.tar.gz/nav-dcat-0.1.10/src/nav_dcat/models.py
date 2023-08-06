from typing import Optional, Sequence, Union, List
from datetime import date
from pydantic import BaseModel

from nav_dcat import doc_fields


class ESDocument(BaseModel):
    id: str
    title: str
    description: str
    type: doc_fields.Type
    uri: str
    format: Optional[Union[doc_fields.Type, List[doc_fields.Type]]]
    modified: Optional[str] = None
    issued: Optional[str] = None
    periodicity: Optional[str] = ""
    provenance: Optional[str] = "NAV"
    contactPoint: Optional[dict] = {}
    author: Optional[str] = ""
    repo: Optional[str] = ""
    readme: Optional[str] = ""
    spatial: Optional[str] = ""
    accessRights: Optional[doc_fields.AccessRights] = doc_fields.AccessRights.INTERNAL.value
    pii: Optional[doc_fields.Pii] = doc_fields.Pii.FALSE.value
    keyword: Optional[Sequence] = []
    theme: Optional[Union[str, List[str]]] = ""
    temporal: Optional[dict] = {"from": f"{date.today().year}", "to": f"{date.today().year}"}
    language: Optional[str] = "NO"
    creator: Optional[dict] = {}
    publisher: Optional[dict] = {"name": "NAV"}
    license: Optional[dict] = {}
    rights: Optional[str] = f"Copyright {date.today().year}, NAV"
    content: Optional[dict] = {}
    url: Optional[str] = ""
