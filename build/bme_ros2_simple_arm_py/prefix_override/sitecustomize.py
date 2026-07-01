import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/siddharth/sor_ws1/install/bme_ros2_simple_arm_py'
