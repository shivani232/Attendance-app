# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from app import models
from datetime import datetime,timedelta
from django.core.mail import send_mail
from django.conf import settings
import random
import pygal
from pygal.style import Style
from django.template import RequestContext

# Create your views here.


@csrf_exempt
def start(request):
	if ("teacher" in request.session):
		return redirect("/teacher_dashboard/")
	elif ("student" in request.session):
		return redirect("/student_dashboard/")
	elif ("parent" in request.session):
		return redirect("/parent_dashboard/")
	elif ("head" in request.session):
		return redirect("/head_dashboard/")
	else:
		return redirect("/login/")

@csrf_exempt
def activities(request):
	context={};
	return render(request,'activities.html',context)



@csrf_exempt
def login(request):

	if ("enroll_no" in request.session):
		if ("teacher" in request.session):
			return redirect("/teacher_dashboard/")
		elif ("student" in request.session):
			return redirect("/student_dashboard/")
		elif ("parent" in request.session):
			return redirect("/parent_dashboard/")
		elif ("head" in request.session):
			return redirect("/head_dashboard/")


	if request.method=="POST":
		enroll_no=request.POST['enroll_no']
		password=request.POST['password']
		context={}

		if models.teacher.objects.filter(enroll_no=enroll_no).exists():
			if models.teacher.objects.filter(enroll_no=enroll_no,password=password).exists():
				request.session['enroll_no']=enroll_no
				request.session['teacher']='teacher'
				try:
					del request.session['not_exist']
				except:
					pass
				try:
					del request.session['marked']
				except:
					pass
				return redirect("/teacher_dashboard/")
			else:
				context["incorrectpass"]="Incorrect passowrd..!!"
				return render(request,'login/login.html',context)
		elif models.student.objects.filter(enroll_no=enroll_no).exists():
			if models.student.objects.filter(enroll_no=enroll_no,password=password).exists():
				request.session['enroll_no']=enroll_no
				request.session['student']='student'

				return redirect("/student_dashboard/")
			else:
				context["incorrectpass"]="Incorrect passowrd..!!"
				return render(request,'login/login.html',context)

		elif models.parent.objects.filter(parent_id=enroll_no).exists():
			if models.parent.objects.filter(parent_id=enroll_no,password=password).exists():
				request.session['enroll_no']=enroll_no
				request.session['parent']='parent'
				return redirect("/parent_dashboard/")
			else:
				context["incorrectpass"]="Incorrect passowrd..!!"
				return render(request,'login/login.html',context)

		elif models.head.objects.filter(enroll_no=enroll_no).exists():
			if models.head.objects.filter(enroll_no=enroll_no,password=password).exists():
				request.session['enroll_no']=enroll_no
				request.session['head']='head'
				return redirect("/head_dashboard/")
			else:
				context["incorrectpass"]="Incorrect passowrd..!!"
				return render(request,'login/login.html',context)


		else:
			context["notexist"]="Username does not exist!!"
			return render(request,'login/login.html',context)

	elif request.method=="GET":
		return render(request,'login/login.html',{})

@csrf_exempt
def logout(request):
	if "enroll_no" in request.session :
		del request.session["enroll_no"];
	try:
		del request.session["div"]
		del request.session["sub"]
	except:
		pass
	try:
		del request.session["teacher"]
	except:
		pass
	try:
		del request.session["student"]
	except:
		pass
	try:
		del request.session["parent"]
	except:
		pass
		
	return redirect("/login/")


@csrf_exempt
def forgot_password(request):

	if ("enroll_no" in request.session):
		if ("teacher" in request.session):
			return redirect("/teacher_dashboard/")
		elif ("student" in request.session):
			return redirect("/student_dashboard/")

	if request.method=="POST":
		email=request.POST['email']
		request.session['email']=request.POST['email']
		context={}

		if models.teacher.objects.filter(email=email).exists():
			temp=random.randint(1000,5001)
			request.session['otp']=temp
			send_mail('Please verify you accout. OTP :- ' + str(temp),
				'Here is the message.',
				settings.EMAIL_HOST_USER,
				[email],
				fail_silently=False)
			return render(request,'login/otp.html',context)
		elif models.student.objects.filter(email=email).exists():
			temp=random.randint(1000,5001)
			request.session['otp']=temp
			send_mail('Please verify you accout. OTP :- ' + str(temp),
				'Here is the message.',
				settings.EMAIL_HOST_USER,
				[email],
				fail_silently=False)
			return render(request,'login/otp.html',context)
		else:
			context["notexist"]="Email Id does not exist!!"
			return render(request,'login/forgot_password.html',context)

	elif request.method=="GET":
		return render(request,'login/forgot_password.html',{})


