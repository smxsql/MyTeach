# encoding=utf8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from organization.models import CourseOrg
# Create your models here.


# 課程model
class Course(models.Model):
    # 新增的字段要给设置成可以为空这样的话就不会已经有的字段冲突
    course = models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name=u'课程名')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(verbose_name=u"难度",choices=(("cj",u"初级"),("zj",u"中级"),("gj",u"高级")),max_length=2)
    learn_times = models.ImageField(default=0,verbose_name=u"学习时长(分钟为单位)")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name=u"封面图",max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 章節model
class Lesson(models.Model):
    # 定义外键指向我们的course
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


#課程視頻model
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=100,verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name


# 課程資源model
class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"下载地址")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name