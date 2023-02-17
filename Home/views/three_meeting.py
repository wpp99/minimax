import re
import pandas as pd 

from django.db.models import Q
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from Home.models import Product, ThreePartMeet, threePartRemark, get_next_week2_date
from B.models import Projection, B1nz, Boms
from B.views.boms import del_data
from B.views.common import choice_map

bom_merge = {}
bom_merge_list = []


@xframe_options_exempt
def three_meeting(req):
    return render(req, 'three_meeting.html', {"path_info": req.path_info})


def get_meeting_data(req):
    """获取三部会审数据"""
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit 
    numbers = [*range(start, end)]
    data_obj = ThreePartMeet.objects.all().order_by("-id")
    data = [{
        "no": i+1,
        "depart": x.depart,
        "pro_no": x.pro_no,
        "batch": x.batch,
        "participants": x.participants,
        "meet_date": x.meet_date,
        "remark": x.remark,
        "meet_sign_filepath": x.meet_sign_filepath,
        "status": x.get_status_display(),
        "id": x.id,
    }for i, x in zip(numbers, data_obj[start:end])]
    content = {
        "code": 0,
        "msg": "成功",
        "data": data,
        "count": data_obj.count()
    }
    return JsonResponse(content)


class MeetingForm(ModelForm):
    class Meta:
        model = ThreePartMeet
        # fields = '__all__'
        exclude = ['threemeet_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {'class': 'layui-input'}


@xframe_options_exempt
def meeting_add(req):
    """添加三部会审"""
    action = "/meeting/add"
    date_week2 =  get_next_week2_date()
    if req.method == 'GET':
        form = MeetingForm()
        return render(req, 'meeting_add.html', {'form': form,  "date": date_week2, "action": action, })
    # condiction = Product.objects.filter(Q(product_code=req.POST['product_code']) | Q(inventory_code=req.POST['inventory_code']))
    three_obj = ThreePartMeet.objects.all()
    threemeet_code = 't0000000001'
    if three_obj:
        last_id = three_obj.order_by("-id").first().id
        threemeet_code = 't' + str(last_id+1).rjust(9, '0')
    req.POST._mutable =True    #  默认不能修改
    req.POST[threemeet_code] = threemeet_code
    form = MeetingForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/threemeeting")
    return render(req, 'meeting_add.html', {'form': form, "date": date_week2, "action":action, })


@xframe_options_exempt
def meeting_edit(req, id):
    """修改三部会审"""
    data = ThreePartMeet.objects.filter(id=id).first()
    action = f"/meeting/edit/{id}"
    
    if req.method == "GET":
        form = MeetingForm(instance=data)
        return render(req, "meeting_add.html", {"form": form, "action": action, })
    form = MeetingForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/threemeeting')
    return render(req, "meeting_add.html", {"form": form, "action": action, })


def meeting_delete(req, id):
    """删除三部会审"""
    ThreePartMeet.objects.filter(id=id).delete()
    return redirect('/threemeeting')


def extract_meet_data(req):
    """
    提取已关闭会审的数据， 存入数据库
    """
    datalist = []
    
    condiction = Q(status=4)
    for threepart_obj in ThreePartMeet.objects.filter(condiction):
        threemeet_code = threepart_obj.threemeet_code
        pro_no = threepart_obj.pro_no
        batch = threepart_obj.batch
        depart = threepart_obj.depart
        batchs = re.findall("(DY\d{3})", str(batch))
        i = 1
        for batch in batchs:
            for boms_object in Boms.objects.filter(Q(bc__has_key=batch), pro_no=pro_no):
                product_code = boms_object.product_code
                bc = boms_object.bc
                three_product_code = threemeet_code + "_" + str(i).rjust(7, '0')
                data = {
                    'three_product_code': three_product_code,
                    'threemeet_code': threemeet_code,
                    'pro_no': str(pro_no),
                    'batch': batch,
                    'product_code': product_code,
                    'num': bc[batch],
                    'depart': depart
                }
                three_remark = threePartRemark(**data)
                datalist.append(three_remark)
                i += 1
    threePartRemark.objects.bulk_update_or_create(datalist, ["pro_no", "batch", "product_code", "num", "depart"], match_field=["three_product_code"])
    content = {
        "code": 0,
        "msg": "success"
    }
    return JsonResponse(content)


def get_purchase_data(req):
    """获取threepartRemark 中的数据"""
    limit = int(req.GET.get("limit"))
    page = int(req.GET.get("page"))
    start = (page - 1) * limit
    end = page * limit

    data = []
    for i, item in enumerate(threePartRemark.objects.all()):
        b1nzobj = B1nz.objects.filter(pro_no=item.pro_no, batch_no=item.batch).first()
        product_obj = Product.objects.filter(product_code = item.product_code).first()
        data.append({
            'no': i + 1,
            'pro_no': item.pro_no,
            'batch': item.batch,
            'deliver_date': b1nzobj.deliver_date,
            'port': b1nzobj.port,
            'trans_method': b1nzobj.get_trans_method_display(),
            'directShipment': b1nzobj.get_directShipment_display(),
            'trans_to': b1nzobj.trans_to,
            'depart': item.depart,
            'product_code': item.product_code,
            'inventory_code': product_obj.inventory_code,
            'product_name': product_obj.product_name,
            'product_type': product_obj.product_type,
            'supply': product_obj.supply,
            'num': item.num,
            # 'inventory_num': num,
            # 'loss_num': num - del_data(bc)
        })
    
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data[start:end]
    }
    return JsonResponse(content)


