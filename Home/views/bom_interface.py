import re
import pandas as pd 
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from Home.models import Product, Bom_sum_record
from B.models import Projection, B1nz, Boms
from B.views.boms import del_data
from B.views.b1nz import get_1nz_data
from B.views.bsjxqd import get_sjxqd_data
from B.views.common import choice_map, bom_map_inverse

bom_merge = {}
bom_merge_list = []



@xframe_options_exempt
def bom_interface(req):
    interface = req.path_info
    interface = interface.split("/")[-1]
    return render(req, 'bom_interface.html', {"interface": interface})


@xframe_options_exempt
def bom_sum(req):
    """bom_sum 页面"""
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit 

    bom_sum_obj = Bom_sum_record.objects.all()
    last_date = datetime.now().strftime("%Y-%m-%d")
    if bom_sum_obj:
        last_date = bom_sum_obj.order_by("-id").first().submit_date
    
    data_obj = Bom_sum_record.objects.filter(submit_date = last_date).order_by("-total_sum")
    
    return render(req, "bom_sum.html", {"datas": data_obj[start: end], "count": data_obj.count()})


def bc_sum(d):
    """处理bc的数字"""
    sum_bc = 0
    for k, v in d.items():
        sum_bc += int(v)
    return sum_bc


def get_bom_data():
    """从B表中获取bom数据"""
    datalist = {}
    data_obj = Boms.objects.all()
    total_sum = 0
    for data_item in data_obj:
        if data_item.bc:
            product_obj = Product.objects.filter(product_code=data_item.product_code).first()
            d = {
                    "pro_no": str(data_item.pro_no),
                    "m_system": bom_map_inverse[data_item.m_system],
                    "bc": data_item.bc,
                    "bc_sum": bc_sum(data_item.bc),
                }
            
            if data_item.product_code in datalist.keys():
                datalist[data_item.product_code]["datas_product"].append(d)
                datalist[data_item.product_code]["total_sum"] += bc_sum(data_item.bc)
            else:
                total_sum = bc_sum(data_item.bc)
                datalist[data_item.product_code] = {
                    "inventory_code": product_obj.inventory_code,
                    "datas_product": [d],
                    "total_sum": total_sum
                }

    # with open("./static/bom_interface.txt", "a", encoding="utf-8") as f:
    #     for key, value in datalist.items():
    #         f.writelines(str(key) + "\t") 
    #         for k, v in value.items():
    #             f.writelines(str(k) + ":" + str(v) + "\t")
    #         f.writelines("\n")
    return datalist



def bom_submit(req):
    """汇总bom并导入数据库"""
    datalist = get_bom_data()
    data = []
    for key, value in datalist.items():
        bom_record = Bom_sum_record(
            product_code = key,
            inventory_code = value["inventory_code"],
            total_sum = value["total_sum"],
            pro_sys_bc = value["datas_product"],
        )
        data.append(bom_record)
    Bom_sum_record.objects.bulk_update_or_create(data, ["pro_sys_bc", "total_sum", "submit_date"], match_field=["product_code"])
    content = {
        "code": 0,
        "msg": "提取成功"
    }
    return JsonResponse(content)


def get_interface_data(req, interface):
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit 
    numbers = [*range(start, end)]

    json_content = {}
    if interface == "ALL1nz":
        json_content = get_1nz_data(req, "all_1nz")
    elif interface == "sjXqdall":
        json_content = get_sjxqd_data(req, "all_sjxqd")
    
    return json_content
    # return JsonResponse(content)
