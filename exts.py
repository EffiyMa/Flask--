# 数据库文件
import pymysql


def mysqlConn():
    conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', passwd='mayifei1997',
        database='edu'
    )
    return conn


# ******************************************************************
# 登陆检查
def loginCheck_stu(username, pwd):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = "select * from s where sno='%s' and s_pwd='%s' " % (username, pwd)
    cur.execute(sql)
    result = cur.fetchall()
    if result is None:
        conn.close()
        return 0
    else:
        conn.close()
        return result


def loginCheck_tchr(username, pwd):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = "select * from t where tno='%s' and t_pwd='%s' " % (username, pwd)
    cur.execute(sql)
    result = cur.fetchone()
    if result is None:
        conn.close()
        return 0
    else:
        conn.close()
        return result


def loginCheck_mangr(username, pwd):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = "select * from m where mno='%s' and m_pwd='%s' " % (username, pwd)
    cur.execute(sql)
    result = cur.fetchone()
    if result is None:
        conn.close()
        return 0
    else:
        conn.close()
        return result


# ********************学生端********************************
def stu_Grade(username):  # 历史成绩，非空
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select sc.semester '学期',sc.cno '课程号',c_name '课程名',
    sum_grade '成绩'from sc,c where sc.cno=c.cno and
    sum_grade is not null and sno='%s' order by sc.cno;''' % (username)
    cur.execute(sql)
    cols = cur.description  # 表头
    result = cur.fetchall()  # 数据
    col_name = []
    scores = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_score = {}
        dict_score['semester'] = item[0]
        dict_score['cno'] = item[1]
        dict_score['c_name'] = item[2]
        dict_score['sum_grade'] = item[3]
        scores.append(dict_score)
    conn.close()
    return col_name, scores


def Class_Info(cno, cname, cdept, tno, tname, credit):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select o.cno '课程号',c.c_name '课程名',c.credit '学分',o.tno '教师号',t.t_name '教师名',d.d_name '专业',c.time '时间' 
          from o,t,c,d where o.tno=t.tno and o.cno=c.cno and c.c_dno=d.dno '''
    str = " "
    if cno != '':
        str += "and o.cno='%s' " % (cno)

    if cname != '':
        str += " and c.c_name='%s' " % (cname)

    if credit != '':
        str += " and c.credit = %d " % (int(credit))

    if tno != '':
        str += " and o.tno = '%s' " % (tno)

    if cdept != '':
        str += " and d.d_name like '%%%s%%' " % (cdept)

    if tname != '':
        str += " and t.t_name like '%%%s%%' " % (tname)
    print(sql + str + "order by 1 ; ")
    cur.execute(sql + str + "order by 1 ; ")
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    info = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_class = {}
        dict_class['cno'] = item[0]
        dict_class['c_name'] = item[1]
        dict_class['credit'] = item[2]
        dict_class['tno'] = item[3]
        dict_class['t_name'] = item[4]
        dict_class['d_name'] = item[5]
        dict_class['time'] = item[6]
        info.append(dict_class)
    conn.close()
    return col_name, info


def Class_select(username, cno1, tno1, cno2, tno2):  # 选课
    conn = mysqlConn()
    cur = conn.cursor()
    if cno1 != '' and tno1 != '':  # 如果执行
        flag1 = True  # 表示执行了
        try:
            sql = "insert into sc(semester,sno, cno,tno, ps_grade,ks_grade,sum_grade) values ('2017-2018 春季','%s','%s','%s',NULL ,NULL,NULL);" % (
                username, cno1, tno1)
            stat1 = cur.execute(sql)
        except:
            stat1 = 0
    else:  # 如果不执行
        flag1 = False
        stat1 = 0
    if cno2 != '' and tno2 != '':
        flag2 = True
        try:
            sql = "insert into sc(semester,sno, cno,tno, ps_grade,ks_grade,sum_grade) values ('2017-2018 春季','%s','%s','%s',NULL ,null ,null );" % (
                username, cno2, tno2)
            stat2 = cur.execute(sql)
        except:
            stat2 = 0
    else:
        flag2 = False
        stat2 = 0
    conn.commit()
    cur.close()
    conn.close()
    return flag1, flag2, stat1, stat2


def Selected_info(username,semester):  # 返回已选课程
    conn = mysqlConn()
    cur = conn.cursor()
    sql = " select sc.cno '课程号',c.c_name '课程名',c.credit '学分',sc.tno '教师号',t.t_name '教师名' from sc,c,t where sc.cno=c.cno and sc.tno=t.tno and sc.sno ='%s' and semester='%s';" % (
        username,semester)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    info = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_info = {}
        dict_info['cno'] = item[0]
        dict_info['c_name'] = item[1]
        dict_info['credit'] = item[2]
        dict_info['tno'] = item[3]
        dict_info['t_name'] = item[4]
        info.append(dict_info)
    conn.close()
    return col_name, info