@csrf_exempt
def otp(request):
	context={}
	try:
		otp=int(request.POST["input"])
	except:
		context['charotp']="Integers only!!"
		return render(request,'login/otp.html',context)

	if request.session["otp"]== otp:
		print "entered"
		return render(request,'login/change_password.html',context)
	else:
		context['incorrectotp']="Incorrect OTP"
		return render(request,'login/otp.html',context)

@csrf_exempt
def change_password(request):
	context={}
	if request.method=="POST":
		print "entered in change password"
		new_password=request.POST['new_password']
		confirm_pass=request.POST['confirm_password']
 		if(new_password==confirm_pass):
	 		try:
				models.student.objects.filter(
					email=request.session['email']
					).update(password=(new_password))
			except:
				pass
			try:
				models.teacher.objects.filter(
					email=request.session['email']
					).update(password=(new_password))
			except:
				pass

			context['password_changed']="Password Changed!!"
			return render(request,"login/login.html",context)
		else:
			context['mismatch']="Passwords do not match!"
			return render(request,'login/change_password.html',context)
	elif request.method=="GET":
		return redirect('/login/');		


@csrf_exempt
def student_profile(request):
	if "student" in request.session:
		context = {}
		enroll_no = request.session['enroll_no']
		student = models.student.objects.get(enroll_no = enroll_no)
		context["course_end"]=student.admission_date+timedelta(days=365*4);
		context['student']= student
		return render(request,'student_profile.html',context)

	elif "teacher" in request.session:
		context={}
		enroll_no = request.GET['enroll_no']
		student = models.student.objects.get(enroll_no = enroll_no)
		context["course_end"]=student.admission_date+timedelta(days=365*4);
		context['student']= student
		context['teacher']= 'teacher'
		return render(request,'student_profile.html',context)


	else:
		return redirect("/student_dashboard/")



@csrf_exempt
def student_dashboard(request):

	if "student" in request.session:
		calculate_attendance(request)
		context = {}
		enroll_no = request.session['enroll_no']
		student = models.student.objects.get(enroll_no = enroll_no)
		context['student']= student
		total_lectures = models.total_lectures.objects.get()

		if(student.division == 'FE1'):

			context['total_lectures'] = total_lectures.fe1
			subjects=['physics','chemistry','maths']
			subjectwise_total = [total_lectures.physics,total_lectures.chemistry,total_lectures.maths]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='FE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;

		elif(student.division == 'SE1'):

			context['total_lectures'] = total_lectures.se1
			subjects=['deld','coa','mp']
			subjectwise_total = [total_lectures.deld,total_lectures.coa,total_lectures.mp]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='SE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;
		elif(student.division == 'TE1'):

			context['total_lectures'] = total_lectures.te1
			subjects=['toc','os','sdl']
			subjectwise_total = [total_lectures.toc,total_lectures.os,total_lectures.sdl]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='TE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;

		elif(student.division == 'BE1'):

			context['total_lectures'] = total_lectures.be1
			subjects=['ml','smd','ics']
			subjectwise_total = [total_lectures.ml,total_lectures.smd,total_lectures.ics]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='BE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;

		return render(request,'student_dashboard.html',context)
	else:
		return redirect("/login/")


@csrf_exempt
def show_classes(request):
	if "teacher" in request.session:
		context={}
		obj=models.teacher.objects.filter(enroll_no=request.session["enroll_no"])
		context["name"]=obj[0].name;
		context["enroll_no"]=obj[0].enroll_no;
		context["obj"]=obj;
		return render(request,'show_classes.html',context);
	else:
	 	return redirect("/teacher_dashboard/")

@csrf_exempt
def teacher_dashboard(request):

	if "teacher" in request.session:
		context={}
		try:
			context['not_exist']=request.session['not_exist']
		except:
			pass
		try:
			context['marked']=request.session['marked']
		except:
			pass
		obj=models.teacher.objects.filter(enroll_no=request.session["enroll_no"])
		context["name"]=obj[0].name;
		context["enroll_no"]=obj[0].enroll_no;
		context["obj"]=obj;
		request.session['flag']=0
		return render(request,'teacher_dashboard.html',context);
	else:
	 	return redirect("/login/")



