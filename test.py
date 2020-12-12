import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块
import re # 正则表达式
import socket
import time


# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('Captain debug')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('800x600')  # 这里的乘是小x
# 第4步，在图形界面上创建一个标签label用以显示并放置
# l = tk.Label(window, bg='green', fg='white', width=60, text='empty').pack()
hvhc = {"src_volt": 4.7,
        "src_curr": 1.0,
        "sik_curr": 1.0,
        "mode":'idle'}
eth_link_status = {"mode":'disable'}

socket_encode = 'utf-8'

tk.Label(window, text='ip:', font=('Arial', 14)).place(x=0, y=0)
ip_para = tk.StringVar()
ip_para.set('169.254.246.99:8888')
ip_et = tk.Entry(window, textvariable=ip_para, width=20, font=('Arial', 12)).place(x=30, y=5)
# global ip_port = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ip_set():
    try:
        str_tmp = ip_para.get()
        addr = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", str_tmp)
        if addr:
            print(addr)
        else:
            print("re cannot find ip")
        # 端口号范围：0~65535
        if (re.search(':(6553[0-5]|'  # 五位：65530~65535  6553[0-5]
                 '655[0-2]\\d|'   # 五位：65500~65529  655[0-2]\d
                 '65[0-4]\\d{2}|' # 五位：65000~65499  65[0-4]\d{2}
                 '6[0-4]\\d{3}|'  # 五位：60000~64999  6[0-4]\d{3}
                 '[1-5]\\d{4}|'   # 五位：10000~59999  [1-5]\d{4}
                 '[1-9]\\d{1,3}|\\d)', str_tmp) != 'none'): # 四位：1000~9999    [1-9]\d{3}     前4种情况合并为：\d|[1-9]\d{1,3}
            port = re.findall(':(6553[0-5]|'
                     '655[0-2]\\d|'
                     '65[0-4]\\d{2}|'
                     '6[0-4]\\d{3}|'
                     '[1-5]\\d{4}|'
                     '[1-9]\\d{1,3}|\\d)', str_tmp)
        else:
            print("not match port")

        port_i = list(map(int, port)) # string list to int list
        ip_info = (addr[0], port_i[0])
        sock.connect(ip_info)
        eth_link_status["mode"] = 'enable'

        # if ip_bt['text'] == "打开端口":
        #     ip_bt['text'] = "关闭端口"
        #     print('if')
        #     # sock.connect(ip_info)
        # else:
        #     print('else')
        #     # ip_bt['text'] = "打开端口"
        #     # sock.close()

    except Exception as e:
        print("error", e)

ip_bt = tk.Button(window, text='打开端口', font=('Calibri', 12), width=10, height=1, command=ip_set).place(x = 220, y = 0)

# ip_bt['command'] = ip_set

def dev_send(x):
    x = x + "\r\n"
    print(x)
    if (eth_link_status["mode"] == 'enable'):
        sock.send(x.encode(socket_encode))
    else:
        tkinter.messagebox.showerror(title='Hi', message='网络未连接，请打开端口！')  # 提出错误对话窗

# 第6步，定义一个触发函数功能
def print_selection(v):
    print(v)
    # l.config(text='you have selected ' + v)

def src_get_volt(v):
    hvhc["src_volt"] = v

def src_get_curr(v):
    hvhc["src_curr"] = v

def sik_get_curr(v):
    hvhc["sik_curr"] = v

# HVHC设置函数
def hvhc_set(mode, volt, curr):
    if mode == "src":
        tmp = str(0)
    elif mode == "sik":
        tmp = str(1)
    else:
        print("mode set error")
        tmp = str(0)
        volt = 0.0
        curr = 0.0
    dev_send("hvhc_v_i_set(" + tmp + ",0," + str(volt) + "," + str(curr) + ")")

# 负载设置按钮回调函数
def sik_set():
    if hvhc['mode'] == 'src':
        tkinter.messagebox.showinfo(title='Hi', message='电源打开时无法打开负载！')  # 提示信息对话窗
        if tkinter.messagebox.askokcancel(title='mode error', message='是否关闭source！') == True:
            hvhc["src_curr"] = 0.0
            src_curr_val.set(hvhc['src_curr'])
            src_para.set('V:' + str(hvhc['src_volt']) + '  I:' + str(hvhc['src_curr']))
            hvhc_set("src", hvhc["src_volt"], hvhc["src_curr"])
            # time.sleep(100)
        else:
            print('更新负载设置fail')
            return 0
    hvhc_set("sik", 0.0, hvhc["sik_curr"])
    sik_para.set('I:' + str(hvhc['sik_curr']))
    # print(type(hvhc['sik_curr']))
    # print(hvhc['sik_curr'])
    if hvhc['sik_curr'] == '0.0':
        hvhc['mode'] = 'idle'
    else:
        hvhc['mode'] = 'sik'

