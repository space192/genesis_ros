from gs_ros import GsRosBridge
import rclpy
from rclpy.node import Node
import genesis as gs
import os
import sys


# Resolve the config path relative to THIS file so it works regardless of the
# current working directory. The original script used "src/configs/panda_demo.yaml",
# which assumes the bridge is cloned directly into <workspace>/src (the README's
# layout). In this repo the bridge is a submodule at src/genesis_ros/, so the
# config lives next to this script in configs/.
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(_HERE, "configs", "panda_demo.yaml")


def main(args=None):
    # Optional first CLI arg = config path (absolute, or a name under configs/).
    # Defaults to panda_demo.yaml.
    config = DEFAULT_CONFIG
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        config = arg if os.path.isabs(arg) or os.path.sep in arg else os.path.join(_HERE, "configs", arg)
    print(f"[test_import] using config: {config}")

    # gs.metal = Apple GPU (M-series). Use gs.gpu/gs.cuda on Linux+NVIDIA,
    # gs.cpu as a fallback if Metal has issues.
    gs.init(backend=gs.metal, logging_level="info", performance_mode=True)
    rclpy.init(args=args)

    default_ros_node = Node("gs_ros_bridge_node")
    # four ros2 nodes can be provided to the constructor
    # default_ros_node (default node used for the clock,ros2_control and service unless overiden),
    # nodes to override the default nodes with: ros_clock_node,ros_control_node,ros_service_node
    # if the default_ros_node is used for everything you may experience bottlenecks
    gs_ros_bridge = GsRosBridge(
        default_ros_node,
        config,
        add_debug_objects=False,
        enable_simulation_interfaces=True,
    )
    gs_ros_bridge.build()
    try:
        while rclpy.ok():
            gs_ros_bridge.step()
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        del gs_ros_bridge
        gs.destroy()


if __name__ == "__main__":
    main()