def Class_drop(username, list):
    conn = mysqlConn()
    cur = conn.cursor()
    sta = 1
    print(list)
    for item in list:
        print(item)
        sql = "delete from sc where sc.semester='2017-2018 春季' and sc.sno='%s' and sc.cno='%s' and sc.tno='%s';" % (
            username, item['cno'], item['tno'])
        last = cur.execute(sql)
        sta = sta and last
    conn.commit()  # 一定不要忘，只有commit数据库才有改变！
    cur.close()
    conn.close()
    return sta


def Get_posts():
    conn = mysqlConn()
    cur = conn.cursor()
    sql = "select title , content, t_name, time from Note natural join t;"
    cur.execute(sql)
    result = cur.fetchall()
    info = []
    for item in result:
        dict_info = {}
        dict_info['title'] = item[0]
        dict_info['content'] = item[1]
        dict_info['t_name'] = item[2]
        dict_info['time'] = item[3]
        info.append(dict_info)
    conn.close()
    return info


# **********教师端***************
def tchr_Class_view(username):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select o.semester '学期',o.cno '课程号',c.c_name '课程名',c.credit '学分',c.time '时间',d.d_name '所属专业',count(*) '选修人数'
    from o ,sc, c , d
    where o.cno=c.cno and c.c_dno=d.dno
      and o.semester=sc.semester and o.cno=sc.cno and o.tno=sc.tno and o.tno='%s'
group by o.semester,o.cno
order by 1 asc ;''' % (username)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    cls = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_clss = {}
        dict_clss['semester'] = item[0]
        dict_clss['cno'] = item[1]
        dict_clss['c_name'] = item[2]
        dict_clss['credit'] = item[3]
        dict_clss['time'] = item[4]
        dict_clss['d_name'] = item[5]
        dict_clss['number'] = item[6]
        cls.append(dict_clss)
    conn.close()
    return col_name, cls


def tchr_semester_view():  # 返回学期
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select distinct o.semester '学期' from o;'''
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    sem = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_sem = {}
        dict_sem['semester'] = item[0]
        sem.append(dict_sem)
    conn.close()
    return col_name, sem


def tchr_Stu(semester, username, cno, cname):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select o.semester '学期',o.cno '课程号',c.c_name '课程名',sc.sno '学号',s.s_name '姓名',d.d_name '学院'
from o,sc,c,s,d
where o.cno=sc.cno and sc.cno=c.cno and o.tno=sc.tno and sc.sno=s.sno and s.s_dno=d.dno and o.tno='%s'  ''' % (username)
    if semester != 'None':
        sql += " and o.semester='%s'  " % (semester)

    if cno != 'None' and cname != 'None':
        sql += " and o.cno='%s' and c.c_name= '%s';  " % (cno, cname)
    elif cno != 'None' and cname == 'None':
        sql += " and o.cno='%s' ;  " % (cno)
    elif cno == 'None' and cname != 'None':
        sql += " and c.c_name='%s' ;  " % (cname)
    elif cno == 'None' and cname == 'None':
        sql += " ; "
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    stu_list = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_stu = {}
        dict_stu['semester'] = item[0]
        dict_stu['cno'] = item[1]
        dict_stu['c_name'] = item[2]
        dict_stu['sno'] = item[3]
        dict_stu['s_name'] = item[4]
        dict_stu['d_name'] = item[5]
        stu_list.append(dict_stu)
    conn.close()
    return col_name, stu_list


def Grade_in_stu(semester, username, cno):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select sc.semester '学期',sc.cno '课号',c.c_name '课名',sc.sno '学号',s.s_name '姓名',d.d_name '学院'
    from sc,s,c,d
    where sc.cno=c.cno and sc.sno=s.sno and s.s_dno=d.dno and sc.semester='%s' and sc.tno='%s' and sc.cno='%s' and (sc.ps_grade is null or sc.ks_grade is null); ''' \
          % ( semester, username, cno)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    stu_list = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_stu = {}
        dict_stu['semester'] = item[0]
        dict_stu['cno'] = item[1]
        dict_stu['c_name'] = item[2]
        dict_stu['sno'] = item[3]
        dict_stu['s_name'] = item[4]
        dict_stu['d_name'] = item[5]
        stu_list.append(dict_stu)
    conn.close()
    return col_name, stu_list


def Grade_update(semester, ps_grade, ks_grade, username, sno, cno):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = " update sc set ps_grade=%d,ks_grade=%d where semester='%s' and tno='%s' and sno='%s' and cno='%s'; "% (ps_grade,ks_grade,semester,username, sno, cno)
    sta = cur.execute(sql)
    conn.commit()
    conn.close()
    return sta


