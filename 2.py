import requests
import json
import tkinter as tk
from tkinter import messagebox

# 创建主窗口
root = tk.Tk()
root.title("学习通我踏马刷刷刷")
root.geometry("400x300")

# 定义全局变量
cookies = None
courseid = None
clazzid = None
personid = None
chapterid = None
course_name = None
selected_course = None  # 存储已选择的课程信息

def login(username, password):
    # 登录学习通
    url = "http://114.132.51.87:3001/chaoxing/login"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    params = {
        "uname": username,
        "password": password
    }
    response = requests.get(url, params=params, headers=headers)
    global cookies
    cookies = response.cookies
    return response.status_code, response.text

def get_course():
    # 获取所有课程
    url = "http://114.132.51.87:3001/chaoxing/course"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    session = requests.session()
    global cookies
    response = session.get(url, headers=headers, cookies=cookies)
    return response.status_code, response.text

def getids(course_name, course_list):
    # 获取courseid, personid, clazzid
    global selected_course
    selected_course = None
    for course in course_list:
        if course["name"] == course_name:
            selected_course = course
            break

    if selected_course is None:
        print('输入有误，未找到此课程')
        exit()

    global courseid
    global personid
    global clazzid
    courseid = selected_course["courseid"]
    personid = selected_course["personid"]
    clazzid = selected_course["clazzid"]

def su_all(username):
    url = "http://114.132.51.87:3001/chaoxing/auto"
    global courseid
    global clazzid
    global personid
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    params = {
        "courseId": courseid,
        "clazzid": clazzid,
        "personid": personid,
        "uname": username
    }
    session = requests.session()
    global cookies
    response = session.get(url, params=params, headers=headers, cookies=cookies)
    return response.status_code, response.text

def login_submit_action():
    username = username_entry.get()
    password = password_entry.get()

    code_login, back_text = login(username, password)
    if code_login == 200:
        # 登录成功
        code_course_f, course = get_course()
        course = json.loads(course)

        if code_course_f == 200:
            if course["code"] == 200:
                global course_list
                course_list = course["data"]
                show_course_selection()
            else:
                messagebox.showerror("登录失败", "登录失败，请检查用户名和密码")
        else:
            messagebox.showerror("登录失败", "登录失败，请检查用户名和密码")
    else:
        messagebox.showerror("登录失败", "登录失败，请检查用户名和密码")

def show_course_selection():
    # 隐藏登录界面
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    login_button.pack_forget()
    shuoming1_button.pack_forget()
    shuoming2_button.pack_forget()
    shuoming3_button.pack_forget()
    shuoming4_button.pack_forget()

    # 显示查询课程按钮
    get_course_button = tk.Button(root, text="查询课程", command=display_course_list)
    get_course_button.pack()

def display_course_list():
    global course_list
    course_label = tk.Label(root, text="请选择课程：")
    course_label.pack()

    course_selection = tk.StringVar()
    course_selection.set("请选择")
    course_menu = tk.OptionMenu(root, course_selection, *[course["name"] for course in course_list], command=set_course_name)
    course_menu.pack()

    global course_entry
    course_entry = tk.Entry(root)
    course_entry.pack()

    submit_button = tk.Button(root, text="提交", command=lambda: submit_action(course_selection.get()))
    submit_button.pack()


def set_course_name(course_name_selected):
    global course_name
    course_name = course_name_selected
    course_entry.delete(0, tk.END)
    course_entry.insert(0, course_name)

def submit_action(selected_course_name):
    username = username_entry.get()
    password = password_entry.get()

    code_login, back_text = login(username, password)
    if code_login == 200:
        # 登录成功
        global course_name

        # 根据选择的课程名称获取courseid
        getids(selected_course_name, course_list)
        if selected_course is not None:
            code_all, text_bac = su_all(username)
            if code_all == 200:
                json_all = json.loads(text_bac)
                code_final = json_all["code"]
                if code_final == 200:
                    messagebox.showinfo("操作成功", f"你的 [{selected_course_name}] 提交成功，请耐心等待")
                else:
                    messagebox.showerror("执行失败", "出现错误")
            else:
                messagebox.showerror("服务器错误", "服务器错误404")
        else:
            messagebox.showerror("课程不存在", "输入的课程名不存在，请重新输入")
    else:
        messagebox.showerror("登录失败", "登录失败，请检查用户名和密码")

def callback(url):
    import webbrowser
    webbrowser.open_new(url)

# 创建登录界面的元素
username_label = tk.Label(root, text="账号：")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="密码：")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="登录", command=login_submit_action)
login_button.pack()


hallo_button = tk.Label(root, text="有问题请找夬（点击我跳转）", fg="blue", cursor="hand2")
hallo_button.pack()
hallo_button.bind("<Button-1>", lambda e: callback("https://www.yinguai.art/"))

shuoming1_button = tk.Label(root, text="这是一个能够快速完成你的大专课程的项目", fg="red", cursor="hand2")
shuoming1_button.pack()

shuoming2_button = tk.Label(root, text="除了题目考试应该都能刷（任务点），一般一门课10min左右", fg="green", cursor="hand2")
shuoming2_button.pack()

shuoming3_button = tk.Label(root, text="请勿短时间内多次提交，等待一门课程刷好后在继续下一门", fg="green", cursor="hand2")
shuoming3_button.pack()

shuoming4_button = tk.Label(root, text="点击提交后程序可随时退出，刷课是在服务器上进行的", fg="green", cursor="hand2")
shuoming4_button.pack()

# 运行主循环
root.mainloop()
