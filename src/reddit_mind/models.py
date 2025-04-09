from pydantic import BaseModel
from typing import List, Optional

class Summary(BaseModel):
	summary: str
	rating: str
	pros: str
	cons: str


class FeatureSummary(BaseModel):
    feature_name: str
    summary: str

class FeatureExtractionResult(BaseModel):
    features: List[FeatureSummary]

class CompetitorComparison(BaseModel):
    name: str
    differences: str

class CompetitorAnalysis(BaseModel):
    competitors: List[CompetitorComparison]


class TimeSegment(BaseModel):
    """
    Represents a single time segment (e.g., a month, week, or
    any time bucket), including volume, sentiment, and key points.
    """
    period: str

    volume: int

    sentiment: Optional[str] = None


    highlights: Optional[str] = None


class TimelineAnalysis(BaseModel):
    """
    A structured timeline analysis of how discussions evolve over time.
    """
    timeline: List[TimeSegment]

    overall_trend_summary: str


    significant_peaks: Optional[str] = None
