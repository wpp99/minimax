import re
import pandas as pd 
from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from Home.models import Product, Bom_sum_record, Inventory, SaleOutInventory, PurchaseOrder, Guan
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


@csrf_exempt
def search(req):
    url = "/yy/"
    field_dict = {field.name: field.verbose_name for field in SaleOutInventory._meta.get_fields()}
    return render(req, "search.html", {'url': url, "field": field_dict})

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
    data = []
    content = {
        "code": 0,
        "msg": "success",
        "data": [],
        "count": 0
    }
    
    sgy02_list = [p_obj.inventory_code for p_obj in Product.objects.filter(pro_system=2)]
    condiction = req.GET.get("con")
    
    json_content = JsonResponse(content)
    if interface == "ALL1nz":
        json_content = get_1nz_data(req, "all_1nz")
    elif interface == "sjXqdall":
        json_content = get_sjxqd_data(req, "all_sjxqd")
    elif interface == "warehouse":
        data_obj = Inventory.objects.all()
        if req.GET.get("Q7") == "true":
            cangku = ["1号库-通用件库KC", "2号库-生产产成品库", "2号库-生产原材料库", "3号库-出口商品库", "4号库-免费库", "4号库-委托保管库", 
                      "5号库-进料加工保税产成品库", "6号库-委托加工产成品库", "销售出库单列表SGY02"]
            data_obj = Inventory.objects.filter(Q(warehouse_name__in=cangku)).exclude(Q(warehouse_name="2号库-生产原材料库"), ~Q(inventory_code__in=sgy02_list))   
        if condiction:
            data_obj = data_obj.filter(Q(product_code=condiction) | Q(inventory_code=condiction))
        for i, x in zip(numbers, data_obj[start:end]):
            product_obj = Product.objects.filter(inventory_code=x.inventory_code).first()
            data.append({
                "no": i+1,
                "product_code":x.product_code,
                "inventory_code":x.inventory_code,
                "inventory_name":product_obj.product_name,
                "warehouse_code":x.warehouse_code,
                "warehouse_name":x.warehouse_name,
                "inven_now_num":x.inven_now_num,
                "to_inventory_num":x.to_inventory_num,
                "inven_delivery_num":x.inven_delivery_num,
                "inven_class_code":x.inven_class_code,
                "inven_class_name":x.inven_class_name,
                "inven_con_code":x.inven_con_code,
                "need_flow_code":x.need_flow_code,
            })

        
        content["data"] = data
        content["count"] = data_obj.count()
       
        json_content = JsonResponse(content)
    elif interface == "sale_out":
        data_obj = SaleOutInventory.objects.all()
        if req.GET.get("Q5") == "true":
            data_obj = SaleOutInventory.objects.exclude(Q(ac_set="SGY02") | Q(reviewed_by="") | Q(out_type="委托加工成品采购") | Q(depart__startswith="D9")) 
        if condiction:
            data_obj = data_obj.filter(Q(product_code=condiction) | Q(inventory_code=condiction) | Q(pro_batch__contains=condiction))
        for i, x in zip(numbers, data_obj[start:end]):
            data.append({
                "no": i+1,
                "three_product_code":x.three_product_code,
                "pro_batch":x.pro_batch,
                "depart":x.depart,
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
                "srd_pro_code":x.srd_pro_code,
            })
        content["data"] = data
        content["count"] = data_obj.count()
        json_content = JsonResponse(content)
    elif interface == "purchase":
        data_obj = PurchaseOrder.objects.all()
        con1 = Q(pro_batch__contains=condiction) | Q(order_code=condiction) | Q(product_code=condiction) | Q(inventory_code=condiction)
        if req.GET.get("Q4") == "true":
            data_obj = PurchaseOrder.objects.exclude(Q(ac_set="SGY02") | Q(ac_set="Q9")).exclude(Q(reviewed_by="")  | Q(depart__startswith="D9")).exclude(
                (Q(ac_set=1) | Q(ac_set=2)) & Q(business_type="普通采购") & ~Q(purchase_type="委托加工成品采购") 
            )
        if req.GET.get("Q90") == "true":
            data_obj = PurchaseOrder.objects.filter(ac_set="Q9")
        if req.GET.get("Q9") == "true":
            data_obj = PurchaseOrder.objects.exclude(~Q(ac_set="SGY02") & (Q(purchase_type="项目采购") | Q(purchase_type="生产采购")  | Q(purchase_type__contains="备件") | Q(pro_des__contains="备件"))
                                                    ).exclude( Q(ac_set="SGY02"), (~Q(purchase_type="生产采购") | ~Q(business_type="普通采购") | Q(audit_date__isnull=True) | ~Q(inventory_code__in=sgy02_list) ))
                                                   
        if condiction:
            data_obj = data_obj.filter(con1)
        for i, x in zip(numbers, data_obj[start:end]):
            data.append({
                "no": i+1,
                "three_product_code":x.three_product_code,
                "ac_set":x.ac_set,
                "pro_batch":x.pro_batch,
                "pro_des":x.pro_des,
                "depart":x.depart,
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
            })
        content["data"] = data
        content["count"] = data_obj.count()
        json_content = JsonResponse(content)
    return json_content
   