def Grade_search(semester, username, cno):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select sc.sno '学号' ,s.s_name '姓名',d.d_name '专业',sc.sum_grade '成绩'
from sc,s,d
where sc.sno=s.sno and s.s_dno=d.dno and sum_grade is not null 
    and sc.semester='%s' and sc.cno='%s' and sc.tno='%s'; ''' % (semester, cno, username)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    scores = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_score = {}
        dict_score['sno'] = item[0]
        dict_score['s_name'] = item[1]
        dict_score['d_name'] = item[2]
        dict_score['grade'] = item[3]
        scores.append(dict_score)
    conn.close()
    return col_name, scores


def Grade_statistic(semester, username, cno):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select
  sum(case when sum_grade<60 then 1 else null end ) '<60',
  sum(case when sum_grade>=60 and sum_grade<70 then 1 else null end) '60-70',
  sum(case when sum_grade>=70 and sum_grade<80 then 1 else null end) '70-80',
  sum(case when sum_grade>=80 and sum_grade<90 then 1 else null end) '80-90',
  sum(case when sum_grade>=90 then 1 else null end) '>=90'
from sc
where sc.semester='%s'and sc.cno='%s' and sc.tno='%s'; ''' % (semester, cno, username)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    scores = []
    for item in cols:
        col_name.append(item[0])
    print("col_name", col_name, "result", result)
    for item in result:
        dict_score = {}
        dict_score['E'] = (0 if (item[0] == None) else int(item[0]))  # <60
        dict_score['D'] = (0 if (item[1] == None) else int(item[1]))  # 60-70
        dict_score['C'] = (0 if (item[2] == None) else int(item[2]))  # 70-80
        dict_score['B'] = (0 if (item[3] == None) else int(item[3]))  # 80-90
        dict_score['A'] = (0 if (item[4] == None) else int(item[4]))  # 90-100
        scores.append(dict_score)
    conn.close()
    print("scores: ", scores)
    return scores


def Post_notice(username, title, content):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''INSERT INTO Note(title, content, tno) VALUES ('%s','%s','%s'); ''' % (title, content, username)
    sta = cur.execute(sql)
    conn.commit()
    conn.close()
    return sta


def Get_teacherposts(username):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = "select id, title , content, t_name, time  from Note natural join t where tno='%s' ;" % (username)
    cur.execute(sql)
    result = cur.fetchall()
    info = []
    for item in result:
        dict_info = {}
        dict_info['id'] = item[0]
        dict_info['title'] = item[1]
        dict_info['content'] = item[2]
        dict_info['t_name'] = item[3]
        dict_info['time'] = item[4]
        info.append(dict_info)
    conn.close()
    return info


def Post_drop(drop_list):
    conn = mysqlConn()
    cur = conn.cursor()
    sta = 1
    for id in drop_list:
        sql = "delete from note where id=%d;" % (int(id))
        last = cur.execute(sql)
        sta = sta and last
    conn.commit()
    cur.close()
    conn.close()
    return sta


# *********************管理员端***************************
def mang_depart():  # 历史成绩，非空
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select d.dno '院系号',d.d_name '院系号',d.address '地址',d.phone '电话' from d;'''
    cur.execute(sql)
    cols = cur.description  # 表头
    result = cur.fetchall()  # 数据
    col_name = []
    department = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_depart = {}
        dict_depart['dno'] = item[0]
        dict_depart['d_name'] = item[1]
        dict_depart['address'] = item[2]
        dict_depart['phone'] = item[3]
        department.append(dict_depart)
    conn.close()
    return col_name, department


def Get_Teacher():
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select  t.tno '教师号',t.t_name '教师姓名',t.background '职称',d.d_name '所属院系' from t left join d on T.t_dno = D.dno;'''
    cur.execute(sql)
    cols = cur.description  # 表头
    result = cur.fetchall()  # 数据
    col_name = []
    tchr_list = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_tchr = {}
        dict_tchr['tno'] = item[0]
        dict_tchr['t_name'] = item[1]
        dict_tchr['background'] = item[2]
        dict_tchr['d_name'] = item[3]
        tchr_list.append(dict_tchr)
    conn.close()
    return col_name, tchr_list

def Get_Stu():
    conn=mysqlConn()
    cur=conn.cursor()
    sql='''select s.sno '学号',s.s_name '姓名', s.hometown '生源地',d.d_name '院系', s.phone '联系电话'
      from s,d where s.s_dno=d.dno order by 1 asc ;'''
    cur.execute(sql)
    result=cur.fetchall()
    cols=cur.description
    col_name=[]
    stu_list=[]
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_class={}
        dict_class['sno']=item[0]
        dict_class['s_name']=item[1]
        dict_class['hometown']=item[2]
        dict_class['d_name']=item[3]
        dict_class['phone']=item[4]
        stu_list.append(dict_class)
    conn.close()
    return col_name,stu_list

def mang_Class_view():
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select c.cno '课程号',c.c_name '课程名',c.credit '学分',c.period '课时',d.d_name '学院',c.time '上课时间'
        from c left join d on c.c_dno=d.dno
        order by 1 desc ;'''
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    cls = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_clss = {}
        dict_clss['cno'] = item[0]
        dict_clss['c_name'] = item[1]
        dict_clss['credit'] = item[2]
        dict_clss['period'] = item[3]
        dict_clss['d_name'] = item[4]
        dict_clss['time'] = item[5]
        cls.append(dict_clss)
    conn.close()
    return col_name, cls


