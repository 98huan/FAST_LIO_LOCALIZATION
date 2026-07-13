#!/usr/bin/python3.8
# coding=utf8
import open3d as o3d    # Version: 0.13.0


if __name__ == "__main__":
    source = o3d.io.read_point_cloud("/home/td/slam/localization/src/FAST_LIO_LOCALIZATION/PCD/scans_floor3.pcd")
    print("Number of points in source:", len(source.points))
    # 每个体素只保留一个点作为其代表。这个代表点是通过在每个体素内选择距离体素中心最近的点来确定的。

    target_0_1 = source.voxel_down_sample(0.4)
    print("Number of points in target_0_1:", len(target_0_1.points))
    o3d.visualization.draw_geometries([target_0_1])
    o3d.io.write_point_cloud("/home/td/slam/localization/src/FAST_LIO_LOCALIZATION/PCD/scans_floor3_voxel_down_sample.pcd", target_0_1)