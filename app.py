from flask import Flask, request, render_template, session, redirect, url_for
import os
# import pyecharts
from decorators import login_required
from exts import loginCheck_stu, loginCheck_tchr, loginCheck_mangr
from exts import stu_Grade, Class_Info, Selected_info, Class_select, Class_drop, Get_posts
from exts import tchr_Class_view, tchr_semester_view, tchr_Stu, Grade_in_stu, Grade_update, Grade_search, \
    Grade_statistic, Post_notice, Get_teacherposts, Post_drop
from exts import mang_depart, Get_Teacher,Get_Stu, mang_Class_view, mang_open_Class_view, Class_add,mang_del_Class,\
    Open_class_add,mang_all_open_Class,del_open_Class

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)



# 上下文处理器钩子函数
@app.context_processor
def my_contest_processor():
    username = session.get('username')
    if username:
        return dict(user=username)
    else:
        return {}  # 没登陆，空字典


# 启动服务器后运行的第一个函数，显示对应网页内容
@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))


# 登陆页面
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    pwd = request.form['password']
    if username[0] == '1':  # 开头1的是学生
        data1 = loginCheck_stu(username, pwd)
        print('data1', data1)
        if data1:  # 登陆成功
            session['username'] = username
            sta = 1
            return render_template("student_index.html", sta=sta)
    elif username[0] == '0':  # 开头2的是老师
        data2 = loginCheck_tchr(username, pwd)
        print('data2', data2)
        if data2:  # 登陆成功
            session['username'] = username
            sta = 1
            return render_template("teacher_index.html", sta=sta)
    elif username[0] == '2':  # 开头2的是管理员
        data3 = loginCheck_mangr(username, pwd)
        print('data3', data3)
        if data3:  # 登陆成功
            session['username'] = username
            sta = 1
            return render_template("admin_index.html", sta=sta)

    return render_template("login.html")


# 登出
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


# *********************学生端**************************
# 学生首页
@app.route('/student/index/', methods=['GET'])
def student_index():
    return render_template('student_index.html')


# 学生成绩总汇
@app.route('/student/grade/', methods=['GET'])
@login_required
def student_grade():
    # username = session.get('username')
    # print('username', username)
    username = '16122000'
    grade_info = stu_Grade(username)
    print(grade_info)
    col_name = grade_info[0]
    score = grade_info[1]
    # print(grade_info)
    # print(col_name)
    # print(score)
    return render_template('student_grade.html', col_name=col_name, score=score)


# 学生开课信息
@app.route('/student/class/', methods=['GET', 'POST'])
@login_required
def student_class():
    if request.method == 'GET':
        return render_template('student_class.html')
    else:
        # 获得输入框内容
        cno = request.form.get('c_no', type=str)
        cname = request.form.get('c_name', type=str)
        cdept = request.form.get('c_dept', type=str)
        tno = request.form.get('t_no', type=str)
        tname = request.form.get('t_name', type=str)
        credit = request.form.get('c_credit', type=str)
        list = Class_Info(cno, cname, cdept, tno, tname, credit)
        col_name = list[0]
        info = list[1]
        # print(col_name)
        # print(info)
        return render_template('student_class.html', col_name=col_name, info=info)


# 学生选课,返回已选的课程
@app.route('/student/select/', methods=['GET', 'POST'])
@login_required
def student_select():
    username = session.get('username')
    semester='2017-2018 春季'
    if request.method == 'GET':
        cls_list = Selected_info(username,semester)
        col_name = cls_list[0]
        info = cls_list[1]
        return render_template('student_select.html', col_name=col_name, info=info)
    else:
        cno1 = request.form.get('c_no1', type=str)
        tno1 = request.form.get('t_no1', type=str)
        cno2 = request.form.get('c_no2', type=str)
        tno2 = request.form.get('t_no2', type=str)
        sta_list = Class_select(username, cno1, tno1, cno2, tno2)  # flag1,flag2,stat1, stat2
        # print(sta_list)
        cls_list = Selected_info(username,semester)
        col_name = cls_list[0]
        info = cls_list[1]
        return render_template('student_select.html', sta_list=sta_list, col_name=col_name, info=info)


