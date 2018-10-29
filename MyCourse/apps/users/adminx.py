# encoding=utf-8

import xadmin

from .models import EmailVerifyRecoed,Banner
from xadmin import views


# 设置xadmin的主题
# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True
#
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 控制xadmin的標題和尾部
class GlobalSettings(object):
    site_title = "好好学习"
    site_footer = "天天向上"
    # 把xadmin中的app给折叠起来
    menu_style = "accordion"

class EmailVerifyRecoedAdmin(object):
    # 控制我們要在admin中显示的字段
    list_display = ['code','email','send_type','send_time']
    # 控制我们的admin中搜索的时的字段
    search_fields = ['code','email','send_type']
    # 过滤器
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecoed,EmailVerifyRecoedAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)