import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'my_robot_description'

    # 1. Process the URDF (Xacro) file
    xacro_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'robot.urdf.xacro')
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # 2. Robot State Publisher Node (Tracks robot joints and transforms)
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': True
        }]
    )

    # 3. Launch the Gazebo Simulator (GZ Sim) with Custom Obstacle World
    world_file = os.path.join(get_package_share_directory(package_name), 'worlds', 'obstacle_course.sdf')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': f'-r {world_file}'}.items()
    )

    # 4. Node to spawn the robot entity inside the Gazebo world
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'robot_car'],
        output='screen'
    )

    # 5. Professional Bridge Node (Handles Keyboard control, Camera feed, and MPU data in one bridge)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Motor control bridge (/cmd_vel)
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            # Odometry tracking bridge (/odom)
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            # MPU6050 / IMU sensor bridge (/imu)
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        bridge  # Unified communication bridge added here
    ])