@csrf_exempt
def fee_summary(request):
	if "student" in request.session:
		context={}
		obj=models.student.objects.get(enroll_no=request.session["enroll_no"])
		context["student"]=obj;
		return render(request,'fee_summary.html',context);
	else:
	 	return redirect("/student_dashboard/")



@csrf_exempt
def check_if_present(request):
	try:
		request.session['sub']=request.GET['sub']
		request.session['div']=request.GET['div']
	except:
		pass

	if request.session['flag']==0:	#Check whether subject is present or not
		try:
			del request.session["marked"]
		except:
			pass
		try:
			del request.session["not_exist"]
		except:
			pass
		return redirect("/store_attendance/")
	elif request.session['flag']==1:	#Subject is present, mark it
		request.session["marked"]="Attendace Marked!!"
		request.session["flag"]=2
		return redirect("/mark_attendance/")
	elif request.session['flag']==2:	#Goes to teacher dash with context as "subject not present" or "attendance marked"
		return redirect("/teacher_dashboard/")


@csrf_exempt
def mark_attendance(request):

	obj=models.student.objects.filter(division=request.session['div'])
	context={};
	context["sub"]=request.session['sub'];
	context["students"]=obj;

	return render(request,'mark_attendance.html',context);


def fe1(request):

	division=request.session['div']
	subject=request.session['sub'];
	status=request.POST.getlist('present_no')
	dates=models.dates.objects.get()
	sunday=dates.sunday
	new_week=dates.new_week
	curr_week=dates.curr_week
	today=datetime.now().date()-timedelta(days=0)

	if ((today-sunday).days)%7==1:	#MONDAY
		if subject=="chemistry":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week	
						).update(chemistry_m=1)
				obj = models.total_lectures.objects.get()
				obj.chemistry += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1


		elif subject=="physics":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(physics_m=1)
				obj = models.total_lectures.objects.get()
				obj.physics += 1
				obj.fe1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Monday!!"

	elif ((today-sunday).days)%7==2:	#TUESDAY

		if subject=="maths":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(maths_tu=1)
				obj = models.total_lectures.objects.get()
				obj.maths += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		elif subject=="physics":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(physics_tu=1)
				obj = models.total_lectures.objects.get()
				obj.physics += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Tuesday!!"

	elif ((today-sunday).days)%7==3:	#WEDNESDAY

		if subject=="physics":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(physics_w=1)
				obj = models.total_lectures.objects.get()
				obj.physics += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		elif subject=="chemistry":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(chemistry_w=1)
				obj = models.total_lectures.objects.get()
				obj.chemistry += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Wednesday!!"

	elif ((today-sunday).days)%7==4:	#thursday

		if subject=="chemistry":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(chemistry_th=1)
				obj = models.total_lectures.objects.get()
				obj.chemistry += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="maths":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(maths_th=1)
				obj = models.total_lectures.objects.get()
				obj.maths += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on thursday!!"


	elif ((today-sunday).days)%7==5:	#FRIDAY

		if subject=="chemistry":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(chemistry_f=1)
				obj = models.total_lectures.objects.get()
				obj.chemistry += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="physics":
			if request.session['flag']==2:
				for present in status:
					models.FE1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(physics_f=1)
				obj = models.total_lectures.objects.get()
				obj.physics += 1
				obj.fe1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Friday!!"
	else:
		request.session["flag"]=2
		request.session["not_exist"]="Oh..No lectures scheduled on Weekend!!"


