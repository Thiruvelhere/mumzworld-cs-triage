from pydantic import BaseModel, field_validator
from typing import Literal, Optional

class TriageResult(BaseModel):
    intent: Literal['refund', 'exchange', 'store_credit', 'escalate', 'other']
    urgency: Literal['low', 'medium', 'high']
    confidence: Optional[float]   # null = model is uncertain
    reasoning: str                # one sentence, always present
    reply_en: Optional[str]       # null if out_of_scope=True
    reply_ar: Optional[str]       # null if out_of_scope=True, Gulf Arabic
    out_of_scope: bool

    @field_validator('confidence')
    def confidence_range(cls, v):
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError('confidence must be 0.0 to 1.0')
        return v
