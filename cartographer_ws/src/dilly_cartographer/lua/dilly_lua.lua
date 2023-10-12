include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "odom",  -- 로봇의 기준 프레임
  published_frame = "base_link",
  odom_frame = "odom",
  provide_odom_frame = false,  -- 오도메트리 프레임 제공하지 않음
  use_odometry = true,
  use_nav_sat = true,
  use_imu_data = true,
  num_laser_scans = 0,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  publish_frame_projected_to_2d = true,  -- 2D로 투영된 프레임 게시
}

-- Map Builder 설정
MAP_BUILDER.use_trajectory_builder_2d = true

-- Trajectory Builder 설정
TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 30
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 10
TRAJECTORY_BUILDER_2D.use_imu_data = true
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(0.1)

-- Sensor Bridge 설정
POSE_GRAPH.optimize_every_n_nodes = 90
POSE_GRAPH.global_sampling_ratio = 0.003
POSE_GRAPH.constraint_builder.min_score = 0.55
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.6
POSE_GRAPH.optimization_problem.ceres_solver_options.use_nonmonotonic_steps = false

return options
