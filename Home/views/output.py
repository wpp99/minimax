from openpyxl import Workbook, load_workbook
from io import BytesIO

from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse, JsonResponse

from B.models import B1nz, BsjXQDD, Boms, Projection
from B.views.common import bom_name, bom_map
from B.views.uploads import find_pro_path, load_B

from Home.models import Product


def file_iterator(file_name,chunk_size=512):
    with open(file_name, 'rb', encoding='utf-8') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def output(req):
    pro_no = req.GET.get("pro_no")
    wb = load_workbook("./B/static/files/ML_allxxxxxxxxx.xlsx")
    wb.encoding = 'utf-8'

    out_1nz(wb, pro_no)
    out_sjXQD(wb, pro_no)

    for sheet in bom_name:
        bb_keys = get_keys(pro_no, sheet, 'bb')
        bc_keys = get_keys(pro_no, sheet, 'bc')
        bd_keys = get_keys(pro_no, sheet, 'bd')
        be_keys = get_keys(pro_no, sheet, 'be')
        bb_dict, bb_add_col = set_keys(wb, bb_keys, sheet, ord('A'), ord('T'))
        bc_dict, bc_add_col = set_keys(wb, bc_keys, sheet, ord('B'), ord('H')+bb_add_col)
        bd_dict, bd_add_col = set_keys(wb, bd_keys, sheet, ord('B'), ord('V')+bc_add_col)
        be_dict, be_add_col = set_keys(wb, be_keys, sheet, ord('C'), ord('J')+bd_add_col)
        print(bb_dict)
        print(bc_dict)
        print(bd_dict)
        print(be_dict)
        out_bom(wb, pro_no, sheet, bb_dict, bc_dict, bd_dict, be_dict)

    output_files = BytesIO()
    wb.save(output_files)
    output_files.seek(0)
    response = HttpResponse(output_files.getvalue())

    # response = StreamingHttpResponse(file_iterator(wb))
    response["Content-type"] = 'application/vnd.ms-excel'
    file_name = f"ML_all{pro_no}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    
    return response


def out_1nz(wb, pro_no):
    sh_b1nz = wb.get_sheet_by_name("1nz")
    i = 10
    for b1nz_obj in B1nz.objects.filter(pro_no=pro_no):
        sh_b1nz[f"C{i}"] = b1nz_obj.batch_no
        sh_b1nz[f"D{i}"] = b1nz_obj.description
        sh_b1nz[f"E{i}"] = b1nz_obj.area
        sh_b1nz[f"F{i}"] = b1nz_obj.design_date
        sh_b1nz[f"G{i}"] = b1nz_obj.deliver_date
        sh_b1nz[f"H{i}"] = b1nz_obj.itp_date
        sh_b1nz[f"I{i}"] = b1nz_obj.port
        sh_b1nz[f"J{i}"] = b1nz_obj.get_trans_method_display()
        sh_b1nz[f"K{i}"] = b1nz_obj.grossWeight
        sh_b1nz[f"L{i}"] = b1nz_obj.volume
        sh_b1nz[f"M{i}"] = b1nz_obj.ship_no
        sh_b1nz[f"N{i}"] = b1nz_obj.wayBill_no
        sh_b1nz[f"O{i}"] = b1nz_obj.arrive_date
        sh_b1nz[f"R{i}"] = b1nz_obj.con_date
        sh_b1nz[f"S{i}"] = b1nz_obj.nz_date
        sh_b1nz[f"T{i}"] = b1nz_obj.true_date
        sh_b1nz[f"U{i}"] = b1nz_obj.mx_body
        sh_b1nz[f"V{i}"] = b1nz_obj.get_trans_des_display()
        sh_b1nz[f"W{i}"] = b1nz_obj.pack_des
        sh_b1nz[f"X{i}"] = b1nz_obj.get_three_status_display()
        sh_b1nz[f"Y{i}"] = b1nz_obj.get_directShipment_display()
        sh_b1nz[f"Z{i}"] = b1nz_obj.trans_to
        i += 1

 
def out_sjXQD(wb, pro_no):
    i = 8
    sh_sjxqd = wb.get_sheet_by_name("sjXQD")
    for sj_obj in BsjXQDD.objects.filter(pro_no=pro_no):
        sh_sjxqd[f"B{i}"] = sj_obj.num
        sh_sjxqd[f"C{i}"] = sj_obj.sys_code
        sh_sjxqd[f"D{i}"] = sj_obj.zgxy
        sh_sjxqd[f"E{i}"] = sj_obj.content_zgxy
        sh_sjxqd[f"F{i}"] = sj_obj.start_date
        sh_sjxqd[f"G{i}"] = sj_obj.close_date
        sh_sjxqd[f"H{i}"] = sj_obj.res_per
        sh_sjxqd[f"I{i}"] = sj_obj.audit_level
        sh_sjxqd[f"J{i}"] = sj_obj.status
        col_1 = ord("K")
        for date_item in sj_obj.date_seria.split(";"):
            if date_item:
                sh_sjxqd[f"{chr(col_1)}{i}"] = date_item
                col_1 += 1
        sh_sjxqd[f"U{i}"] = sj_obj.sjxqd_remark
        sh_sjxqd[f"V{i}"] = sj_obj.xqd0
        sh_sjxqd[f"W{i}"] = sj_obj.xqd1
        sh_sjxqd[f"X{i}"] = sj_obj.xqd2
        sh_sjxqd[f"Y{i}"] = sj_obj.xqd_remind
        i += 1