def get_meeting_product_data(req, his_this):
    """获取本次会审的数据"""
    limit = int(req.GET.get("limit"))
    page = int(req.GET.get("page"))
    start = (page - 1) * limit
    end = page * limit
    meet_date=get_next_week2_date()

    meet_date_obj = ThreePartMeet.objects.all().order_by("-meet_date").first()
    if meet_date_obj:
        meet_date = meet_date_obj.meet_date

    condiction = Q(meet_date=meet_date)
    # if his_this == "history":
    #     condiction = Q(status=2) | Q(status=3)
    data = []
    i = 1
    for threepart_obj in ThreePartMeet.objects.filter(condiction):
        threemeet_code = threepart_obj.threemeet_code
        depart = threepart_obj.depart
        pro_no = threepart_obj.pro_no
        batch = threepart_obj.batch
        batchs = re.findall("(DY\d{3})", str(batch))
        
        for batch in batchs:
            
            b1nz_object = B1nz.objects.filter(pro_no=pro_no, batch_no=batch).first()
            deliver_date = b1nz_object.deliver_date
            port = b1nz_object.port
            trans_method = b1nz_object.get_trans_method_display()
            directShipment = b1nz_object.get_directShipment_display()
            trans_to = b1nz_object.trans_to
            for boms_object in Boms.objects.filter(Q(bc__has_key=batch), pro_no=pro_no):
                product_code = boms_object.product_code
                bc = boms_object.bc
                product_object = Product.objects.filter(product_code=product_code).first()
                product_name = product_object.product_name
                product_type = product_object.product_type
                supply = product_object.supply
                num = product_object.inventory_num
                three_product_code = threemeet_code + "_" + str(i).rjust(7, '0')
                data.append({
                    'no': i,
                    'three_product_code': three_product_code,
                    'threemeet_code': threemeet_code,
                    'pro_no': str(pro_no),
                    'batch': batch,
                    'deliver_date': deliver_date,
                    'port': port,
                    'trans_method': trans_method,
                    'directShipment': directShipment,
                    'trans_to': trans_to,
                    'depart_no': depart,
                    'product_code': product_code,
                    'product_name': product_name,
                    'product_type': product_type,
                    'supply': supply,
                    'num': bc[batch],
                    'inventory_num': num,
                    'loss_num': num - del_data(bc)
                })
                i = i + 1
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data[start:end]
    }
    return JsonResponse(content)