from typing import List, Dict, Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    # 'Field' provides additional information like descriptions and rules for the variables
    # The 'description' of the 'Field' helps the llm to identify which is supposed to be the 'summary' and
    # which are supposed to be the 'facts'

    # In 'output_parser', we are using the llm only to identify which is 'summary' and which are 'facts' and everything else within 'output_parser' is programming logic.

    def to_dict(self) -> Dict[str, Any]:
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)