def se1(request):

	division=request.session['div']
	subject=request.session['sub'];
	status=request.POST.getlist('present_no')
	dates=models.dates.objects.get()
	sunday=dates.sunday
	new_week=dates.new_week
	curr_week=dates.curr_week
	today=datetime.now().date()-timedelta(days=0)

	if ((today-sunday).days)%7==1:	#MONDAY
		if subject=="coa":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week	
						).update(coa_m=1)
				obj = models.total_lectures.objects.get()
				obj.coa += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1


		elif subject=="deld":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(deld_m=1)
				obj = models.total_lectures.objects.get()
				obj.deld += 1
				obj.se1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="mp":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(mp_m=1)
				obj = models.total_lectures.objects.get()
				obj.mp += 1
				obj.se1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Monday!!"


	elif ((today-sunday).days)%7==2:	#TUESDAY

		if subject=="mp":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(mp_tu=1)
				obj = models.total_lectures.objects.get()
				obj.mp += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		elif subject=="coa":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(coa_tu=1)
				obj = models.total_lectures.objects.get()
				obj.coa += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Tuesday!!"

	elif ((today-sunday).days)%7==3:	#WEDNESDAY

		if subject=="deld":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(deld_w=1)
				obj = models.total_lectures.objects.get()
				obj.deld += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Wednesday!!"

	elif ((today-sunday).days)%7==4:	#thursday

		if subject=="coa":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(coa_th=1)
				obj = models.total_lectures.objects.get()
				obj.coa += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="deld":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(deld_th=1)
				obj = models.total_lectures.objects.get()
				obj.deld += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on thursday!!"


	elif ((today-sunday).days)%7==5:	#FRIDAY

		if subject=="coa":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(coa_f=1)
				obj = models.total_lectures.objects.get()
				obj.coa += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="mp":
			if request.session['flag']==2:
				for present in status:
					models.se1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(mp_f=1)
				obj = models.total_lectures.objects.get()
				obj.mp += 1
				obj.se1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Friday!!"
	else:
		request.session["flag"]=2
		request.session["not_exist"]="Oh..No lectures scheduled on Weekend!!"

def te1(request):

	division=request.session['div']
	subject=request.session['sub'];
	status=request.POST.getlist('present_no')
	dates=models.dates.objects.get()
	sunday=dates.sunday
	new_week=dates.new_week
	curr_week=dates.curr_week
	today=datetime.now().date()-timedelta(days=0)

	if ((today-sunday).days)%7==1:	#MONDAY
		if subject=="toc":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week	
						).update(toc_m=1)
				obj = models.total_lectures.objects.get()
				obj.toc += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1


		elif subject=="os":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(os_m=1)
				obj = models.total_lectures.objects.get()
				obj.os += 1
				obj.te1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="sdl":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(sdl_m=1)
				obj = models.total_lectures.objects.get()
				obj.sdl += 1
				obj.te1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Monday!!"


	elif ((today-sunday).days)%7==2:	#TUESDAY

		if subject=="sdl":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(sdl_tu=1)
				obj = models.total_lectures.objects.get()
				obj.sdl += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		elif subject=="toc":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(toc_tu=1)
				obj = models.total_lectures.objects.get()
				obj.toc += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Tuesday!!"

	elif ((today-sunday).days)%7==3:	#WEDNESDAY

		if subject=="os":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(os_w=1)
				obj = models.total_lectures.objects.get()
				obj.os += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Wednesday!!"

	elif ((today-sunday).days)%7==4:	#thursday

		if subject=="toc":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(toc_th=1)
				obj = models.total_lectures.objects.get()
				obj.toc += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="os":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(os_th=1)
				obj = models.total_lectures.objects.get()
				obj.os += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on thursday!!"


	elif ((today-sunday).days)%7==5:	#FRIDAY

		if subject=="toc":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(toc_f=1)
				obj = models.total_lectures.objects.get()
				obj.toc += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="sdl":
			if request.session['flag']==2:
				for present in status:
					models.te1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(sdl_f=1)
				obj = models.total_lectures.objects.get()
				obj.sdl += 1
				obj.te1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Friday!!"
	else:
		request.session["flag"]=2
		request.session["not_exist"]="Oh..No lectures scheduled on Weekend!!"

