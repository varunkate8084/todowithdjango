from django.shortcuts import render
from .import pool
from django.http import JsonResponse
# from werkzeug.security import generate_password_hash,check_password_hash
from django.views.decorators.clickjacking import xframe_options_exempt
userid=''
def Log_Out(request):
    # SECURITY PURPOSE
    del request.session['ADMIN']
    return render(request,"login.html")

def Action_LogIn_Page(request):
    return render(request,"login.html")

def Action_Registration_Page(request):
    return render(request,"registration.html")

@xframe_options_exempt
def Action_Main_Page(request):
    try:
       #  For Security
       admin=request.session['ADMIN']
       return render(request,"mainpage.html")
    except:
        print("No Admin")
        return render(request,"login.html")


@xframe_options_exempt
def submit_Registration_Record(request):
   try:
       DB,CMD= pool.ConnectionPooling()
       firstname = request.POST['firstname']
       lastname = request.POST['lastname']
       email= request.POST['email']
       password = request.POST['password']
       # used Hashing
       # password = generate_password_hash(password)
       # print("------------------",password)
       cpassword = request.POST['cpassword']
       phone = request.POST['phone']
       Q="insert into registration(firstname,lastname,password,phone,email) values('{0}','{1}','{2}','{3}','{4}')".format(firstname,lastname,password,phone,email)
       print(Q)
       CMD.execute(Q)
       print(Q)
       return render(request,'registration.html',{'message': 'Record Submitted successfully'})
   except Exception as d:
       print("Error:",d)
       return render(request,'registration.html',{'message': 'Record Submitted unsuccessfully'})
   finally:
       DB.commit()
       DB.close()

@xframe_options_exempt
def Check_LogIn(request):
    try:
        DB, CMD = pool.ConnectionPooling()
        phone = request.POST['phone']
        password = request.POST['password']
        # print("-----------------",password)
        Q = "select * from registration where phone='{0}'and password='{1}'".format(phone,password)
        CMD.execute(Q)
        # print(Q)
        row=CMD.fetchone()

        if(row):
            global userid
            userid=row["userid"]
            print(userid)
            request.session['ADMIN']=row
            return render(request, 'mainpage.html',{'data':row})
        else:
            return render(request, 'login.html', {'message': 'Invalid User Id/Password'})
        DB.close()
    except  Exception as d:
        print("error:", d)
        return render(request, 'login.html', {'message': 'Something went wrong'})

@xframe_options_exempt
def submit_work(request):
   try:
       DB,CMD= pool.ConnectionPooling()
       work = request.POST['work']
       date = request.POST['date']
       status = request.POST['status']
       Q="insert into addwork(work,date,status,userid) values('{0}','{1}','{2}','{3}')".format(work,date,status,userid)
       # print(Q)
       CMD.execute(Q)
       return render(request,'mainpage.html',{'message': 'Record Submitted successfully'})
   except Exception as d:
       print("Error:",d)
   finally:
       DB.commit()
       DB.close()


@xframe_options_exempt
def Display_All_Work(request):
    try:
        admin=request.session['ADMIN']
    except:
        print("No Admin")
        return render(request,"login.html")
    try:
        DB,CMD = pool.ConnectionPooling()
        Q= "select * from addwork where userid = '{0}'".format(userid)
        count="select count(status) from addwork where status='In-Complete' and userid='{0}'".format(userid)
        # print(Q)
        CMD.execute(Q)
        records=CMD.fetchall()
        # to check the form of data
        print(records)
        CMD.execute(count)
        count=CMD.fetchall()
        print(count)
        count = count[0]['count(status)']
        print(count)
        return render(request,'todolist.html',{'records':records,'count':count})
    except Exception as d:
         return render(request,'todolist.html',{'records':None})
    finally:
        DB.close()
def Edit_worklist(request):
    try:
        DB,CMD=pool.ConnectionPooling()
        workid=request.GET['workid']
        workname=request.GET['workname']
        workdate=request.GET['workdate']
        workstatus = request.GET['workstatus']
        Q="update addwork set work='{0}',date='{1}',status='{2}' where workid='{3}'".format(workname,workdate,workstatus,workid)
        # print(Q)
        CMD.execute(Q)
        return JsonResponse({'result':True},safe=False)
    except Exception as d:
        print("Error:",d)
        return JsonResponse({'result':False},safe=False)
    finally:
        DB.commit()
        DB.close()
def Delet_Work(request):
    try:
        DB,CMD=pool.ConnectionPooling()
        workid=request.GET['workid']
        Q="delete from addwork where workid={0}".format(workid)
        print(Q)
        CMD.execute(Q)
        return JsonResponse({'result':True},safe=False)
    except Exception as d:
        print("Error:",d)
        return JsonResponse({'result':False},safe=False)
    finally:
        DB.commit()
        DB.close()





