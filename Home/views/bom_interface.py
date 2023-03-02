import re
import pandas as pd 
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from Home.models import Product, Bom_sum_record, Inventory, SaleOutInventory, PurchaseOrder
from B.models import Projection, B1nz, Boms
from B.views.boms import del_data
from B.views.b1nz import get_1nz_data
from B.views.bsjxqd import get_sjxqd_data
from B.views.common import choice_map, bom_map_inverse, bom_map

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
    bom = req.GET.get('bom')


    start = (page - 1) * limit
    end = page * limit 

    if bom == 'all':
        bom_sum_obj = Bom_sum_record.objects.all()
    else:
        bom_sum_obj = Bom_sum_record.objects.filter(pro_sys_bc__contains=bom)
    last_date = datetime.now().strftime("%Y-%m-%d")
    if bom_sum_obj:
        last_date = bom_sum_obj.order_by("-id").first().submit_date
    
    # bom_sum_obj = bom_sum_obj.filter(submit_date=last_date).order_by("-total_sum")
    bom_sum_obj = bom_sum_obj.order_by("-total_sum")
    return render(req, "bom_sum.html", {"datas": bom_sum_obj[start: end], "count": bom_sum_obj.count(), "bom_name": bom_map})


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
    Bom_sum_record.objects.bulk_create(data)
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

    content = {
        "code": 0,
        "msg": "success",
        "data": [],
        "count": 0
    }
    json_content = JsonResponse(content)
    if interface == "ALL1nz":
        json_content = get_1nz_data(req, "all_1nz")
    elif interface == "sjXqdall":
        json_content = get_sjxqd_data(req, "all_sjxqd")
    elif interface == "warehouse":
        data = [{
            "no": i+1,
            "product_code":x.product_code,
            "inventory_code":x.inventory_code,
            "inventory_name":x.inventory_name,
            "warehouse_code":x.warehouse_code,
            "warehouse_name":x.warehouse_name,
            "inven_now_num":x.inven_now_num,
            "to_inventory_num":x.to_inventory_num,
            "inven_delivery_num":x.inven_delivery_num,
            "inven_class_code":x.inven_class_code,
            "inven_class_name":x.inven_class_name,
            "inven_con_code":x.inven_con_code,
            "need_flow_code":x.need_flow_code,
        } for i, x in zip(numbers, Inventory.objects.all()[start:end])]
        
        content["data"] = data
        content["count"] = Inventory.objects.all().count()
        print(content)
        json_content = JsonResponse(content)
    elif interface == "sale_out":
        data = [{
            "no": i+1,
            "three_product_code":x.three_product_code,
            "product_code":x.product_code,
            "inventory_code":x.inventory_code,
            "ac_set":x.ac_set,
            "warehouse_code":x.warehouse_code,
            "warehouse_name":x.warehouse_name,
            "warehouse_out_code":x.warehouse_out_code,
            "out_num":x.out_num,
            "out_date":x.out_date,
            "order_code":x.order_code,
            "reviewed_by":x.reviewed_by,
            "audit_date":x.audit_date,
            "out_type":x.out_type,
        } for i, x in zip(numbers, SaleOutInventory.objects.all()[start:end])]
        content["data"] = data
        content["count"] = SaleOutInventory.objects.all().count()
        json_content = JsonResponse(content)
    elif interface == "purchase":
        print("b")
        data = [{
            "no": i+1,
            "three_product_code":x.three_product_code,
            "product_code":x.product_code,
            "inventory_code":x.inventory_code,
            "order_code":x.order_code,
            "business_type":x.business_type,
            "purchase_type":x.purchase_type,
            "purchase_num":x.purchase_num,
            "upper_order_code":x.upper_order_code,
            "prepared_by":x.prepared_by,
            "order_date":x.order_date,
            "reviewed_by":x.reviewed_by,
            "audit_date":x.audit_date,
            "arrive_date":x.arrive_date,
            "warehouse_status":x.warehouse_status,
            "remark":x.remark,
        } for i, x in zip(numbers, PurchaseOrder.objects.all()[start:end])]
        content["data"] = data
        content["count"] = PurchaseOrder.objects.all().count()
        json_content = JsonResponse(content)
    return json_content
   
