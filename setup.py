import datetime
import time
import tkinter.messagebox
from threading import Thread
from tkinter import *
from tkinter import ttk, scrolledtext

import psutil
import pymysql
import win32api
import win32con
from ttkbootstrap import Style

status = True

style = Style(theme="journal")  # 使用的主题名称

now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
winWidth = 500
winHeight = 660
# 获取屏幕分辨率
screenWidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screenHeight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)


class MY_GUI:
    def __init__(self, init_window_name):
        self.init_window_name = None
        self.start_button = ttk.Button(self.init_window_name, text="执行监控程序", width=12, style='info.TButton',
                                       command=lambda: [self.start_info(), self.start_thread()])  # 调用内部方法  加()为直接调用
        self.stop_button = ttk.Button(self.init_window_name, text="结束监控程序", width=12, style='info.TButton',
                                      command=lambda: [self.stop_info(), self.stop_proc()])  # 调用内部方法  加()为直接调用
        self.clear_button = ttk.Button(self.init_window_name, text="清除所有数据", width=12, style='info.TButton',
                                       command=lambda: [self.clear(), self.clear_info()])  # 调用内部方法  加()为直接调用
        self.result_data_Text = scrolledtext.ScrolledText(self.init_window_name, width=69, height=33)  # 处理结果展示
        self.result_data_label = ttk.Label(self.init_window_name, text="执行结果", justify=CENTER,
                                           font=('微软雅黑', 11, 'bold'), style='info.TLabel', relief=FLAT)
        self.init_window_name = init_window_name

    # 运行程序
    def running(self):
        while status:
            self.get_sys_info()
            time.sleep(5)
            if status is not True:
                self.result_data_Text.insert(END, now_time + "  程序已停止...")
                break  # Break while loop when stop = 1

    # 启动
    def start_thread(self):
        # Assign global variable and initialize value
        global status
        status = True
        # Create and launch a thread
        t = Thread(target=self.running)
        t.setDaemon(True)
        t.start()

    # 停止
    def stop_proc(self):
        global status
        status = False
        # Create and launch a thread
        t = Thread(target=self.running())
        t.start()

    # 启动提示
    def start_info(self):
        tkinter.messagebox.showinfo("监控消息", "监控系统已启动！")

    # 停止提示
    def stop_info(self):
        tkinter.messagebox.showinfo("监控消息", "监控系统已停止！")

    # 清空提示
    def clear_info(self):
        tkinter.messagebox.showinfo("清除消息", "面板数据已清除！")

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("系统资源监控工具_v1.0")  # 窗口名
        self.init_window_name.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        self.init_window_name.resizable(False, False)  ## 规定窗口不可缩放
        self.init_window_name["bg"] = "WhiteSmoke"
        self.result_data_label.grid(row=2, column=1, padx=10, pady=0, sticky=W)
        # 文本框
        self.result_data_Text.grid(row=3, column=1, rowspan=10, columnspan=5)
        # 按钮
        self.start_button.grid(row=0, column=1, padx=10, pady=13)
        self.stop_button.grid(row=0, column=2, padx=10, pady=13)
        self.clear_button.grid(row=0, column=3, padx=10, pady=13)

    # 资源监控函数
    def get_sys_info(self):
        # 连接数据库
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='aisys',
                                     charset='utf8')
        # 获取连接下的游标
        cursor_test = connection.cursor()
        connection.ping(reconnect=True)
        # 当前时间
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # self.result_data_Text.insert(END, now_time + "\n")
        # 查看cpu物理个数的信息
        cpuNum = psutil.cpu_count(logical=False)
        # self.result_data_Text.insert(END, "物理CPU个数: %s" % cpuNum + "\n")
        # cpu的使用率
        cpu = psutil.cpu_percent(1)
        # self.result_data_Text.insert(END, "cpu使用率: %s" % (str(cpu)) + '%' + "\n")

        # 查看内存信息,剩余内存.free  总共.total
        # round()函数方法为返回浮点数x的四舍五入值。
        free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
        total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
        memory = int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(
            psutil.virtual_memory().total)
        # self.result_data_Text.insert(END, "物理内存： %s G" % total + "\n")
        # self.result_data_Text.insert(END, "剩余物理内存： %s G" % free + "\n")
        # self.result_data_Text.insert(END, "物理内存使用率： %s %%" % int(memory * 100) + "\n")

        # 获取系统启动时间
        startTime = datetime.datetime.fromtimestamp(psutil.boot_time())
        # self.result_data_Text.insert(END, "系统启动时间: %s" % startTime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        # 获取系统用户
        # 获取网卡信息，可以得到得到网卡属性，连接数，当前数据等信息
        net = psutil.net_io_counters()
        bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
        bytes_rcvd = '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)
        # self.result_data_Text.insert(END, "网卡接收数据 %s 网卡发送数据 %s" % (bytes_rcvd, bytes_sent) + "\n")
        # 获取磁盘数据信息
        io = psutil.disk_partitions()
        # self.result_data_Text.insert(END,
        #                              '-----------------------------磁盘信息--------------------------------' + "\n")
        for i in io:
            try:
                o = psutil.disk_usage(i.device)
                totalDisk = int(o.total / (1024.0 * 1024.0 * 1024.0))
                spareDisk = int(o.used / (1024.0 * 1024.0 * 1024.0))
                # self.result_data_Text.insert(END, "总容量：" + str(totalDisk) + "G" + "\n")
                # self.result_data_Text.insert(END, "已用容量：" + str(spareDisk) + "G" + "\n")
                # self.result_data_Text.insert(END,
                #                              "可用容量：" + str(
                #                                  int(o.free / (1024.0 * 1024.0 * 1024.0))) + "G" + "\n")

            except PermissionError:
                continue

            totalDisk += totalDisk
            spareDisk += spareDisk
        # self.result_data_Text.insert(END,
        #                              '----------------------------------------------------------------------' + "\n")
        # self.result_data_Text.insert(END,
        #                              '----------------------------每5S获取一次数据--------------------------' + "\n")
        self.result_data_Text.insert(END, "程序已启动..." + "\n" +
                                     now_time + "\n" + "物理CPU个数: %s" % cpuNum + "\n" + "cpu使用率: %s" % (
                                         str(cpu)) + '%' + "\n" + "物理内存： %s G" % total + "\n" + "剩余物理内存： %s G" % free + "\n" + "物理内存使用率： %s %%" % int(
            memory * 100) + "\n" + "系统启动时间: %s" % startTime.strftime(
            "%Y-%m-%d %H:%M:%S") + "\n" + "网卡接收数据 %s 网卡发送数据 %s" % (
                                         bytes_rcvd, bytes_sent) + "\n" + "总容量：" + str(
            totalDisk) + "G" + "\n" + "已用容量：" + str(
            spareDisk) + "G" + "\n" + "可用容量：" + str(
            int(o.free / (
                    1024.0 * 1024.0 * 1024.0))) + "G" + "\n" + '--------------------------------------------------------' + "\n" + '-----------------------每5S获取一次数据---------------------' + "\n")
        self.result_data_Text.update()
        self.result_data_Text.focus_force()

        self.result_data_Text.see(END)
        # 执行sql语句
        sql = """INSERT INTO system_info(cpuPercent,totalMem,time,cpuNum,totalDisk,spareDisk,spareMem,startTime,netDown,netUp)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        try:
            # 执行sql语句
            cursor_test.execute(sql,
                                (
                                    cpu, total, now_time, cpuNum, totalDisk, spareDisk, free, startTime,
                                    bytes_rcvd,
                                    bytes_sent))
            # 提交到数据库执行
            connection.commit()
        except:
            # 如果发生错误则回滚
            connection.rollback()
        # 关闭数据库连接
        connection.close()

    # 清除文本框
    def clear(self):
        self.result_data_Text.delete(1.0, END)


def gui_start():
    init_window = style.master  # 实例化出一个父窗口
    Window = MY_GUI(init_window)
    # 设置根窗口默认属性
    Window.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
