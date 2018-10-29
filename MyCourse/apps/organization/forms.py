# encoding=utf-8

from django import forms
import re

from operation.models import UserAsk
# 自己写的from
# class UserAskFrom(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,max_length=5,min_length=5)


# 可以直接把我们的model的字段转换成form验证继承的model的form
class UserAskFrom(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    # clean函数对我们的单个字段进行验证必须是以clean开头
    def clean_mobile(self):
        # cleaned_data：就是取出我们的mobile字段的值
        mobile = self.cleaned_data['mobile']

        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        # mobile
        if p.match(mobile):
            return mobile
        # raise就是抛出异常
        else:
            raise forms.ValidationError(u'手机号码非法',code="mobile_invalid")