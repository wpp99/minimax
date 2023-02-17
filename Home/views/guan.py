import re
import pandas as pd 

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from Home.models import Product, Guan
from B.models import Projection, B1nz, Boms
from B.views.boms import del_data
from B.views.b1nz import get_1nz_data
from B.views.bsjxqd import get_sjxqd_data
from B.views.common import choice_map


@xframe_options_exempt
def guan(req):
    return render(req, "guan.html")


def get_guan_data(req):
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit 
    number = [*range(start, end)]
    data_obj = Guan.objects.all()
    data = [dict(
        no = i + 1,
        pro_no = x.pro_no, 
        batch = x.batch,
        product_num = x.product_num,
        prod_task_content = x.prod_task_content,
        product_code = x.product_code,
        order_date = x.order_date,
        acc_date = x.acc_date,
        sj_date = x.sj_date,
        expect_date = x.expect_date,
        table0_update_date = x.table0_update_date,
        first_sign_date = x.first_sign_date,
        change_date = x.change_date,
        responsible = x.responsible,
        inventory_code = x.inventory_code,
        status = x.status,
        warehousing_date =x.warehousing_date,
        warehousing_num = x.warehousing_num,
        warehousing_code =x.warehousing_code,
        change_record = x.change_record,
        attribute = x.attribute,
        description = x.description,
        jin1 = x.jin1,
        warehousing_status = x.warehousing_status,
        assembly_method = x.assembly_method,
        last_deliver_date = x.last_deliver_date,
        file_place = x.file_place,
        to_warehouse = x.to_warehouse,
        change_times = x.change_times,
        under_construction =x.under_construction,
        success_num = x.success_num,
        need_1nz = x.need_1nz,
        manage_order_no = x.manage_order_no,
        sales_order = x.sales_order,
        manage_code = x.manage_code,
        process_code = x.process_code,
        on_delivery_rate =x.on_delivery_rate,
        yield_rate = x.yield_rate,
        man_assembly_time =  x.man_assembly_time,
        el_assembly_time =x.el_assembly_time,
        quality_check_time = x.quality_check_time,
        op_overlap_rate = x.op_overlap_rate,
        inventory_num = x.inventory_num,
        warehouse_out_num = x.warehouse_out_num,
        assembly_cycle = x.assembly_cycle,
        srd_num = x.srd_num,
    )for i, x in zip(number, data_obj)]

    content = {
        "code": 0,
        "msg": "",
        "count": data_obj.count(),
        "data": data,
    }

    return JsonResponse(content)


def guan_add(req):
    return


def guan_edit(req, id):
    return 

def guan_delete(req, id):
    return