def be1(request):

	division=request.session['div']
	subject=request.session['sub'];
	status=request.PsmdT.getlist('present_no')
	dates=models.dates.objects.get()
	sunday=dates.sunday
	new_week=dates.new_week
	curr_week=dates.curr_week
	today=datetime.now().date()-timedelta(days=0)

	if ((today-sunday).days)%7==1:	#MONDAY
		if subject=="ml":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week	
						).update(ml_m=1)
				obj = models.total_lectures.objects.get()
				obj.ml += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1


		elif subject=="smd":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(smd_m=1)
				obj = models.total_lectures.objects.get()
				obj.smd += 1
				obj.be1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="ics":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(ics_m=1)
				obj = models.total_lectures.objects.get()
				obj.ics += 1
				obj.be1 += 1
				obj.save()					
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Monday!!"


	elif ((today-sunday).days)%7==2:	#TUESDAY

		if subject=="ics":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(ics_tu=1)
				obj = models.total_lectures.objects.get()
				obj.ics += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		elif subject=="ml":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(ml_tu=1)
				obj = models.total_lectures.objects.get()
				obj.ml += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Tuesday!!"

	elif ((today-sunday).days)%7==3:	#WEDNESDAY

		if subject=="smd":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(smd_w=1)
				obj = models.total_lectures.objects.get()
				obj.smd += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Wednesday!!"

	elif ((today-sunday).days)%7==4:	#thursday

		if subject=="ml":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(ml_th=1)
				obj = models.total_lectures.objects.get()
				obj.ml += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="ics":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(ics_th=1)
				obj = models.total_lectures.objects.get()
				obj.ics += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on thursday!!"


	elif ((today-sunday).days)%7==5:	#FRIDAY

		if subject=="ml":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(ml_f=1)
				obj = models.total_lectures.objects.get()
				obj.ml += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		elif subject=="smd":
			if request.session['flag']==2:
				for present in status:
					models.be1.objects.filter(
						student__enroll_no=present,
						date=curr_week
						).update(smd_f=1)
				obj = models.total_lectures.objects.get()
				obj.smd += 1
				obj.be1 += 1
				obj.save()
				request.session['flag']=2
			else:
				request.session['flag']=1

		
		else:
			request.session["flag"]=2
			request.session["not_exist"]="Oh..it seems this lecture is not scheduled on Friday!!"
	else:
		request.session["flag"]=2
		request.session["not_exist"]="Oh..No lectures scheduled on Weekend!!"


@csrf_exempt
def all_teachers(request):
	if "head" in request.session:
		context = {}
		head = models.head.objects.get(enroll_no= request.session['enroll_no'])
		context['head']=head;
		context["teachers"]=models.teacher.objects.all();
		return render(request,'all_teachers.html',context)
	else:
		return redirect("/all_teachers/")

@csrf_exempt
def all_students(request):
	if "head" in request.session:
		context = {}
		head = models.head.objects.get(enroll_no= request.session['enroll_no'])
		context['head']=head;
		context["fe1"]=models.student.objects.filter(division='FE1');
		context["se1"]=models.student.objects.filter(division='SE1');
		context["te1"]=models.student.objects.filter(division='TE1');
		context["be1"]=models.student.objects.filter(division='BE1');
		return render(request,'all_students.html',context)
	else:
		return redirect("/all_students/")


@csrf_exempt
def time_table(request):
		context = {}
		return render(request,'time_table.html',context)


@csrf_exempt
def head_dashboard(request):
	if "head" in request.session:
		context = {}
		head = models.head.objects.get(enroll_no= request.session['enroll_no'])
		context['head']=head;
		context["teachers"]=models.teacher.objects.all();
		return render(request,'head_dashboard.html',context)
	else:
		return redirect("/head_dashboard/")


@csrf_exempt
def store_attendance(request):

	if "enroll_no" not in request.session:
	 	return redirect("/login/")
	else:
		division=request.session['div']
		subject=request.session['sub']
		dates=models.dates.objects.get()
		status=request.POST.getlist('present_no')
		new_week=dates.new_week
		curr_week=dates.curr_week
		today=datetime.now().date()+timedelta(days=0)

		if new_week<=today:

			models.dates.objects.all().update(new_week=new_week+timedelta(days=7))
			models.dates.objects.all().update(curr_week=curr_week+timedelta(days=7))

			temp=models.student.objects.filter(division='FE1')
			for i in temp:
				obj=models.FE1(date=curr_week)
				obj.student=i
				obj.save()

			temp=models.student.objects.filter(division='SE1')
			for i in temp:
				obj=models.SE1(date=curr_week)
				obj.student=i
				obj.save()

		if division=="FE1":
			fe1(request)
			for i in status:
				student = models.student.objects.get(enroll_no = i)
				if subject == 'physics':
					student.sub1_present += 1
				elif subject == 'chemistry':
					student.sub2_present += 1
				elif subject == 'maths':
					student.sub3_present += 1
				student.save()
		if division=="SE1":
			se1(request)
			for i in status:
				student = models.student.objects.get(enroll_no = i)
				if subject == 'deld':
					student.sub1_present += 1
				elif subject == 'coa':
					student.sub2_present += 1
				elif subject == 'mp':
					student.sub3_present += 1
				student.save()
		if division=="TE1":
			te1(request)
			for i in status:
				student = models.student.objects.get(enroll_no = i)
				if subject == 'toc':
					student.sub1_present += 1
				elif subject == 'os':
					student.sub2_present += 1
				elif subject == 'sdl':
					student.sub3_present += 1
				student.save()
		if division=="BE1":
			be1(request)
			for i in status:
				student = models.student.objects.get(enroll_no = i)
				if subject == 'ml':
					student.sub1_present += 1
				elif subject == 'smd':
					student.sub2_present += 1
				elif subject == 'ics':
					student.sub3_present += 1
				student.save()
		return redirect("/check_if_present/")


