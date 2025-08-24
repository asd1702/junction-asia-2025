"""
데이터 처리 로직
"""
import os
import pandas as pd
import numpy as np
import csv
from typing import List, Dict, Tuple, Optional
from .models import BurnedPixel

# 기본 설정
# 현재 파일의 위치를 기준으로 동적으로 경로 설정
HANDLER_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.dirname(HANDLER_DIR)
CELL2FIRE_DIR = os.path.join(SERVER_DIR, "Cell2Fire")

RESULTS_BASE_PATH = os.path.join(CELL2FIRE_DIR, "results")
DATA_BASE_PATH = os.path.join(CELL2FIRE_DIR, "data")

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
    def get_ignition_point(dataset: str) -> Optional[Dict[str, float]]:
        """점화 지점 좌표를 IgnitionPoints.csv에서 직접 읽어 반환"""
        ignition_file_path = os.path.join(DATA_BASE_PATH, dataset, "IgnitionPoints.csv")
        if not os.path.exists(ignition_file_path):
            return None

        try:
            ignition_df = pd.read_csv(ignition_file_path)
            if ignition_df.empty:
                return None
            
            # 첫 번째 점화 지점 사용
            ncell_val = ignition_df.iloc[0]['Ncell']
            
            _, grid_size = DataHandler.get_coordinates_from_data_csv(dataset)
            if grid_size == 0:
                return None

            # Ncell (1-based) to 0-based index
            zero_based_index = int(ncell_val) - 1
            row_idx = zero_based_index // grid_size
            col_idx = zero_based_index % grid_size
            coord_key = f"{row_idx},{col_idx}"

            # 좌표 가져오기
            coordinates_map, _ = DataHandler.get_coordinates_from_data_csv(dataset)
            
            return coordinates_map.get(coord_key)

        except Exception as e:
            print(f"Ignition point error: {e}")
            return None

    @staticmethod
    def get_ignition_pixel(dataset: str) -> Optional[BurnedPixel]:
        """점화 지점 정보를 BurnedPixel 객체로 반환"""
        ignition_file_path = os.path.join(DATA_BASE_PATH, dataset, "IgnitionPoints.csv")
        if not os.path.exists(ignition_file_path):
            return None

        try:
            ignition_df = pd.read_csv(ignition_file_path)
            if ignition_df.empty:
                return None
            
            ncell_val = ignition_df.iloc[0]['Ncell']
            
            _, grid_size = DataHandler.get_coordinates_from_data_csv(dataset)
            if grid_size == 0:
                return None

            # Ncell (1-based) to 0-based index
            zero_based_index = int(ncell_val) - 1
            row_idx = zero_based_index // grid_size
            col_idx = zero_based_index % grid_size
            coord_key = f"{row_idx},{col_idx}"

            coordinates_map, _ = DataHandler.get_coordinates_from_data_csv(dataset)
            coord_info = coordinates_map.get(coord_key)

            if coord_info:
                return BurnedPixel(
                    row=row_idx,
                    col=col_idx,
                    lat=coord_info["lat"],
                    lon=coord_info["lon"]
                )
            return None

        except Exception as e:
            print(f"Ignition pixel error: {e}")
            return None

    @staticmethod
    def get_grid_file_path(dataset: str, simulation: int, time_minutes: int) -> str:
        """그리드 파일 경로 생성"""
        time_step = DataHandler.calculate_time_step(dataset, time_minutes)
        grid_file = f"ForestGrid{time_step:02d}.csv"
        return os.path.join(RESULTS_BASE_PATH, dataset, "Grids", f"Grids{simulation}", grid_file)

    @staticmethod
    def calculate_time_step(dataset: str, time_minutes: int) -> int:
        """시간(분)을 기반으로 시뮬레이션 시간 단계 계산"""
        if time_minutes == 0:
            return 0
        
        # 9cellsC1 예제는 10분 간격
        if dataset.startswith("9cellsC1"):
            return time_minutes // 10
        
        # 기본값은 30분 간격
        return time_minutes // 30