def get_keys(pro_no, sheet, mode):
    """获取表头"""
    keys = []
    for b_obj in Boms.objects.filter(pro_no=pro_no, m_system=bom_map[sheet]):
        if mode == 'bb':
            keys.extend(b_obj.bb.keys())
        elif mode == 'bc':
            keys.extend(b_obj.bc.keys())
        elif mode == 'bd':
            keys.extend(b_obj.bd.keys())
        elif mode == 'be':
            keys.extend(b_obj.be_arrive.keys())
    return set(keys)


def set_keys(wb, keys, sheet, col1, col2):
    """设置表头"""
    if col2 > 90:
        col2 = 65
        col1 += 1
    # keys = get_keys(pro_no, sheet)
    keys_dict = {}
    # bom_obj = Boms.objects.filter(pro_no=pro_no, m_system=sheet)
    sh_bom = wb.get_sheet_by_name(sheet)
    add_cols = len(keys) - 12 
    if len(keys) > 12:
        start_col = (col1 - 64) * 26 + col2 - 64
        for i in range(add_cols):
            sh_bom.insert_cols(start_col + 9 + i)
    for key in keys:
        keys_dict[key] = chr(col1) + chr(col2)
        sh_bom[f"{keys_dict[key]}7"] = key
        col2 += 1
        if col2 > 90:
            col2 = 65
            col1 += 1
    if add_cols < 0:
        add_cols = 0
    return keys_dict, add_cols


def out_bom(wb, pro_no, m_system, dict_head_bb, dict_head_bc, dict_head_bd, dict_head_be):
    """修改bom"""
    sh_bom = wb.get_sheet_by_name(m_system)
    inventory_code_list = []
    for bom_obj in Boms.objects.filter(pro_no=pro_no, m_system=bom_map[m_system]):
        if not bom_obj.inventory_code.startswith("000000000"):
            inventory_code_list.append(bom_obj.inventory_code)
    all_row = 0
    
    for i, row in enumerate(sh_bom.values):
        if row[1] in inventory_code_list:
            b_obj = Boms.objects.filter(pro_no=pro_no, m_system=bom_map[m_system], inventory_code=row[1]).first()
            sh_bom[f"AJ{i+1}"] = b_obj.ba
            for key, val in b_obj.bb.items():
                sh_bom[f"{dict_head_bb[key]}{i+1}"] = val
            for key, val in b_obj.bc.items():
                sh_bom[f"{dict_head_bc[key]}{i+1}"] = val
            for key, val in b_obj.bd.items():
                sh_bom[f"{dict_head_bd[key]}{i+1}"] = val
            for key, val in b_obj.be_arrive.items():
                sh_bom[f"{dict_head_be[key]}{i+1}"] = val
        if row[0] == 'END':
            all_row = i + 2
        
    for i, b in enumerate(Boms.objects.filter(pro_no=pro_no, m_system=bom_map[m_system], inventory_code__startswith="000000000")):
        sh_bom[f'B{all_row+i}'] = '000000000'
        product_obj = Product.objects.filter(product_code=b.product_code).first()
        sh_bom[f'D{all_row+i}'] = product_obj.unit
        sh_bom[f'E{all_row+i}'] = product_obj.product_name
        sh_bom[f'G{all_row+i}'] = product_obj.product_type
        sh_bom[f'H{all_row+i}'] = product_obj.supply
        sh_bom[f"AJ{i+all_row}"] = b.ba
        for key, val in b.bb.items():
            sh_bom[f"{dict_head_bb[key]}{i+all_row}"] = val
        for key, val in b.bc.items():
            sh_bom[f"{dict_head_bc[key]}{i+all_row}"] = val
        for key, val in b.bd.items():
            sh_bom[f"{dict_head_bd[key]}{i+all_row}"] = val
        for key, val in b.be_arrive.items():
            sh_bom[f"{dict_head_be[key]}{i+all_row}"] = val


def add_inventory_code(req):
    for bom_obj in Boms.objects.all():
        inventory_code = Product.objects.filter(product_code=bom_obj.product_code).first().inventory_code
        bom_obj.inventory_code=inventory_code
        bom_obj.save()
    return JsonResponse({
        "code": 0,
        "msg": "修改成功"
    })


def load_btable(req):
    pro_no = req.GET.get("pro_no")
    pro_obj = Projection.objects.filter(pro_no=pro_no).first()
    con_year = pro_obj.con_year
    con_depart = pro_obj.con_depart
    msg = "导入成功"
    if not con_year or not con_depart:
        msg = "找不到，请补全B表位置"
        return JsonResponse({
            'code': 0,
            "msg": msg
        })
    try:
        file_path = find_pro_path(pro_no, con_year, con_depart)
        load_B(file_path, pro_obj)
    except Exception as e:
        msg = str(e)
    return JsonResponse({
        "code": 0,
        "msg": msg
    })