def calculate_attendance(request):

	if "student" in request.session:
		student = models.student.objects.get(enroll_no = request.session['enroll_no'])
	elif "parent"in request.session:
		parent = models.parent.objects.get(parent_id= request.session['enroll_no'])
		student = parent.student

	present_sub1 = student.sub1_present
	present_sub2 = student.sub2_present
	present_sub3 = student.sub3_present
	present = present_sub1 + present_sub2 + present_sub3
	student.total_present = present
		
	total=0
	obj = models.total_lectures.objects.get()

	if student.division == 'FE1':
		total = obj.fe1
		total_sub1 = obj.physics
		total_sub2=obj.chemistry
		total_sub3= obj.maths
	elif student.division == 'SE1':
		total = obj.se1
		total_sub1 = obj.deld
		total_sub2=obj.coa
		total_sub3= obj.mp
	elif student.division == 'TE1':
		total = obj.te1
		total_sub1 = obj.toc
		total_sub2=obj.os
		total_sub3= obj.sdl
	elif student.division == 'BE1':
		total = obj.be1
		total_sub1 = obj.ml
		total_sub2=obj.smd
		total_sub3= obj.ics

	student.sub1_attendance = (present_sub1*100)/total_sub1
	student.sub2_attendance = (present_sub2*100)/total_sub2
	student.sub3_attendance = (present_sub3*100)/total_sub3

	student.avg_attendance = (present*100)/total
	student.save()

 
@csrf_exempt
def register_teacher(request):
	context={}
	if request.method=="GET":
		return render(request,'register_teacher.html');
	elif request.method=="POST":
		try:
			Enroll_no=request.GET['enroll_no'];
		except:
			pass

		Enroll_no=request.POST['enroll_no'];
		Name=request.POST['name'];
		Password=request.POST['password'];
		Email=request.POST['email'];
		Division=request.POST['division'];
		Subject=request.POST['subject'];


		if models.teacher.objects.filter(enroll_no=Enroll_no).exists():
			if models.teacher.objects.filter(enroll_no=Enroll_no,name=Name).exists():
				obj1=models.teacher(
					enroll_no=Enroll_no,
					name=Name,password=Password,
					email=Email,
					division=Division,subject=Subject)
				obj1.save()
				context['success']="Teacher registration successful."
				return render(request,'register_teacher.html',context);

			else:	

				context['same_teacher']="Name should match for registered Enrollment no "
				return render(request,'register_teacher.html',context);
		else:
				obj2=models.teacher(
					enroll_no=Enroll_no,
					name=Name,password=Password,
					email=Email,
					division=Division,subject=Subject)
				obj2.save()
				context['success']="Teacher registration successful."
				return render(request,'register_teacher.html',context);

@csrf_exempt
def parent_profile(request):
	if "parent" in request.session:
		context = {}
		parent = models.parent.objects.get(parent_id= request.session['enroll_no'])
		student = parent.student
		context['parent']= parent
		context['student']= student
		return render(request,'parent_profile.html',context)
	else:
		return redirect("/parent_dashboard/")


