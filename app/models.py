# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class teacher(models.Model):
	enroll_no=models.CharField(max_length=50,blank=False)
	name=models.CharField(max_length=50,blank=False);
	password=models.CharField(max_length=50,blank=False)
	email=models.CharField(max_length=50,blank=False)
	DIV = {
		('FE1','FE1'),
		('SE1','SE1'),
		('TE1','TE1'),
		('BE1','BE1'),
	}
	division=models.CharField(max_length=50,choices=DIV,blank=False)
	SUB = {
		('physics','Physics'),
		('chemistry','Chemistry'),
		('maths','Maths'),

		('deld','D.E.L.D'),
		('coa','C.O.A'),
		('mp','M.P'),

		('toc','T.O.C'),
		('os','O.S'),
		('sdl','S.D.L'),
		
		('ml','M.L'),
		('smd','S.M.D'),
		('ics','I.C.S'),
	}
	subject=models.CharField(max_length=50,choices=sorted(SUB),blank=False)

	def __str__(self):
		return self.name

class head(models.Model):
	enroll_no=models.CharField(max_length=50,blank=False)
	name=models.CharField(max_length=50,blank=False);
	password=models.CharField(max_length=50,blank=False)
	email=models.CharField(max_length=50,blank=False)

	def __str__(self):
		return self.name


class student(models.Model):
	name=models.CharField(max_length=50,blank=False)
	enroll_no=models.CharField(max_length=50,blank=False,unique=True)
	password=models.CharField(max_length=50,blank=False)
	DIV = {
		('FE1','FE1'),
		('SE1','SE1'),
		('TE1','TE1'),
		('BE1','BE1'),
	}
	division=models.CharField(max_length=50,choices=DIV,blank=False)
	GENDER = {
		('male','male'),
		('female','female'),
		('other','other'),
	}
	gender=models.CharField(max_length=50,choices=GENDER,blank=False)
	age=models.IntegerField()
	email=models.CharField(max_length=50,blank=False)
	admission_date=models.DateTimeField(blank=False)
	

	sub1_present = models.IntegerField(default=0)
	sub2_present= models.IntegerField(default=0)
	sub3_present = models.IntegerField(default=0)

	total_present = models.IntegerField(default = 0)
	
	sub1_attendance = models.FloatField(default=0)
	sub2_attendance = models.FloatField(default=0)
	sub3_attendance = models.FloatField(default=0)
	avg_attendance = models.FloatField(default=0)
	university_fee = models.FloatField(default=2000)
	development_fee = models.FloatField(default=8414)
	tution_fee = models.FloatField(default=84136)
	exam_fee = models.FloatField(default=00)

	def __str__(self):
		return self.name

class dates(models.Model):

	sunday = models.DateField(default = "2018-09-09")
	new_week = models.DateField(default = datetime.now)
	curr_week = models.DateField(default = datetime.now)

	class Meta:
		verbose_name_plural ='Dates'




class FE1(models.Model):

	date = models.DateField(default = datetime.now)

	physics_m = models.IntegerField(default=0)
	chemistry_m = models.IntegerField(default=0)

	maths_tu = models.IntegerField(default=0)
	physics_tu = models.IntegerField(default=0)

	physics_w = models.IntegerField(default=0)
	chemistry_w = models.IntegerField(default=0)

	chemistry_th = models.IntegerField(default=0)
	maths_th = models.IntegerField(default=0)

	chemistry_f = models.IntegerField(default=0)
	physics_f = models.IntegerField(default=0)

	weekly_attendance = models.FloatField(default=0)
	student = models.ForeignKey(student,on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural ='FE1'

	def __str__(self):
		return str(self.date) +  " || " + str(self.student.name)


class SE1(models.Model):

	date = models.DateField(default = datetime.now)

	deld_m = models.IntegerField(default=0)
	coa_m = models.IntegerField(default=0)
	mp_m = models.IntegerField(default=0)


	mp_tu = models.IntegerField(default=0)
	coa_tu = models.IntegerField(default=0)

	deld_w =models.IntegerField(default=0)
	

	coa_th = models.IntegerField(default=0)
	deld_th = models.IntegerField(default=0)

	mp_f = models.IntegerField(default=0)
	coa_f = models.IntegerField(default=0)
	
	weekly_attendance = models.FloatField(default=0)
	student = models.ForeignKey(student,on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural ='SE1'

	def __str__(self):
		return str(self.date) +  " || " + str(self.student.name)


	class Meta:
		verbose_name_plural ='SE1'


class TE1(models.Model):

	date = models.DateField(default = datetime.now)

	toc_m = models.IntegerField(default=0)
	os_m = models.IntegerField(default=0)
	sdl_m = models.IntegerField(default=0)


	sdl_tu = models.IntegerField(default=0)
	toc_tu = models.IntegerField(default=0)

	os_w =models.IntegerField(default=0)
	

	toc_th = models.IntegerField(default=0)
	os_th = models.IntegerField(default=0)

	sdl_f = models.IntegerField(default=0)
	toc_f = models.IntegerField(default=0)
	
	weekly_attendance = models.FloatField(default=0)

	student = models.ForeignKey(student,on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural ='TE1'

	def __str__(self):
		return str(self.date) +  " || " + str(self.student.name)


	class Meta:
		verbose_name_plural ='TE1'



class BE1(models.Model):

	date = models.DateField(default = datetime.now)

	ml_m = models.IntegerField(default=0)
	smd_m = models.IntegerField(default=0)
	ics_m = models.IntegerField(default=0)


	ics_tu = models.IntegerField(default=0)
	ml_tu = models.IntegerField(default=0)

	smd_w =models.IntegerField(default=0)
	

	ml_th = models.IntegerField(default=0)
	ics_th = models.IntegerField(default=0)

	smd_f = models.IntegerField(default=0)
	ml_f = models.IntegerField(default=0)

	weekly_attendance = models.FloatField(default=0)
	student = models.ForeignKey(student,on_delete=models.CASCADE)


	def __str__(self):
		return str(self.date) +  " || " + str(self.student.name)


	class Meta:
		verbose_name_plural ='BE1'




class parent(models.Model):
	name=models.CharField(max_length=50,blank=False)
	parent_id=models.CharField(max_length=50,blank=False,unique=True)
	password=models.CharField(max_length=50,blank=False)
	
	GENDER = {
		('male','male'),
		('female','female'),
		('other','other'),
	}
	gender=models.CharField(max_length=50,choices=GENDER,blank=False)
	age=models.IntegerField()
	email=models.CharField(max_length=50,blank=False)
	occupation =models.CharField(max_length=50)

	RELATIONS = {
		('father','father'),
		('mother','mother'),
		('guardian','guardian'),
	}
	relation=models.CharField(max_length=50,choices=RELATIONS,blank=False)

	student=models.ForeignKey(student,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name + " || "+self.student.name

class total_lectures(models.Model):

	fe1 = models.IntegerField(default=0)
	physics = models.IntegerField(default=0)
	chemistry = models.IntegerField(default=0)
	maths = models.IntegerField(default=0)

	se1 = models.IntegerField(default=0)
	deld = models.IntegerField(default=0)
	coa = models.IntegerField(default=0)
	mp = models.IntegerField(default=0)

	te1 = models.IntegerField(default=0)
	toc = models.IntegerField(default=0)
	os = models.IntegerField(default=0)
	sdl = models.IntegerField(default=0)

	be1 = models.IntegerField(default=0)
	ml = models.IntegerField(default=0)
	smd = models.IntegerField(default=0)
	ics = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural ='total lectures'




