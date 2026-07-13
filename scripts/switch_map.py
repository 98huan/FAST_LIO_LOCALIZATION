#!/usr/bin/python3.8
# coding=utf8
import subprocess
import rospy

def close_terminal_by_name(terminal_name):
    # 使用 wmctrl -l 来列出所有窗口和其标题
    wmctrl_process = subprocess.Popen(["wmctrl", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, _ = wmctrl_process.communicate()

    # 在输出中查找指定名称的终端
    for line in stdout.splitlines():
        if terminal_name in line:
            # 获取终端的窗口 ID，并使用 wmctrl -i -c 命令关闭该终端
            window_id = line.split()[0]
            subprocess.run(["wmctrl", "-i", "-c", window_id])
            print("已关闭终端:", terminal_name)
            return

    # 如果未找到指定名称的终端
    print("未找到名称为", terminal_name, "的终端")

def step(commands):
    # global i
    command_str = " && ".join(commands)  # 将命令列表连接为一个字符串，使用 && 分隔

    # subprocess.run() 函数用于执行外部命令。它会创建一个新的子进程，并等待子进程执行完成后返回。
    # gnome-terminal" 是要执行的命令，即打开一个新的终端
    # "--" 表示后面的参数将被传递给 gnome-terminal 命令
    # 使用 bash -c 执行命令
    rospy.sleep(1)
    subprocess.run(["gnome-terminal", "--", "bash", "-c", command_str]) # title 无效???
    # 添加标题："--title", str(i),
    # i = i + 1

def step_name(commands):
    global i
    command_str = " && ".join(commands)  # 将命令列表连接为一个字符串，使用 && 分隔

    # subprocess.run() 函数用于执行外部命令。它会创建一个新的子进程，并等待子进程执行完成后返回。
    # gnome-terminal" 是要执行的命令，即打开一个新的终端
    # "--" 表示后面的参数将被传递给 gnome-terminal 命令
    # 使用 bash -c 执行命令
    rospy.sleep(1)
    subprocess.run(["gnome-terminal", "--title", str(i), "--", "bash", "-c", command_str]) # title 无效???
    # 添加标题："--title", str(i),
    i = i + 1

def start_roscore():
    command = "roscore"
    print("启动roscore:", command)
    subprocess.Popen(["gnome-terminal", "--", "bash", "-c", command])

i = 101

if __name__ == '__main__':
    rospy.init_node('switch_map')
    rospy.loginfo('*****************************')

    command_1 = [
        "ls /dev/ttyUSB0",
        "sudo chmod 777 /dev/ttyUSB0"
    ]
    command_2 = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "roslaunch dy_rec dy_rec.launch"
    ]
    command_3 = [
        "cd /home/agv/agv",
        "sudo ptpd -M -i eth0 -C"
    ]
    command_4 = [
        "cd /home/agv/3rdparty/livox_ws",
        "source ./devel/setup.bash",
        "roslaunch livox_ros_driver livox_hub_msg.launch "
    ]
    command_5 = [
        "cd /home/agv/3rdparty/livox_ws",
        "source ./devel/setup.bash",
        "rosrun livox_hc hc"
    ]
    command_6 = [
        "cd /home/agv/3rdparty/livox_ws",
        "source ./devel/setup.bash",
        "roslaunch fast_lio_localization localization_avia.launch"
    ]
    command_7 = [
        "cd /home/agv/3rdparty/livox_ws",
        "source ./devel/setup.bash",
        "rosrun fast_lio_localization publish_initial_pose.py 0.1 0.1 0.1 0 0 0"
    ]
    command_6_3 = [
        "cd /home/agv/3rdparty/livox_ws",
        "source ./devel/setup.bash",
        "roslaunch fast_lio_localization localization_avia_floor3.launch"
    ]
    command_7_3 = [
        "cd /home/agv/3rdparty/livox_ws",
        "source ./devel/setup.bash",
        "rosrun fast_lio_localization publish_initial_pose.py 0.1 0.1 0.1 0 0 0"
    ]
    command_can = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "roslaunch by_djstl rviz_can_1.launch"
    ]
    command_global = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "rosrun by_djstl shinei_djstl"
    ]
    command_local = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "rosrun la fs"
    ] 
    command_global_floor3 = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "rosrun by_djstl shinei_djstl_3"
    ]
    command_run_elevator = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "rosrun la gz_dianti"
    ]
    command_camera = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "roslaunch multicam_yolov5 perception_by_yolov5.launch"
    ]
    command_TCP_1 = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "rosrun tcp_by send_and_receive"
    ]
    command_TCP_2 = [
        "cd /home/agv/agv",
        "source ./devel/setup.bash",
        "rosrun tcp_by send_and_receive_2"
    ]

    current_map_index = 0 # 默认打开公共部分终端
    rospy.set_param('map_index', current_map_index)

    current_close_index = 0 
    rospy.set_param('close_index', current_close_index)    

    # start_roscore() # 启动roscore, 未启动成功, 什么原因???
    while True:
        r = rospy.Rate(1)                   # 1 Hz
        r.sleep()                           # 等待足够的时间，以满足之前设置的频率要求
        index = rospy.get_param("map_index")
        close = rospy.get_param("close_index")
        
        if(index == -1):
            print("ok!")
        
        elif(index == 0):   # 公共部分
            print("---打开公共部分！---")
            rospy.set_param('map_index', -1)
            step(command_camera)
            rospy.sleep(25)
            step(command_1)
            rospy.sleep(1.5) 
            step(command_2)
            rospy.sleep(4)
            step(command_3) # 有问题，在运行中为什莫关闭终端了
            rospy.sleep(2)
            step(command_4)
            rospy.sleep(5)
            step(command_5)
            rospy.sleep(3) 

            step(command_can)
            rospy.sleep(3) 
            step(command_TCP_1)
            rospy.sleep(3)
            step(command_TCP_2)
            rospy.sleep(3)

        elif(index == 1):
            print("当前楼层: 1")
            rospy.set_param('map_index', -1)

            rospy.sleep(1)
            step(command_6)
            rospy.sleep(20) # 根据地图大小调整，若地图过大，增加时间
            step(command_7)
            rospy.sleep(3)

            step_name(command_local)
            rospy.sleep(3)
            step_name(command_global)
            rospy.sleep(4)
            step_name(command_run_elevator)
            rospy.sleep(4)

        elif(index == 2):
            print("当前楼层: 2")
            rospy.set_param('map_index', -1)

        elif(index == 3):
            print("当前楼层: 3")
            rospy.set_param('map_index', -1)

            rospy.sleep(1)
            close_terminal_by_name("103") # kill run elevator !      

            rospy.sleep(1)
            step(command_6_3)
            rospy.sleep(10)
            step(command_7_3)
            rospy.sleep(3)

            step_name(command_local)
            rospy.sleep(3)
            step_name(command_global_floor3)
            rospy.sleep(4)
        
        else:
            print(" floor 错误! ")



        if(close == -1):
            print("close ok!")
        
        elif(close == 1):
            rospy.set_param('close_index', -1)
            print("close == 1!")
            # 关闭终端. 参数：终端名
            rospy.sleep(1)
            close_terminal_by_name("/home/agv/3rdparty/livox_ws/src/FAST_LIO_LOCALIZATION/launch/localization_avia.launch http://localhost:11311")
            rospy.sleep(1)
            close_terminal_by_name("102")  # kill global!
            rospy.sleep(1)
            close_terminal_by_name("101")  # kill local!
            rospy.sleep(1)                  
        
        elif(close == 2):
            rospy.set_param('close_index', -1)
            print("close == 2!")
            # 关闭终端. 参数：终端名
            rospy.sleep(1)

        elif(close == 3):
            rospy.set_param('close_index', -1)
            print("close == 3!")
            # 关闭终端. 参数：终端名
            rospy.sleep(1)
            close_terminal_by_name("/home/agv/3rdparty/livox_ws/src/FAST_LIO_LOCALIZATION/launch/localization_avia_floor3.launch http://localhost:11311")
            rospy.sleep(1)


        else:
            print("close: 0")




