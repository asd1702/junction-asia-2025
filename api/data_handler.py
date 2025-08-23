"""
데이터 처리 로직
"""
import os
import pandas as pd
import numpy as np
import csv
from typing import List, Dict, Tuple
from .models import BurnedPixel

# 기본 설정
RESULTS_BASE_PATH = "/home/asd1802/junction_asia_2025/Cell2Fire/results"
DATA_BASE_PATH = "/home/asd1802/junction_asia_2025/Cell2Fire/data"

class DataHandler:
    """Cell2Fire 데이터 처리 클래스"""
    
    @staticmethod
    def get_coordinates_from_data_csv(dataset_name: str) -> Tuple[Dict[str, Dict[str, float]], int]:
        """Data.csv에서 각 셀의 실제 좌표를 가져오기"""
        try:
            data_path = os.path.join(DATA_BASE_PATH, dataset_name, "Data.csv")
            df = pd.read_csv(data_path)
            
            # 격자 크기 계산 (3x3, 20x20, 40x40 등)
            total_cells = len(df)
            grid_size = int(np.sqrt(total_cells))
            
            coordinates = {}
            for idx, row in df.iterrows():
                grid_row = idx // grid_size
                grid_col = idx % grid_size
                coordinates[f"{grid_row},{grid_col}"] = {
                    "lat": float(row.get("lat", 0)) if pd.notna(row.get("lat")) else 0.0,
                    "lon": float(row.get("lon", 0)) if pd.notna(row.get("lon")) else 0.0
                }
            
            return coordinates, grid_size
        except Exception as e:
            print(f"좌표 데이터 로드 오류: {e}")
            return {}, 0

    @staticmethod
    def parse_grid_csv(file_path: str, coordinates_map: dict, grid_size: int) -> List[BurnedPixel]:
        """ForestGrid CSV 파일을 파싱해서 연소된 픽셀 좌표 반환"""
        burned_pixels = []
        
        try:
            with open(file_path, 'r') as f:
                csv_reader = csv.reader(f)
                for row_idx, row in enumerate(csv_reader):
                    if not row:  # 빈 행 건너뛰기
                        continue
                    for col_idx, cell_value in enumerate(row):
                        if cell_value.strip() == '1':  # 연소된 셀
                            coord_key = f"{row_idx},{col_idx}"
                            coord_info = coordinates_map.get(coord_key, {"lat": 0, "lon": 0})
                            
                            burned_pixels.append(BurnedPixel(
                                row=row_idx,
                                col=col_idx,
                                lat=coord_info["lat"],
                                lon=coord_info["lon"]
                            ))
        except Exception as e:
            print(f"그리드 파일 파싱 오류: {e}")
        
        return burned_pixels

    @staticmethod
    def get_ignition_point(dataset_name: str) -> Dict[str, int]:
        """점화점 정보 가져오기"""
        try:
            ignition_path = os.path.join(DATA_BASE_PATH, dataset_name, "IgnitionPoints.csv")
            if os.path.exists(ignition_path):
                df = pd.read_csv(ignition_path)
                if not df.empty:
                    return {"row": int(df.iloc[0].get("row", 0)), "col": int(df.iloc[0].get("col", 0))}
        except Exception as e:
            print(f"점화점 정보 로드 오류: {e}")
        
        return {"row": 1, "col": 1}  # 기본값

    @staticmethod
    def get_available_simulations() -> List[str]:
        """사용 가능한 시뮬레이션 목록 반환"""
        simulations = []
        
        if os.path.exists(RESULTS_BASE_PATH):
            for item in os.listdir(RESULTS_BASE_PATH):
                if os.path.isdir(os.path.join(RESULTS_BASE_PATH, item)) and item != "__pycache__":
                    simulations.append(item)
        
        return simulations

    @staticmethod
    def calculate_time_step(dataset: str, time_minutes: int) -> int:
        """데이터셋에 따른 시간 스텝 계산"""
        if dataset.startswith("Korean"):
            return time_minutes // 30  # 30분 간격
        else:
            return min(time_minutes // 10, 10)  # 기존 10분 단위

    @staticmethod
    def get_grid_file_path(dataset: str, simulation: int, time_minutes: int) -> str:
        """그리드 파일 경로 생성"""
        result_path = os.path.join(RESULTS_BASE_PATH, dataset)
        grid_path = os.path.join(result_path, "Grids", f"Grids{simulation}")
        
        time_step = DataHandler.calculate_time_step(dataset, time_minutes)
        grid_file = f"ForestGrid{time_step:02d}.csv"
        
        return os.path.join(grid_path, grid_file)
