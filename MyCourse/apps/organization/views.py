# encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import CourseOrg,CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskFrom
from courses.models import Course
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        # 调用Paginator进行分页
        # 城市筛选
        city_id = request.GET.get('city','')
        # 根据点击量进行排名利用Django的orm的order_by来进行排名只取前三名在筛选的字段中加上一个-号就是代表从大向小取
        host_orgs = all_orgs.order_by("-click_nums")[:3]


        if city_id:
            all_orgs = CourseOrg.objects.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct',"")

        if category:
            all_orgs = CourseOrg.objects.filter(category=category)

        sort = request.GET.get("sort","")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        # 统计查询出来的数量
        org_num = all_orgs.count()
        all_citys = CityDict.objects.all()
        return render(request,"org-list.html",{"all_orgs":orgs,"all_citys":all_citys,"org_num":org_num,"city_id":city_id,"category":category,"host_orgs":host_orgs,"sort":sort})


# 处理用户咨询的view
class AskView(View):
    """
    用户咨询表单提交
    """
    def post(self,request):
        userask_from = UserAskFrom(request.POST)
        if userask_from.is_valid():
            # commit=True就是直接存储到我们的数据库当中因为我们继承的是modelform
            user_ask = userask_from.save(commit=True)
            # return HttpResponse("{'status':'success'}",content_type='application/json')
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # return HttpResponse("{'status':'fail', 'msg':'用户出错'}", content_type='application/json')
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        # 传递一个变量用来标识我们列表页的导航
        current_page = "home"
        # 首先就是查出这个机构
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 接着就会根据查出的和这个机构的外键查出所有的课程
        all_course = course_org.course_set.all()[:3]
        # 根据外键取出所有的老师
        all_teacher = course_org.teacher_set.all()[:2]

        return render(request,"org-detail-homepage.html",{"all_course":all_course,
                                                          "all_teacher":all_teacher,
                                                          "course_org":course_org,
                                                          "current_page":current_page
                                                          })



class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        current_page = "course"
        # 首先就是查出这个机构
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 接着就会根据查出的和这个机构的外键查出所有的课程
        all_course = course_org.course_set.all()

        return render(request,"org-detail-course.html",{"all_course":all_course,
                                                        "course_org":course_org,
                                                        "current_page": current_page
                                                          })


class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id = int(org_id))
        return render(request,"org-detail-desc.html",{"course_org":course_org,"current_page":current_page})



class OrgTeacherView(View):
    """
    机构教师列表页
    """
    def get(self,request,org_id):
        current_page = "teacher"
        # 首先就是查出这个机构
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 接着就会根据查出的和这个机构的外键查出所有的课程
        all_teacher = course_org.teacher_set.all()

        return render(request,"org-detail-teachers.html",{"all_teacher":all_teacher,
                                                        "course_org":course_org,
                                                        "current_page": current_page
                                                          })


class AddFavView(View):
    """
    用户收藏,用户取消收藏
    """
    def post(self,request):
        # 全都前台ajax传过来的,0避免转换时出现异常
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 调用request的内置类user中的is_authenticated():来判断用户是否存在
        if not request.user.is_authenticated():
            # 前台的ajax判断到这个fail状态码之后就会跳转到登录页面
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        # 前台有用戶request就是前台请求来的user
        exist_recods = UserFavorite.objects.filter(user=request,fav_id=int(fav_id),fav_type=int(fav_type))

        if exist_recods:
            # 如果已经存在那么就是用户要删除，就直接删掉
            exist_recods.delete()
            return HttpResponse('{"status":"fail", "msg":"收藏"}', content_type='application/json')
        # 不存在的话就是往数据库中添加
        else:
            user_fav = UserFavorite()
            # 当他们都大于0时就是表示是用户添加的才有必要添加到数据库中
            if int(fav_type) > 0 and int(fav_id)>0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')