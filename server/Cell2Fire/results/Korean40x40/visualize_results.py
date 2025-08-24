#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cell2Fire 결과 시각화 스크립트
Korean40x40 동네 산 산불 시뮬레이션 결과 분석
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.colors import ListedColormap

def visualize_results():
    print("=== Cell2Fire Korean40x40 시뮬레이션 결과 분석 ===")
    
    # 1. 일반 통계 읽기
    stats_df = pd.read_csv('/home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/Stats/FinalStats.csv')
    print(f"\\n📊 시뮬레이션 결과 요약:")
    print(f"   - 총 셀 수: {stats_df['NonBurned'].iloc[0] + stats_df['Burned'].iloc[0]}")
    print(f"   - 타지 않은 셀: {stats_df['NonBurned'].iloc[0]}개 ({stats_df['%NonBurned'].iloc[0]:.1%})")
    print(f"   - 탄 셀: {stats_df['Burned'].iloc[0]}개 ({stats_df['%Burned'].iloc[0]:.1%})")
    
    # 2. 화상확률 맵 읽기
    bp_data = np.loadtxt('/home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/Stats/BProb.csv')
    print(f"\\n🔥 화상확률 맵:")
    print(f"   - 격자 크기: {bp_data.shape[0]} x {bp_data.shape[1]}")
    print(f"   - 최대 화상확률: {bp_data.max():.2f}")
    print(f"   - 평균 화상확률: {bp_data.mean():.3f}")
    
    # 3. 시각화
    plt.style.use('default')
    fig = plt.figure(figsize=(16, 12))
    
    # 화상확률 맵
    ax1 = plt.subplot(2, 3, 1)
    im1 = ax1.imshow(bp_data, cmap='Reds', vmin=0, vmax=1)
    ax1.set_title('화상확률 맵 (Burn Probability)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('경도 방향 (50m/셀)')
    ax1.set_ylabel('위도 방향 (50m/셀)')
    plt.colorbar(im1, ax=ax1, label='화상확률')
    
    # 최종 화재 상태
    final_grid = np.loadtxt('/home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/Grids/Grids1/ForestGrid07.csv', delimiter=',')
    ax2 = plt.subplot(2, 3, 2)
    cmap = ListedColormap(['lightgray', 'red'])
    im2 = ax2.imshow(final_grid, cmap=cmap, vmin=0, vmax=1)
    ax2.set_title('최종 화재 확산 결과', fontsize=12, fontweight='bold')
    ax2.set_xlabel('경도 방향 (50m/셀)')
    ax2.set_ylabel('위도 방향 (50m/셀)')
    
    # 범례 추가
    burned_patch = mpatches.Patch(color='red', label='탄 지역')
    unburned_patch = mpatches.Patch(color='lightgray', label='타지 않은 지역')
    ax2.legend(handles=[unburned_patch, burned_patch], loc='upper right')
    
    # 시간별 화재 확산 (4개 시점)
    time_points = [0, 2, 4, 7]
    titles = ['초기 상태', '2시간 후', '4시간 후', '최종 (7시간 후)']
    
    for i, (time_point, title) in enumerate(zip(time_points, titles)):
        ax = plt.subplot(2, 3, 3 + i)
        if time_point < 10:
            grid_file = f'/home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/Grids/Grids1/ForestGrid0{time_point}.csv'
        else:
            grid_file = f'/home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/Grids/Grids1/ForestGrid{time_point}.csv'
        
        try:
            time_grid = np.loadtxt(grid_file, delimiter=',')
            im = ax.imshow(time_grid, cmap=cmap, vmin=0, vmax=1)
            ax.set_title(title, fontsize=10, fontweight='bold')
            ax.set_xlabel('경도 (50m/셀)')
            ax.set_ylabel('위도 (50m/셀)')
            
            # 탄 셀 수 표시
            burned_count = np.sum(time_grid == 1)
            ax.text(0.02, 0.98, f'탄 셀: {burned_count}개', 
                   transform=ax.transAxes, va='top', ha='left',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        except:
            ax.text(0.5, 0.5, '데이터 없음', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title, fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/fire_simulation_results.png', 
                dpi=300, bbox_inches='tight')
    print(f"\\n📈 시각화 결과가 저장되었습니다:")
    print(f"   - 파일: /home/asd1802/junction_asia_2025/Cell2Fire/results/Korean40x40/fire_simulation_results.png")
    
    # 4. 화재 확산 분석
    print(f"\\n🔍 상세 분석:")
    
    # 중심점에서의 거리별 화상확률 분석
    center_row, center_col = bp_data.shape[0] // 2, bp_data.shape[1] // 2
    distances = []
    burn_probs = []
    
    for i in range(bp_data.shape[0]):
        for j in range(bp_data.shape[1]):
            dist = np.sqrt((i - center_row)**2 + (j - center_col)**2) * 50  # 미터 단위
            distances.append(dist)
            burn_probs.append(bp_data[i, j])
    
    distances = np.array(distances)
    burn_probs = np.array(burn_probs)
    
    # 거리별 평균 화상확률
    dist_bins = np.arange(0, distances.max() + 50, 50)
    bin_indices = np.digitize(distances, dist_bins)
    
    avg_burn_prob_by_dist = []
    for bin_idx in range(1, len(dist_bins)):
        mask = bin_indices == bin_idx
        if np.any(mask):
            avg_burn_prob_by_dist.append(burn_probs[mask].mean())
        else:
            avg_burn_prob_by_dist.append(0)
    
    print(f"   - 중심점에서 100m 이내 평균 화상확률: {avg_burn_prob_by_dist[1]:.3f}")
    print(f"   - 중심점에서 200m 이내 평균 화상확률: {avg_burn_prob_by_dist[3]:.3f}")
    print(f"   - 화재가 확산된 최대 거리: {distances[burn_probs > 0].max():.0f}m")
    
    # 연료 타입별 분석
    data_df = pd.read_csv('/home/asd1802/junction_asia_2025/Cell2Fire/data/Korean40x40/Data.csv')
    print(f"\\n🌲 연료 타입별 특성:")
    for fuel_type in data_df['fueltype'].unique():
        count = (data_df['fueltype'] == fuel_type).sum()
        print(f"   - {fuel_type}: {count}개 ({count/len(data_df)*100:.1f}%)")
    
    plt.show()

if __name__ == "__main__":
    visualize_results()