# 学生退课
@app.route('/student/drop/', methods=['GET', 'POST'])
@login_required
def student_drop():
    username = session.get('username')
    semester='2017-2018 春季'
    # username = '16122000'
    if request.method == 'GET':
        cls_list = Selected_info(username,semester)  # 获取已选的课程
        col_name = cls_list[0]
        info = cls_list[1]
        return render_template('student_drop.html', col_name=col_name, info=info)
    else:  # 发送所要退的课
        drop_list = request.form.getlist("chk_box")  # request.POST.getlist(key)获取一个列表,request.POST.get(key)获取的是最后一个值
        # print(drop_list) #['C18,00022003', 'C20,00022005', 'C7,00022007']
        list = [ ]
        for one in drop_list:
            cno = one[:-9]
            tno = one[-8:]
            list.append({'cno': cno, 'tno': tno})
        sta = Class_drop(username, list)
        print('****', sta)
        cls_list = Selected_info(username,semester)  # 获取已选的课程
        col_name = cls_list[0]
        info = cls_list[1]
    # return "hello"
    return render_template('student_drop.html', sta=sta, col_name=col_name, info=info)


@app.route('/student/notice/', methods=['GET'])
def stu_notice_view():
    posts = Get_posts()
    return render_template('student_noticeboard.html', posts=posts)


# *********教师**************************
# 教师登陆首页
@app.route('/teacher/index/', methods=['GET'])
def teacher_index():
    return render_template('teacher_index.html')


# 教师历年教学计划
@app.route('/teacher/class/', methods=['GET'])
@login_required
def teacher_class():
    # username = session.get('username')
    username = '00022000'
    list = tchr_Class_view(username)
    col_name = list[0]  # 信息行
    cls_info = list[1]  # 数据
    # print(list)
    # print(len(cls_info))
    return render_template('teacher_class.html', col_name=col_name, cls_info=cls_info)


# 查看某班级学生
@app.route('/teacher/stu_search/', methods=['GET', 'POST'])
@login_required
def stu_search():
    username = session.get('username')
    username = '00022000'
    # semester='2017-2018 春季'
    sem_list = tchr_semester_view()  # 学期
    sem_info = sem_list[1]
    class_list = tchr_Class_view(username)  # 班级
    cls_info = class_list[1]
    print(cls_info)
    if request.method == 'POST':
        sem = request.form.get('sem')
        cno = request.form.get('cno')
        cname = request.form.get('cname')
        # print(cno, cname)
        list2 = tchr_Stu(sem, username, cno, cname)
        col_name = list2[0]
        stu_list = list2[1]
        # print(stu_list)
        return render_template('teacher_stusearch.html', sem_info=sem_info, cls_info=cls_info, col_name=col_name,
                               stu_list=stu_list)
    return render_template('teacher_stusearch.html', sem_info=sem_info, cls_info=cls_info)


# 教师输入成绩总功能
@app.route('/teacher/grade/', methods=['GET', 'POST'])
@login_required
def teacher_grade():
    # username = session.get('username')
    username = '00022000'
    # semester='2017-2018 春季'
    list = tchr_Class_view(username)  # 所有班级
    col_name = list[0]
    cls_info = list[1]
    return render_template('teacher_grade.html', col_name=col_name, cls_info=cls_info)


# 成绩输入
@app.route('/teacher/grade_input/<semester>/<cno>/', methods=['GET', 'POST'])
@login_required
def grade_input(semester, cno):
    # username = session.get('username')
    username = '00022000'
    # print(cno)
    list = Grade_in_stu(semester, username, cno)  # 选课同学，输入成绩
    print(list)
    col_name = list[0]
    stu_info = list[1]
    flg = 0
    # print('colname=',col_name)
    # print('stu_info=', stu_info)
    if request.method == 'POST':  # 提交成绩
        ps_grade_list = request.form.getlist('ps_grade')  # request.form.get和getlist方法都要在html中form的method=post的时候才能获得数据
        ks_grade_list = request.form.getlist('ks_grade')
        # print(ps_grade_list)
        # print(ks_grade_list)
        i = 0
        sta = 1
        for k in range(len(ps_grade_list)):  # 每一个提交的成绩
            if ps_grade_list[k] != '' and ks_grade_list[k]!='':  # 有成绩提交
                print(semester, int(ps_grade_list[k]),int(ks_grade_list[k]) , username, stu_info[i].get('sno'), cno)
                last = Grade_update(semester, int(ps_grade_list[k]),int(ks_grade_list[k]) , username, stu_info[i].get('sno'), cno)  # 教师号，获取学号
                print(last)
                sta = sta and last
                i = i + 1
        if (i + 1) == len(stu_info) and sta == 1:
            flg = 1  # 全部成绩录入且成功
        elif i != 0 and sta == 1:
            flg = 2  # 部分成绩全部录入且成功
        elif i == 0:
            flg = 3  # 无成绩修改,flg = 3

        list = Grade_in_stu(semester, username, cno)  # 重新刷新
        col_name = list[0]
        stu_info = list[1]
        return render_template('teacher_grade_input.html', col_name=col_name, stu_info=stu_info, flg=flg)
    return render_template('teacher_grade_input.html', col_name=col_name, stu_info=stu_info, flg=flg)