# src_set 电源设置按钮回调函数
def src_set():
    if hvhc['mode'] == 'sik':
        tkinter.messagebox.showinfo(title='Hi', message='负载打开时无法打开源！')  # 提示信息对话窗
        # tkinter.messagebox.showwarning(title='Hi', message='有警告！')  # 提出警告对话窗
        # tkinter.messagebox.showerror(title='Hi', message='出错了！')  # 提出错误对话窗
        # print(tkinter.messagebox.askquestion(title='Hi', message='你好！'))  # 询问选择对话窗return 'yes', 'no'
        # print(tkinter.messagebox.askyesno(title='Hi', message='你好！'))  # return 'True', 'False'
        # print(tkinter.messagebox.askokcancel(title='Hi', message='你好！'))  # return 'True', 'False'
        if tkinter.messagebox.askokcancel(title='mode error', message='是否关闭sink！') == True:
            hvhc["sik_curr"] = 0.0
            sik_curr_val.set(hvhc['sik_curr'])
            sik_para.set('I:' + str(hvhc['sik_curr']))
            hvhc_set("sik", hvhc["src_volt"], hvhc["sik_curr"])
            # time.sleep(100)
        else:
            print('更新电源设置fail')
            return 0
    # print("src debug")
    hvhc_set("src", hvhc["src_volt"], hvhc["src_curr"])
    src_para.set('V: ' + str(hvhc['src_volt']) + '  I: ' + str(hvhc['src_curr']))
    if hvhc['src_curr'] == '0.0':
        hvhc['mode'] = 'idle'
    else:
        hvhc['mode'] = 'src'

# hvhc_en 使能按钮回调函数
def hvhc_en():
    if hvhc_en_bt['text'] == "HVHC已开启":
        hvhc_en_bt['bg'] = 'yellow'
        # hvhc_en_bt['state'] = tk.DISABLED
        hvhc_en_bt['text'] = "HVHC已关闭"
        hvhc['mode'] = 'idle'
        dev_send("hvhc_en(0)")
    else:
        hvhc_en_bt['bg'] = 'green'
        hvhc_en_bt['text'] = "HVHC已开启"
        dev_send("pack_test_init(2.0,0.5,0.5)")
        # dev_send("hvhc_en(1)")

print(hvhc["mode"])


src_volt_val = tk.StringVar()
src_volt_val.set(hvhc['src_volt'])
# 第5步，创建一个尺度滑条，长度200字符，从0开始10结束，以2为刻度，精度为0.01，触发调用print_selection函数
src_volt_sc = tk.Scale(window, width = 60, label='电源 电压', from_=0, to=12, orient=tk.HORIZONTAL, length=200, showvalue=0,
             tickinterval=2, resolution=0.5, command=src_get_volt, variable=src_volt_val).place(x = 0, y = 40)
src_curr_val = tk.StringVar()
src_curr_val.set(hvhc['sik_curr'])
src_curr = tk.Scale(window, width = 60, label='电源 电流', from_=0, to=5, orient=tk.HORIZONTAL, length=200, showvalue=0,
             tickinterval=1, resolution=0.5, command=src_get_curr, variable=src_curr_val).place(x = 0, y = 160)
sik_curr_val = tk.StringVar()
sik_curr_val.set(hvhc['sik_curr'])
sik_curr = tk.Scale(window, width = 60, label='负载 电流', from_=0, to=5, orient=tk.HORIZONTAL, length=200, showvalue=0,
             tickinterval=1, resolution=0.5, command=sik_get_curr, variable=sik_curr_val).place(x = 0, y = 280)

hvhc_en_bt = tk.Button(window, text='HVHC已关闭', bg='yellow', font=('Calibri', 12), width=10, height=4, command=hvhc_en)
hvhc_en_bt.place(x=220, y=50)

src_bt = tk.Button(window, text='电源输出', font=('Calibri', 12), width=10, height=3, command=src_set).place(x=220, y=170)
sik_bt = tk.Button(window, text='负载输入', font=('Calibri', 12), width=10, height=3, command=sik_set).place(x = 220, y = 290)

# tk.Label(window, text='Captain debug panel', font=('Arial', 14)).place(x=200, y=0)
tk.Label(window, text='Password:', font=('Arial', 14)).place(x=500, y=210)
# s.pack()

src_para = tk.StringVar()
src_para.set('V:' + str(hvhc['src_volt']) + '  I:' + str(hvhc['src_curr']))
entry_usr_name = tk.Entry(window, textvariable=src_para, width=9, font=('Arial', 12)).place(x=220, y=240)

sik_para = tk.StringVar()
sik_para.set('I:' + str(hvhc['sik_curr']))
sik_et = tk.Entry(window, textvariable=sik_para, width=9, font=('Arial', 12)).place(x=220, y=360)
# 第7步，主窗口循环显示
window.mainloop()