#!/usr/bin/env python
import rospy
import tf2_ros
import tf2_msgs.msg
import geometry_msgs.msg
from tf_conversions import transformations

def msg_from_matrix(transform_matrix, child_frame_id="child", parent_frame_id="world"):
    t = geometry_msgs.msg.TransformStamped()
    t.header.frame_id = parent_frame_id
    t.header.stamp = rospy.Time.now()
    t.child_frame_id = child_frame_id

    translation = transformations.translation_from_matrix(transform_matrix)

    t.transform.translation.x = translation[0]
    t.transform.translation.y = translation[1]
    t.transform.translation.z = translation[2]

    quaternion = transformations.quaternion_from_matrix(transform_matrix)

    t.transform.rotation.x = quaternion[0]
    t.transform.rotation.y = quaternion[1]
    t.transform.rotation.z = quaternion[2]
    t.transform.rotation.w = quaternion[3]

    return t


if __name__ == '__main__':
    pub = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=10)
    rospy.init_node('fixed_tf2_broadcaster')
    rate = rospy.Rate(10) # 10Hz

    # object
    object_rot_matrix = transformations.euler_matrix(0.79, 0.0, 0.79)
    object_transl_matrix = transformations.translation_matrix([0.0, 1.0, 1.0])
    object_transf_matrix = transformations.concatenate_matrices(object_rot_matrix, object_transl_matrix)

    # robot
    robot_rot_matrix = transformations.euler_matrix(0.0, 1.5, 0.0)
    robot_transl_matrix = transformations.translation_matrix([0.0, -1.0, 0.0])
    robot_transf_matrix = transformations.concatenate_matrices(robot_rot_matrix, robot_transl_matrix)

    # camera
    camera_transl_matrix = transformations.translation_matrix([0.0, 0.1, 0.1])

    while not rospy.is_shutdown():
        base_msg = msg_from_matrix(transformations.identity_matrix(), child_frame_id="base")
        object_msg = msg_from_matrix(object_transf_matrix, child_frame_id="object", parent_frame_id="base")
        robot_msg = msg_from_matrix(robot_transf_matrix, child_frame_id="robot", parent_frame_id="base")

        combi_message = tf2_msgs.msg.TFMessage([base_msg, object_msg, robot_msg])
        pub.publish(combi_message)

        rate.sleep()
