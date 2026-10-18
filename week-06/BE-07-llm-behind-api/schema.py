from enum import Enum
from pydantic import BaseModel, Field

class CategoryEnum(str, Enum):
    technical_support = "technical_support"
    billing = "billing"
    sales = "sales"
    security_incident = "security_incident"
    other = "other"

class UrgencyEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TeamEnum(str, Enum):
    support_tier_1 = "support_tier_1"
    support_tier_2 = "support_tier_2"
    finance = "finance"
    sales_reps = "sales_reps"
    security_ops = "security_ops"

class TriageInput(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="Customer message text to classify")

class TriageOutput(BaseModel):
    category: CategoryEnum = Field(..., description="Classified category")
    urgency: UrgencyEnum = Field(..., description="Urgency priority level")
    assigned_team: TeamEnum = Field(..., description="Target routing team")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model classification confidence")
    summary: str = Field(..., min_length=1, max_length=200, description="1-sentence clean summary")
    requires_escalation: bool = Field(..., description="Whether managerial escalation is triggered")

STUB_RESPONSE = {
    "category": "technical_support",
    "urgency": "medium",
    "assigned_team": "support_tier_1",
    "confidence": 0.95,
    "summary": "User requested assistance with database connection error.",
    "requires_escalation": False
}
