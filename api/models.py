"""
데이터 모델 정의
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class BurnedPixel(BaseModel):
    """연소된 픽셀 정보"""
    row: int
    col: int
    lat: Optional[float] = None
    lon: Optional[float] = None

class FireSpreadResponse(BaseModel):
    """화재 확산 응답 데이터"""
    time_minutes: int
    total_burned_pixels: int
    burned_coordinates: List[BurnedPixel]
    ignition_point: Dict[str, int]
    metadata: Dict[str, Any]

class AvailableSimulations(BaseModel):
    """사용 가능한 시뮬레이션 목록"""
    simulations: List[str]
    description: str

class ServerStatus(BaseModel):
    """서버 상태 정보"""
    message: str
    status: str
    version: str
    korean_forest_data: str
    time_intervals: str
    endpoints: List[str]
