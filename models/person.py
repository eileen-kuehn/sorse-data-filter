from dataclasses import dataclass
from typing import Optional, Dict, List

from models import FilteredModel
from models.affiliation import search_matching_affiliation, Affiliation
from utils import search_matching_orcid, to_bool, to_str


@dataclass
class Person(FilteredModel):
    address: str
    affiliation_id: Optional[int]
    author_type:  str
    first_name: str
    last_name: str
    is_speaker: bool
    title: str
    orcid: Optional[str]
    email: str

    @classmethod
    def from_json(cls, allow_list, json_content, orcids: Dict[str, Dict],
                  affiliations: List[Affiliation], email_agreement=False, contact_email=None):
        first_name = json_content["first_name"]
        last_name = json_content["last_name"]
        orcid_id = search_matching_orcid(first_name, last_name, orcids)
        affiliation_id = search_matching_affiliation(to_str(json_content["affiliation"]), affiliations)
        email = None
        if email_agreement:
            parsed_email = to_str(json_content["email"])
            if parsed_email is not None and parsed_email.lower() == contact_email.lower():
                email = contact_email
        return Person(
            allow_list=allow_list,
            first_name=to_str(json_content["first_name"]),
            last_name=to_str(json_content["last_name"]),
            affiliation_id=affiliation_id,
            address=to_str(json_content["address"]),
            author_type=json_content["author_type"],
            is_speaker=to_bool(json_content["is_speaker"]),
            title=to_str(json_content["title"]),
            orcid=orcid_id,
            email=email,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(address='{self.address}', " \
               f"affiliation_id='{self.affiliation_id}', author_type='{self.author_type}', " \
               f"first_name='{self.first_name}', last_name='{self.last_name}', " \
               f"is_speaker='{self.is_speaker}', title='{self.title}', " \
               f"orcid='{self.orcid}')"