@csrf_exempt
def parent_dashboard(request):

	if "parent" in request.session:
		calculate_attendance(request)
		context = {}
		parent = models.parent.objects.get(parent_id= request.session['enroll_no'])
		student = parent.student
		context['parent']= parent
		context['student']= student
		total_lectures = models.total_lectures.objects.get()

		if(student.division == 'FE1'):

			context['total_lectures'] = total_lectures.fe1
			subjects=['physics','chemistry','maths']
			subjectwise_total = [total_lectures.physics,total_lectures.chemistry,total_lectures.maths]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]
			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='FE1')
				print t
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;

		elif(student.division == 'SE1'):

			context['total_lectures'] = total_lectures.SE1
			subjects=['deld','coa','mp']
			subjectwise_total = [total_lectures.deld,total_lectures.coa,total_lectures.mp]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='SE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;
		elif(student.division == 'TE1'):

			context['total_lectures'] = total_lectures.TE1
			subjects=['toc','os','sdl']
			subjectwise_total = [total_lectures.toc,total_lectures.os,total_lectures.sdl]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='TE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;

		elif(student.division == 'BE1'):

			context['total_lectures'] = total_lectures.BE1
			subjects=['ml','smd','ics']
			subjectwise_total = [total_lectures.ml,total_lectures.smd,total_lectures.ics]
			subjectwise_present = [student.sub1_present,student.sub2_present,student.sub3_present]
			subjectwise_attendance = [student.sub1_attendance,student.sub2_attendance,student.sub3_attendance]
			obj =[]

			i=0
			for s in subjects:
				t = models.teacher.objects.filter(subject = s,division='BE1')
				temp={}
				temp['subject']=s
				temp['teacher']=t[0].name
				temp['total']= subjectwise_total[i]
				temp['present']=subjectwise_present[i]
				temp['attendance']= subjectwise_attendance[i]

				obj.append(temp)
				i=i+1

			context['obj']= obj;
		return render(request,'parent_dashboard.html',context)
	else:
		return redirect("/login/")


@csrf_exempt
def weekly_stats(request):
	enroll_no = request.GET['enroll_no']
	division= request.GET['division']
	obj_list=[]

	if division== 'FE1':
		obj_list = models.FE1.objects.filter(student__enroll_no = enroll_no)
		for i in obj_list: 
			pcount = 0
			tcount=0
			if i.physics_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.chemistry_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.physics_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.maths_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.physics_w ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.chemistry_w ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.chemistry_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.maths_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.physics_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.chemistry_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			i.weekly_attendance = (pcount*100/tcount)
			i.save()

	elif division== 'SE1':
		obj_list = models.SE1.objects.filter(student__enroll_no = enroll_no)
		for i in obj_list: 
			pcount = 0
			tcount=0
			if i.deld_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.coa_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.mp_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.mp_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.coa_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.deld_w ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			
			if i.coa_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.deld_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.deld_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.coa_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.mp_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			i.weekly_attendance = (pcount*100/tcount)
			i.save()

	elif division== 'TE1':
		obj_list = models.TE1.objects.filter(student__enroll_no = enroll_no)
		for i in obj_list: 
			pcount = 0
			tcount=0
			if i.os_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.toc_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.sdl_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.sdl_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.toc_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.os_w ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			
			if i.toc_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.os_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.os_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.toc_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.sdl_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			i.weekly_attendance = (pcount*100/tcount)
			i.save()

	elif division== 'BE1':
		obj_list = models.BE1.objects.filter(student__enroll_no = enroll_no)
		for i in obj_list: 
			pcount = 0
			tcount=0
			if i.smd_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ml_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ics_m ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ics_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ml_tu ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.smd_w ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			
			if i.ml_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ics_th ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.smd_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ml_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			if i.ics_f ==1:
				pcount +=1
				tcount+=1
			else:
				tcount +=1
			i.weekly_attendance = (pcount*100/tcount)
			i.save()
			

	prev_weeks= []

	for i in obj_list:
		time_delta = datetime.now().date() - i.date
		if time_delta.days >= 6:
			prev_weeks.append(i)

	values=[]
	for i in prev_weeks:
		values.append(i.weekly_attendance)


	customstyle=Style(plot_background='#fafafa',foreground=' rgb(89, 137, 214)')
	line_chart = pygal.Line(style=customstyle)
	# line_chart.title = 'Weekly Attendance Analysis'

	weeks = ['Week1','Week2','Week3','Week4','Week5','Week6','Week7','Week8']
	line_chart.x_labels = weeks[0:len(values)]


	student = models.student.objects.get(enroll_no = enroll_no)
	line_chart.add(student.name, values)
	line_chart.render_to_file('/home/shivani/Desktop/proj3/app/static/graph/weekly_attendance.svg')

	context={}
	context['student']= student
	if 'student'in request.session:
		return render(request,'weekly_analysis_student.html',context)
	elif 'parent'in request.session:
		return render(request,'weekly_analysis_parent.html',context)

	
