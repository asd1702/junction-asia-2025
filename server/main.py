"""
Cell2Fire Korean Forest Demo API - 한국 산림 화재 확산 시뮬레이션 데모 API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.models import FireSpreadResponse, AvailableSimulations, ServerStatus
from api.endpoints import FireSpreadAPI

# FastAPI 앱 초기화
app = FastAPI(
    title="Cell2Fire Korean Forest Demo",
    description="한국 동네 산 화재 확산 시뮬레이션 데모 API (2km x 2km, 50m 해상도)",
    version="1.0.0"
)

# CORS 설정 (프론트엔드에서 접근 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시에는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== 기본 엔드포인트 ==============

@app.get("/", response_model=ServerStatus)
async def root():
    """API 서버 상태 확인"""
    return await FireSpreadAPI.get_server_status()

@app.get("/simulations", response_model=AvailableSimulations)
async def get_available_simulations():
    """사용 가능한 시뮬레이션 목록 반환"""
    return await FireSpreadAPI.get_available_simulations()

# ============== 한국 산림 데모 API ==============

@app.get("/korean-fire-spread/0", response_model=FireSpreadResponse)
async def get_korean_0min():
    """한국 산림 - 발화 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(0)

@app.get("/korean-fire-spread/30", response_model=FireSpreadResponse)
async def get_korean_30min():
    """한국 산림 - 발화 후 30분 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(30)

@app.get("/korean-fire-spread/60", response_model=FireSpreadResponse)
async def get_korean_60min():
    """한국 산림 - 발화 후 1시간 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(60)

@app.get("/korean-fire-spread/90", response_model=FireSpreadResponse)
async def get_korean_90min():
    """한국 산림 - 발화 후 1시간 30분 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(90)

@app.get("/korean-fire-spread/120", response_model=FireSpreadResponse)
async def get_korean_120min():
    """한국 산림 - 발화 후 2시간 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(120)

@app.get("/korean-fire-spread/150", response_model=FireSpreadResponse)
async def get_korean_150min():
    """한국 산림 - 발화 후 2시간 30분 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(150)

@app.get("/korean-fire-spread/180", response_model=FireSpreadResponse)
async def get_korean_180min():
    """한국 산림 - 발화 후 3시간 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(180)

@app.get("/korean-fire-spread/210", response_model=FireSpreadResponse)
async def get_korean_210min():
    """한국 산림 - 발화 후 3시간 30분 시점"""
    return await FireSpreadAPI.get_korean_fire_spread(210)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
