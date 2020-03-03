from django.http.response import JsonResponse
import json
import requests
from django.views import View
from utils.util import ReturnCode,wrap_json_response,CommonResponseMixin,is_authorized
from .models import User,Customer
# Create your views here
class CusFollow(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        data = {}
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        year = str(post_data.get('year')).strip()
        month = str(post_data.get('month')).strip()
        day = str(post_data.get('day')).strip()
        open_id = request.session.get("open_id")
        customer = Customer.objects.filter(cus_coming_time__year=year, cus_coming_time__month=month,
                                                 cus_coming_time__day=day,open_id=open_id).values()
        data['data'] = list(customer)
        return JsonResponse(data, safe=False)

class NewCus(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        data = {}
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        year = str(post_data.get('year')).strip()
        month = str(post_data.get('month')).strip()
        day = str(post_data.get('day')).strip()
        customer = Customer.objects.filter(cus_coming_time__year=year, cus_coming_time__month=month,
                                                 cus_coming_time__day=day,cus_coming_counts__lt=2).values()
        data['data'] = list(customer)
        return JsonResponse(data, safe=False)

class WaitCus(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        data = {}
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        year = str(post_data.get('year')).strip()
        month = str(post_data.get('month')).strip()
        day = str(post_data.get('day')).strip()
        customer = Customer.objects.filter(cus_coming_time__year=year, cus_coming_time__month=month,
                                                 cus_coming_time__day=day,open_id=None).values()
        data['data'] = list(customer)
        return JsonResponse(data, safe=False)




class CusView(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        data = {}
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        year = str(post_data.get('year')).strip()
        month = str(post_data.get('month')).strip()
        day = str(post_data.get('day')).strip()
        "到店总数"
        total_customer = Customer.objects.filter(cus_coming_time__year=year, cus_coming_time__month=month, cus_coming_time__day=day)
        customer = total_customer.values()
        data['data'] = list(customer)
        data['total_cus'] = len(customer)
        "我的跟踪"
        open_id = request.session.get("open_id")
        my_follow = total_customer.filter(open_id=open_id).values()
        data["my_follow"] = len(my_follow)
        "新客户"
        new_cus = total_customer.filter(cus_coming_counts__lt=2).values()
        data["new_cus"] = len(new_cus)
        "待接单服务"
        waiting_cus = total_customer.filter(open_id=None).values()
        data["waiting_cus"] = len(waiting_cus)
        return JsonResponse(data, safe=False)
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        tel_num = request.GET.get('tel_num').strip()
        data = {}
        customer = Customer.objects.filter(cus_tel_num=tel_num).values()
        open_id = request.session.get("open_id")
        user_name = User.objects.get(open_id=open_id).user_name
        data['data'] = list(customer)
        data['user_name'] = user_name
        return JsonResponse(data, safe=False)


class UserView(View,CommonResponseMixin):
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        open_id = request.session.get("open_id")
        user = User.objects.get(open_id=open_id)
        data = {}
        data['user_name'] = [user.user_name,'用户名']
        data['tel_num'] = [user.tel_num,'电话号码']
        return JsonResponse(data, safe=False)
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        content = post_data.get('content').strip()
        title = post_data.get('title').strip()
        data={title:content}
        response = {}
        if not content or not title:
            response['message'] = "数据发送错误"
            response['code'] = ReturnCode.UNAUHORIZED
            return JsonResponse(data=response, safe=False)
        open_id = request.session.get("open_id")
        User.objects.filter(open_id=open_id).update(**data)
        response = wrap_json_response(code=ReturnCode.SUCCESS, data="更新成功")
        return JsonResponse(data=response, safe=False)


def __author_by_code(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    code = post_data.get('code').strip()
    appid = post_data.get('appId').strip()
    avatarurl = post_data.get('avatarUrl').strip()
    first_people = False
    response = {}
    if not code or not appid:
        response['message'] = "授权登录失败"
        response['code'] = ReturnCode.UNAUHORIZED
        return JsonResponse(data=response, safe=False)
    data = c2s(appid,code)
    open_id = data.get("openid")
    if not open_id:
        response= wrap_json_response(code=ReturnCode.FAILED,data="授权登录失败")
        return JsonResponse(data=response,safe=False)
    request.session['open_id'] = open_id
    request.session['is_authorized'] = True
    if not User.objects.filter(open_id=open_id):
        new_user = User(open_id=open_id, avatar_url=avatarurl)
        new_user.save()
        first_people = True
    response = wrap_json_response(code=ReturnCode.SUCCESS,data="授权登录成功")
    response['first_people'] = first_people
    response['open_id'] = open_id
    return JsonResponse(data=response,safe=False)

def authorized(request):
    return __author_by_code(request)


def c2s(appid,code):
    Secret_id = "6ccdaca17d88860cadd4cf8d152fc14a"
    api = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"%(appid,Secret_id,code)
    response = requests.get(url=api)
    data = json.loads(response.text)
    return data