@csrf_exempt
def show_students(request):
	division = request.GET['division']
	subject = request.GET['subject']
	context={}
	context['division']=division
	context['subject']=subject
	students = models.student.objects.filter(division=division)
	student_info=[]

	if division == "FE1":
		if subject == "physics":
			context['sub_total'] = models.total_lectures.objects.get().physics
			
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub1_present
				temp['sub_attendance']= i.sub1_attendance
				student_info.append(temp)
		elif subject == "chemistry":
			context['sub_total'] = models.total_lectures.objects.get().chemistry
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub2_present
				temp['sub_attendance']= i.sub2_attendance
				student_info.append(temp)
		elif subject == "maths":
			context['sub_total'] = models.total_lectures.objects.get().maths
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub3_present
				temp['sub_attendance']= i.sub3_attendance
				student_info.append(temp)

	if division == "SE1":
		if subject == "deld":
			context['sub_total'] = models.total_lectures.objects.get().deld
			
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub1_present
				temp['sub_attendance']= i.sub1_attendance
				student_info.append(temp)
		elif subject == "coa":
			context['sub_total'] = models.total_lectures.objects.get().coa
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub2_present
				temp['sub_attendance']= i.sub2_attendance
				student_info.append(temp)
		elif subject == "mp":
			context['sub_total'] = models.total_lectures.objects.get().mp
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub3_present
				temp['sub_attendance']= i.sub3_attendance
				student_info.append(temp)

	if division == "TE1":
		if subject == "toc":
			context['sub_total'] = models.total_lectures.objects.get().toc
			
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub1_present
				temp['sub_attendance']= i.sub1_attendance
				student_info.append(temp)
		elif subject == "os":
			context['sub_total'] = models.total_lectures.objects.get().os
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub2_present
				temp['sub_attendance']= i.sub2_attendance
				student_info.append(temp)
		elif subject == "sdl":
			context['sub_total'] = models.total_lectures.objects.get().sdl
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub3_present
				temp['sub_attendance']= i.sub3_attendance
				student_info.append(temp)

	if division == "BE1":
		if subject == "ml":
			context['sub_total'] = models.total_lectures.objects.get().ml
			
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub1_present
				temp['sub_attendance']= i.sub1_attendance
				student_info.append(temp)
		elif subject == "smd":
			context['sub_total'] = models.total_lectures.objects.get().smd
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub2_present
				temp['sub_attendance']= i.sub2_attendance
				student_info.append(temp)
		elif subject == "ics":
			context['sub_total'] = models.total_lectures.objects.get().ics
			for i in students:
				temp = {}
				temp['student']= i
				temp['enroll_no']= i.enroll_no
				temp['sub_present']= i.sub3_present
				temp['sub_attendance']= i.sub3_attendance
				student_info.append(temp)

	context['student_info']=student_info
	return render(request,'view_students.html',context)


@csrf_exempt
def register_student(request):
	context={}
	if request.method=="GET":
		return render(request,'register_student.html');
	elif request.method=="POST":
		try:
			Enroll_no=request.GET['enroll_no'];
		except:
			pass

		Enroll_no=request.POST['enroll_no'];
		Name=request.POST['name'];
		Password=request.POST['password'];
		Email=request.POST['email'];
		Gender=request.POST['gender']
		Age=request.POST['age']
		Division=request.POST['division'];
		admission_date=datetime.now()

		if models.student.objects.filter(enroll_no=Enroll_no).exists():
			context['duplicate_enroll']="Enrollment no must be unique"
			return render(request,'register_student.html',context);
		else:	
			obj1=models.student(
				enroll_no=Enroll_no,
				name=Name,password=Password,
				email=Email,age=Age,
				division=Division,gender=Gender,admission_date=admission_date)
			obj1.save()
			context['success']="Student registration successful."
			return render(request,'register_student.html',context);


		