def mang_open_Class_view(semester, cno):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select distinct o.cno '课程号',c.c_name '课程名',o.tno '教师号',t.t_name '教师名'
            from o,c,t
            where o.tno=t.tno and o.cno=c.cno and o.semester='%s' and o.cno='%s'
            order by 3 ;''' % (semester, cno)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    open_cls = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_clss = {}
        dict_clss['cno'] = item[0]
        dict_clss['c_name'] = item[1]
        dict_clss['tno'] = item[2]
        dict_clss['t_name'] = item[3]
        open_cls.append(dict_clss)
    conn.close()
    return col_name, open_cls

def mang_all_open_Class(semester):
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select o.cno '课程号',c.c_name '课程名',o.tno '教师号',t.t_name '教师名'
                from o,c,t
                where o.tno=t.tno and o.cno=c.cno and o.semester='%s' order by 1;''' % (semester)
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    all_open_cls = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_clss = {}
        dict_clss['cno'] = item[0]
        dict_clss['c_name'] = item[1]
        dict_clss['tno'] = item[2]
        dict_clss['t_name'] = item[3]
        all_open_cls.append(dict_clss)
    conn.close()
    return col_name, all_open_cls



# 添加课程
def Class_add(cno, cname, credit, period, depart, time):  # 选课
    conn = mysqlConn()
    cur = conn.cursor()
    try:
        sql = "insert into c(cno, c_name, credit,period,c_dno, time) values ('%s','%s','%s','%s','%s','%s' );" % (cno, cname, credit, period, depart, time)
        stat = cur.execute(sql)
    except:
        stat = 0
    conn.commit()
    cur.close()
    conn.close()
    return stat

def mang_del_Class(drop_list):#是一个列表 ['C2', 'C1']
    conn = mysqlConn()
    cur = conn.cursor()
    sta = 1
    for cno in drop_list:
        try:
            sql = "delete from c where c.cno='%s';" % (cno)
            last = cur.execute(sql)
        except:
            last=0
        sta = sta and last
    conn.commit()
    cur.close()
    conn.close()
    return sta

def mang_Class_only():
    conn = mysqlConn()
    cur = conn.cursor()
    sql = '''select distinct c.cno '课程号',c.c_name '课程名'
                from c;'''
    cur.execute(sql)
    result = cur.fetchall()
    cols = cur.description
    col_name = []
    cls = []
    for item in cols:
        col_name.append(item[0])
    for item in result:
        dict_clss = {}
        dict_clss['cno'] = item[0]
        dict_clss['c_name'] = item[1]
        cls.append(dict_clss)
    conn.close()
    return col_name, cls


def Open_class_add(cno,tno1,tno2):
    print(cno,tno1,tno2)
    conn = mysqlConn()
    cur = conn.cursor()
    if cno!= '' and tno1 != '':  # 如果加了一个老师
        flag1 = True  # 表示执行了
        try:
            sql = "insert into o values ('2017-2018 春季','%s','%s');" % (cno, tno1)
            stat1 = cur.execute(sql)
            print('stat1',stat1)
        except:
            stat1 = 0
    else:  # 如果不执行
        flag1 = False
        stat1 = 0
    if cno != '' and tno2 != '':
        flag2 = True
        try:
            sql = "insert into o values ('2017-2018 春季','%s','%s');" % (cno, tno2)
            stat2 = cur.execute(sql)
            print('stat2', stat2)
        except:
            stat2 = 0
    else:
        flag2 = False
        stat2 = 0
    conn.commit()
    cur.close()
    conn.close()
    return flag1, flag2, stat1, stat2

def del_open_Class(del_list):
    conn = mysqlConn()
    cur = conn.cursor()
    sta =1
    for opt in del_list:
        try:
            sql = "delete from o where o.semester='2017-2018 春季' and o.cno='%s' and o.tno='%s';" % (opt['cno'],opt['tno'])
            last = cur.execute(sql)#本条执行情况
        except:
            last = 0
        sta = sta and last
    conn.commit()
    cur.close()
    conn.close()
    return sta