# 成绩查看
@app.route('/teacher/grade_view/<semester>/<cno>/', methods=['GET'])
@login_required
def grade_view(semester, cno):
    # username = session.get('username')
    username = '00022000'
    grade_list = Grade_search(semester, username, cno)
    # print('Grade_LIST:',grade_list)
    col_name1 = grade_list[0]
    grade_info = grade_list[1]
    gra_count_list = Grade_statistic(semester, username, cno)
    gra_count_list = list(gra_count_list)
    print("gra_count_list:", gra_count_list)

    # 用过pyecharts统计用
    # print(list)
    # print(len(cls_info))
    return render_template('teacher_score_view.html', col_name1=col_name1, grade_info=grade_info,
                           gra_count_list=gra_count_list, semester=semester)

@app.route('/teacher/notice/', methods=['GET', 'POST'])
@login_required
def notice_board():
    # username = session.get('username')
    username = '00022000'
    if request.method == 'GET':
        return render_template('teacher_notice.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        sta = Post_notice(username, title, content)
        return render_template('teacher_notice.html', sta=sta)


# 教师查看我的发布
@app.route('/teacher/notice_view/', methods=['GET', 'POST'])
@login_required
def notice_view():
    # username = session.get('username')
    username = '00022000'
    if request.method == 'GET':
        info = Get_teacherposts(username)
        print(info)
        return render_template('teacher_boardview.html', info=info)
    else:
        drop_list = request.form.getlist("chk_box")
        sta = Post_drop(drop_list)
        info = Get_teacherposts(username)
        return render_template('teacher_boardview.html', sta=sta, info=info)


# *********************管理员端**************************
@app.route('/manager/index/', methods=['GET'])  # 管理员登陆首页
def manager_index():
    return render_template('admin_index.html')


# 院系一览
@app.route('/manager/department/', methods=['GET'])
@login_required
def manager_depart():
    # username = session.get('username')
    # print('username', username)
    username = '20022000'
    depart_info = mang_depart()
    col_name = depart_info[0]
    depart = depart_info[1]
    return render_template('admin_depart.html', col_name=col_name, depart=depart)


# 教师信息查看
@app.route('/manager/teacher/', methods=['GET'])
@login_required
def manager_tchr():
    # username = session.get('username')
    # print('username', username)
    username = '20022000'
    tchr_info = Get_Teacher()
    col_name = tchr_info[0]
    tchr_list = tchr_info[1]
    return render_template('admin_tchr.html', col_name=col_name, tchr_list=tchr_list)

#学生信息
@app.route('/manager/student/', methods=['GET'])
@login_required
def manager_stu():
    # username = session.get('username')
    # print('username', username)
    username = '20022000'
    stu_info = Get_Stu()
    col_name = stu_info[0]
    stu_list = stu_info[1]
    return render_template('admin_stu.html', col_name=col_name, stu_list=stu_list)

#课程和开课查看
@app.route('/manager/class/', methods=['GET'])
@login_required
def manager_class():
    # username = session.get('username')
    username = '00022000'
    semester = '2017-2018 春季'
    list = mang_Class_view()  # 所有课程目录
    col_name = list[0]
    cls_info = list[1]
    return render_template('admin_class.html', semester=semester, col_name=col_name, cls_info=cls_info)

#开课查看
@app.route('/manager/open_class/<semester>/<cno>/', methods=['GET'])
@login_required
def manager_open_class(semester, cno):
    # username = session.get('username')
    username = '00022000'
    semester = '2017-2018 春季'
    list = mang_open_Class_view(semester, cno)  # 所有课程目录
    col_name = list[0]
    cls_info = list[1]
    return render_template('admin_open_class.html', semester=semester, col_name=col_name, cls_info=cls_info)

#加C表课程
@app.route('/manager/add_class/', methods=['GET', 'POST'])
@login_required
def manager_class_add():
    # username = session.get('username')
    username = '00022000'
    semester = '2017-2018 春季'
    if request.method == 'GET':  # 获得所有已有C表课程
        cls_list = mang_Class_view()
        col_name = cls_list[0]
        info = cls_list[1]
        depart = mang_depart()
        depart_list = depart[1]
        return render_template('admin_add_class.html', col_name=col_name, info=info, depart_list=depart_list)
    else:
        cno = request.form.get('c_no', type=str)
        cname = request.form.get('c_name', type=str)
        credit = request.form.get('c_redit', type=str)
        period = request.form.get('p_eriod', type=str)
        depart = request.form.get('d_epart', type=str)
        time = request.form.get('t_ime', type=str)
        sta = Class_add(cno, cname, credit, period, depart, time)
        cls_list = mang_Class_view()
        col_name = cls_list[0]
        info = cls_list[1]
        depart = mang_depart()
        depart_list = depart[1]
        return render_template('admin_add_class.html', sta=sta, col_name=col_name, info=info, depart_list=depart_list)

#删除C表课程
@app.route('/manager/del_class/', methods=['GET', 'POST'])
@login_required
def mang_class_delete():
    # username = session.get('username')
    username = '20022000'
    if request.method == 'GET':  # 获得所有已有C表课程
        cls_list = mang_Class_view()
        col_name = cls_list[0]
        info = cls_list[1]
        return render_template('admin_del_class.html', col_name=col_name, info=info)
    else:  # 发送所要退的课
        drop_list = request.form.getlist("chk_box")
        print(drop_list)
        sta = mang_del_Class(drop_list)
        print('****', sta)
        cls_list = mang_Class_view()
        col_name = cls_list[0]
        info = cls_list[1]
        return render_template('admin_del_class.html', sta=sta, col_name=col_name, info=info)


#添加O表课程
@app.route('/manager/add_open_class/', methods=['GET', 'POST'])
@login_required
def manager_open_class_add():
    # username = session.get('username')
    username = '00022000'
    semester = '2017-2018 春季'
    if request.method == 'GET':  # 获得所有已有C表课程
        cls_list = mang_Class_view()
        cls = cls_list[1]
        List=mang_all_open_Class(semester)
        col_name=List[0]
        All_open=List[1]
        return render_template('admin_add_open_class.html', col_name=col_name, cls=cls,All_open=All_open)
    else:
        cno = request.form.get('c_lass', type=str)
        tno1 = request.form.get('t_no1', type=str)
        tno2 = request.form.get('t_no2', type=str)
        sta=Open_class_add(cno,tno1,tno2)
        cls_list = mang_Class_view()
        cls = cls_list[1]
        List = mang_all_open_Class(semester)
        col_name = List[0]
        All_open = List[1]
        return render_template('admin_add_open_class.html', sta=list(sta),col_name=col_name, cls=cls,All_open=All_open)

# 开课删除
@app.route('/manager/del_open_class/', methods=['GET', 'POST'])
@login_required
def mang_del_open_class():
    # username = session.get('username')
    username = '20022000'
    semester = '2017-2018 春季'
    if request.method == 'GET':  # 获得所有已有C表课程
        List = mang_all_open_Class(semester)
        col_name = List[0]
        All_open = List[1]
        return render_template('admin_del_open_class.html', col_name=col_name, All_open=All_open)
    else:  # 发送所要退的开课
        drop_list = request.form.getlist("chk_box")
        # print(drop_list) #['C1,00022000', 'C8,00022000']
        del_list = [ ]
        for one in drop_list:
            cno=one[:-9]
            tno = one[-8:]
            del_list.append({'cno':cno,'tno':tno})
        sta = del_open_Class(del_list)
        List = mang_all_open_Class(semester)
        col_name = List[0]
        All_open = List[1]
        return render_template('admin_del_open_class.html', sta=sta, col_name=col_name, All_open=All_open)


if __name__ == '__main__':
    app.run()
