from django.http.response import JsonResponse,FileResponse
import json
import requests
from django.views import View
from utils.util import ReturnCode,wrap_json_response,CommonResponseMixin,is_authorized
from .models import User,Customer,Cus_Follow_Record,Cus_Sign_Record
import datetime

# Create your views here
class SignCus(View,CommonResponseMixin):
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        data ={}
        open_id = request.session.get("open_id")
        cus = Customer.objects.filter(open_id=open_id,cus_sign="1").values()
        data['data'] = list(cus)
        return JsonResponse(data, safe=False)


class SearchCus(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        name = post_data.get("name").strip()
        data = {}
        if name:
            cus = Customer.objects.filter(cus_name__contains=name).values()
            data['data'] = list(cus)
        else:
            data['data'] = []
        return JsonResponse(data, safe=False)


class AllCus(View,CommonResponseMixin):
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        data ={}
        open_id = request.session.get("open_id")
        cus = Customer.objects.filter(open_id=open_id).values()
        data['data'] = list(cus)
        return JsonResponse(data, safe=False)
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        data = {}
        cus = Customer.objects.filter(open_id=None).values()
        data['data'] = list(cus)
        return JsonResponse(data, safe=False)

class CusInfoChange(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        data = {}
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        tel_num = post_data.get("tel_num").strip()
        cus_tel_num = post_data.get("cus_tel_num").strip()
        cus_adress = post_data.get("cus_adress").strip()
        cus_wanting_level = post_data.get("cus_wanting_level")
        cus_wanting_cars = post_data.get("cus_wanting_cars").strip()
        cus_budget =int(post_data.get("cus_budget").strip())
        cus_wanting_reason = post_data.get("cus_wanting_reason").strip()
        cus_coming_rules = post_data.get("cus_coming_rules").strip()
        open_id = request.session.get("open_id")
        treat_counts = Customer.objects.filter(cus_tel_num=tel_num).values("cus_treat_counts")[0]
        treat_counts = treat_counts['cus_treat_counts']
        current = datetime.datetime.now()
        Customer.objects.filter(cus_tel_num=tel_num).update(cus_tel_num=cus_tel_num,cus_adress=cus_adress,cus_wanting_level=cus_wanting_level,cus_treat_counts=treat_counts+1,
                             cus_wanting_cars=cus_wanting_cars,cus_budget=cus_budget,cus_wanting_reason=cus_wanting_reason,cus_coming_rules=cus_coming_rules,cus_following_time=current)
        Cus_Follow_Record.objects.create(open_id=open_id,cus_tel_num_id=cus_tel_num,cus_follow_time=current,cus_wanting_cars=cus_wanting_cars,
                                         cus_budget=cus_budget,cus_wangting_level=cus_wanting_level)
        customer = Customer.objects.filter(cus_tel_num=cus_tel_num).values()
        data['data'] = list(customer)
        return JsonResponse(data, safe=False)

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
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        data = {}
        open_id = request.session.get("open_id")
        cus = Customer.objects.filter(open_id=open_id,cus_sign="0").values()
        data['data'] = list(cus)
        return JsonResponse(data, safe=False)



class FollowView(View,CommonResponseMixin):
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        data = {}
        tel_num = request.GET.get('tel_num').strip()
        sign_record = Cus_Sign_Record.objects.filter(cus_tel_num_id=tel_num).values()
        sign_record = list(sign_record)
        if sign_record:
            open_id = sign_record[0]['open_id']
            user_name = User.objects.get(open_id=open_id).user_name
            sign_record[0]['user_name'] = user_name
        data['sign_record'] = sign_record
        records = Cus_Follow_Record.objects.filter(cus_tel_num_id=tel_num).values()
        records = list(records)
        for record in records:
            open_id = record['open_id']
            user_name = User.objects.get(open_id=open_id).user_name
            record['user_name'] = user_name
        data["data"] = records
        return JsonResponse(data, safe=False)
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        tel_num = post_data.get("tel_num").strip()
        cus_budget = post_data.get("cus_budget").strip()
        cus_wangting_level = post_data.get("cus_wangting_level")
        cus_wanting_cars = post_data.get("cus_wanting_cars").strip()
        cus_next_following_time = post_data.get("cus_next_following_time").strip()
        mark = post_data.get("mark").strip()
        current = datetime.datetime.now()
        open_id = request.session.get("open_id")
        Cus_Follow_Record.objects.create(open_id=open_id,cus_tel_num_id=tel_num,cus_follow_time=current,cus_wanting_cars=cus_wanting_cars,mark=mark,
                                         cus_budget=cus_budget,cus_wangting_level=cus_wangting_level,cus_next_following_time=cus_next_following_time)
        treat_counts = Customer.objects.filter(cus_tel_num=tel_num).values("cus_treat_counts")[0]
        treat_counts = treat_counts['cus_treat_counts']
        Customer.objects.filter(cus_tel_num=tel_num).update(cus_following_time=current,cus_wanting_cars=cus_wanting_cars,cus_budget=cus_budget,
                                cus_treat_counts=treat_counts+1, cus_next_following_time=cus_next_following_time,cus_wanting_level=cus_wangting_level)
        response = wrap_json_response(code=ReturnCode.SUCCESS, data="更新成功")
        return JsonResponse(data=response, safe=False)

class WarnView(View,CommonResponseMixin):
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        data = {}
        open_id = request.session.get("open_id")
        customer = Customer.objects.filter(cus_coming_counts__gte=15,cus_sign="0",open_id=open_id).values()
        data['coming_counts'] = list(customer)
        # data['coming_counts'].append({"reason":"到店次数多，未签单"})
        customer = Customer.objects.filter(cus_treat_counts__gte=15, cus_sign="0", open_id=open_id).values()
        data['treat_counts'] = list(customer)
        # data['treat_counts'].append({"reason": "接待次数多，未签单"})
        customer = Customer.objects.filter(cus_budget__gte=100,open_id=open_id,cus_sign="0",cus_wanting_level__gte=3).values()
        data['budget'] = list(customer)
        # data['budget'].append({"reason":"预算大，购买意愿强，未签单"})
        return JsonResponse(data, safe=False)

class SignView(View,CommonResponseMixin):
    def post(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        open_id = request.session.get("open_id")
        post_data = request.body.decode('utf-8')
        print(post_data)
        post_data = json.loads(post_data)
        tel_num = post_data.get("tel_num").strip()
        cus_cost = post_data.get("cus_cost").strip()
        cus_buying_cars = post_data.get("cus_buying_cars").strip()
        current = datetime.datetime.now()
        Customer.objects.filter(cus_tel_num=tel_num).update(cus_sign="1")
        Cus_Sign_Record.objects.create(open_id=open_id,cus_cost=cus_cost,cus_buying_cars=cus_buying_cars,cus_sign_time=current,cus_tel_num_id=tel_num)
        response = wrap_json_response(code=ReturnCode.SUCCESS, data="更新成功")
        return JsonResponse(data=response, safe=False)
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED, message="failed")
            return JsonResponse(response, safe=False)
        tel_num = request.GET.get('tel_num').strip()
        Customer.objects.filter(cus_tel_num=tel_num).update(open_id="")
        response = wrap_json_response(code=ReturnCode.SUCCESS, data="更新成功")
        return JsonResponse(data=response, safe=False)





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
    def get(self,request):
        if not is_authorized(request):
            response = self.wrap_json_response(code=ReturnCode.FAILED,message="failed")
            return JsonResponse(response,safe=False)
        tel_num = request.GET.get('tel_num').strip()
        open_id = request.session.get("open_id")
        Customer.objects.filter(cus_tel_num=tel_num).update(open_id=open_id)
        response = wrap_json_response(code=ReturnCode.SUCCESS, data="更新成功")
        return JsonResponse(data=response, safe=False)

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
        data['data'] = list(customer)
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


