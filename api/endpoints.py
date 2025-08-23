"""
API 엔드포인트 정의
"""
import os
from fastapi import HTTPException
from .models import FireSpreadResponse, AvailableSimulations, ServerStatus
from .data_handler import DataHandler, RESULTS_BASE_PATH

class FireSpreadAPI:
    """화재 확산 API 엔드포인트 클래스"""
    
    @staticmethod
    async def get_server_status() -> ServerStatus:
        """API 서버 상태 확인"""
        return ServerStatus(
            message="Cell2Fire API Server - Korean Forest Demo",
            status="running",
            version="1.0.0",
            korean_forest_data="Korean40x40 dataset available (2km x 2km, 50m resolution)",
            time_intervals="30분 간격 (30분 ~ 210분)",
            endpoints=[
                "/simulations - 사용 가능한 시뮬레이션 목록",
                "/korean-fire-spread/30 - 한국 산림 30분 후",
                "/korean-fire-spread/60 - 한국 산림 1시간 후", 
                "/korean-fire-spread/90 - 한국 산림 1시간 30분 후",
                "/korean-fire-spread/120 - 한국 산림 2시간 후",
                "/korean-fire-spread/150 - 한국 산림 2시간 30분 후",
                "/korean-fire-spread/180 - 한국 산림 3시간 후",
                "/korean-fire-spread/210 - 한국 산림 3시간 30분 후"
            ]
        )

    @staticmethod
    async def get_available_simulations() -> AvailableSimulations:
        """사용 가능한 시뮬레이션 목록 반환"""
        simulations = DataHandler.get_available_simulations()
        
        return AvailableSimulations(
            simulations=simulations,
            description="Cell2Fire로 실행된 시뮬레이션 결과들"
        )

    @staticmethod
    async def get_fire_spread_data(dataset: str, simulation: int, time_minutes: int) -> FireSpreadResponse:
        """특정 시간대의 산불 확산 데이터 반환"""
        
        # 결과 폴더 경로 구성
        result_path = os.path.join(RESULTS_BASE_PATH, dataset)
        grid_path = os.path.join(result_path, "Grids", f"Grids{simulation}")
        
        # 폴더 존재 확인
        if not os.path.exists(grid_path):
            raise HTTPException(
                status_code=404, 
                detail=f"시뮬레이션 결과를 찾을 수 없습니다: {dataset}/Grids{simulation}"
            )
        
        # 그리드 파일 경로 생성
        grid_file_path = DataHandler.get_grid_file_path(dataset, simulation, time_minutes)
        
        if not os.path.exists(grid_file_path):
            time_step = DataHandler.calculate_time_step(dataset, time_minutes)
            grid_file = f"ForestGrid{time_step:02d}.csv"
            raise HTTPException(
                status_code=404,
                detail=f"해당 시간대 데이터가 없습니다: {grid_file}"
            )
        
        # 좌표 매핑 정보 가져오기
        base_dataset = dataset.replace("_full", "")  # 9cellsC1_full -> 9cellsC1
        coordinates_map, grid_size = DataHandler.get_coordinates_from_data_csv(base_dataset)
        
        # 그리드 파일 파싱
        burned_pixels = DataHandler.parse_grid_csv(grid_file_path, coordinates_map, grid_size)
        
        # 점화점 정보
        ignition_point = DataHandler.get_ignition_point(base_dataset)
        
        # 메타데이터
        time_step = DataHandler.calculate_time_step(dataset, time_minutes)
        grid_file = f"ForestGrid{time_step:02d}.csv"
        
        metadata = {
            "dataset": dataset,
            "simulation_number": simulation,
            "grid_size": f"{grid_size}x{grid_size}",
            "grid_file": grid_file,
            "data_source": "Cell2Fire simulation results"
        }
        
        return FireSpreadResponse(
            time_minutes=time_minutes,
            total_burned_pixels=len(burned_pixels),
            burned_coordinates=burned_pixels,
            ignition_point=ignition_point,
            metadata=metadata
        )

    @staticmethod
    async def get_fire_spread_data_simple(dataset: str, time_minutes: int) -> FireSpreadResponse:
        """간단한 API: 첫 번째 시뮬레이션의 특정 시간대 데이터 반환"""
        return await FireSpreadAPI.get_fire_spread_data(dataset, 1, time_minutes)

    @staticmethod
    async def get_korean_fire_spread(time_minutes: int) -> FireSpreadResponse:
        """한국 산림 전용 엔드포인트"""
        return await FireSpreadAPI.get_fire_spread_data_simple("Korean40x40", time_minutes)
