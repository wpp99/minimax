import re, os
import json
from copy import deepcopy
import pandas as pd
import aiofiles, asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

from B.models import  B1nz, Boms, BsjXQDD, Projection
from Home.models import Product, Guan
from B.views.common import choice_map, bom_name, bom_map, Del_Load_1nz, Del_load_bom, Del_load_sjxqd


data = []
need_fields = []
file_paths = []
base_path = '\\\\192.168.1.88\\contract'



@xframe_options_exempt
def upload(req):    
    sheet_map = deepcopy(bom_map)
    sheet_map["1nz"] = 21
    sheet_map["sjXQD"] = 22
    sheet_map["product"] = 23
    sheet_map["projection"] = 24
    sheet_map["guan"] = 25
    return render(req, 'upload.html', {"sheet_name": sheet_map})


# 处理上传事件
@csrf_exempt
def upload_del(req, sheet_name=None):
    status = 0
    msg = "上传成功"
    file_obj = req.FILES.get('file')
    
    try:
        if sheet_name == '1nz':
            del_1nz(file_obj)
        elif sheet_name == 'sjXQD':
            del_sjxqd(file_obj)
        elif sheet_name in bom_name:
            del_bom(file_obj, sheet_name)
        elif sheet_name == "product":
            del_product(file_obj)
        elif sheet_name == "projection":
            del_projection(file_obj)
        elif sheet_name == "guan":
            del_guan(file_obj)
        else:
            status = 1
            msg = f"上传失败：无{sheet_name}"
    except Exception as e:
        msg = str(e)
    content = {
        'status': status,
        'msg': msg,
        # 'data': data
    }
    return JsonResponse(content)

# 获取数据
def get_upload_data(req):
    global need_fields
    if data:
        need_fields = list(data[0].keys())
        need_fields.pop(0)
    content = {
        'code': 0,
        'data': data
        # 'msg': '获取成功',
    }
    return JsonResponse(content)

# 导入数据库
@csrf_exempt
def load_data(req, mode):
    datalist = []
    datas = req.POST
    msg = '导入失败'
    pro_no = Projection.objects.filter(pro_no=datas['pro_no']).first()
    num = int(datas['length'])
   
    try:
        if mode == '1nz':
            load_1nz(datalist, datas, num, pro_no)
        elif mode == 'sjXQD':
            load_sjXQD(datalist, datas, num, pro_no)
        elif mode in bom_name:
            load_bom(datalist, datas, num, pro_no, mode)
        elif mode == 'product':
            load_product(datalist, datas, num)
        elif mode == "projection":
            print(1)
            load_projection(datalist, datas, num)
        elif mode == "guan":
            load_guan(datalist, datas, num)
        msg = '导入成功'


    except Exception as e:
        print(e)
    
    content = {
        'msg': msg,
        'status': 0,
    }
    return JsonResponse(content)




# 将数字为空的置为0
def del_null(d):
    if d:
        return d
    return 0


# 格式化时间
def del_date(date_data):
    r1 = re.findall("(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4})", str(date_data))
    if r1:
        return r1[0][2] + "-" + r1[0][0] + "-" + r1[0][1]

    res = re.findall("(\d{4}-\d{2}-\d{2})", str(date_data))
    if res:
        return res[0]
    return None


def b1nz_three(d):
    if str(d) == 'N/A':
        return "取消"
    return d

def del_1nz_mxbody(d):
    try:
        return d["MX采购主体"]
    except:
        return d["MX合同主体"]

def del_1nz_batch(d):
    try:
        return d["批次号\nShipment No."]
    except Exception as e:
        return d["发运批次\nShipment No."]

def del_none_field(row_obj, d, columns):
    if d in columns:
        return row_obj[d]
    return None




# 上传1nz
def del_1nz(data_obj):
    global data
    # data.clear()
    print("=====================1")
    b1nz_obj = Del_Load_1nz(data_obj)
    print("==================================2")
    data = b1nz_obj.del_1nz()
    print("==================================2")

    
    # excel_data = pd.read_excel(data_obj, sheet_name='1nz', header=7)
    # # df = excel_data[excel_data["批次号\nShipment No."].str.contains('DY\d{3}$', na=False)]
    # df = excel_data[excel_data["三部会审状态"].notna()]
    # df = df.fillna('')
    # columns = df.columns
    # for index, row in df.iterrows():
        # data.append({
        #     "id": index, 
        #     "batch_no": del_1nz_batch(row),   
        #     "description": row["货物描述(中英文)\nDecription"],    
        #     "area": row["区域\nArea"],  
        #     "design_date": del_date(row["设计输入资料提供时间\nDesign Input"]),      
        #     "deliver_date": del_date(row["计划交货 日期\nEx-work Date"]),      
        #     "itp_date": row["ITP放行日期\nITP Approval Date"],       
        #     "port": row["起运港\nLoading Port"],   
        #     "trans_method": row["运输方式\nTransportation Term"],   
        #     "grossWeight": del_null(row["毛重(吨)\nGW. (T)"]),  
        #     "volume": del_null(row["体积(立方米)\nCBM"]),  
        #     "ship_no": row["船名船次\nFlight/Vesssel No."],    
        #     "wayBill_no": row["运单号\nAWB/BL No."],   
        #     "arrive_date": del_date(row["预计到港时间\nETA"]),      
        #     "con_date": del_date(row["合同签定\n发运日期\nContract DS"]),     
        #     "nz_date": del_date(row["初版1nz预测\n发运日期"]),       
        #     "true_date": del_date(row["实际发货日期\nEx-wrok Date"]),      
        #     "mx_body": del_1nz_mxbody(row),      
        #     "trans_des": row["放行说明"],    
        #     "pack_des": del_none_field(row, "单独包装特殊说明", columns),      
        #     "three_status": b1nz_three(row["三部会审状态"]),      
        #     "directShipment": row["直运至"],   
        #     "trans_to": row["发运地"], 
        # })

# 合并sjXQD中的时间序列
def del_date_seria(date_datas):
    date_datas[date_datas.isnull()] = ''
    strings = ""
    for date_ in date_datas:
        if date_:
            strings += str(del_date(date_))
            strings += ";"
    return strings

# 处理sjxQD中的序号
def del_sjxqd_num(sj_num):
    if str(sj_num) == "nan":
        return ''
    return sj_num


# 上传sjXQD
def del_sjxqd(data_obj):
    global data
    data.clear()
    excel_data = pd.read_excel(data_obj, sheet_name='sjXQD', header=6, index_col="序号")
    obj_data = excel_data.loc[1:8, :]
    # print(obj_data.index)
    j = 1
    new_index = []
    for i, number in enumerate(obj_data.index):
        
        if str(obj_data.index[i-1]) != 'nan':
            pre = obj_data.index[i-1]
            j = 1
        if str(number) == 'nan':
            new_num = str(pre) + f'.{j}'
            new_index.append(new_num)
            j += 1
        else:
            new_index.append(str(number))

    obj_data.set_axis(new_index, axis=0, inplace=True)
    obj_data = obj_data.fillna('')
    for index, row in obj_data.iterrows():
        data.append({
            'id': del_sjxqd_num(index),
            "sys_code": row["\n系统代码"],
            "zgxy": row["ZGXY"],
            "content_zgxy": row["sjXQD 内容"],
            "start_date": del_date(row["起始日期"]),
            "close_date": del_date(row["关闭/最迟日期"]),
            "res_per": row["责任人"],
            "audit_level": row["审核\n级别"],
            "status":row["状态"],
            "date_seria": del_date_seria(row["日期1": "日期10"]),
            "sjxqd_remark": row["sjXQD要点及备注\nRemark"],
            "xqd0":row["XQD0"],
            "xqd1":row["XQD1"],
            "xqd2":row["XQD2"],
            "xqd_remind":row["XQD1,2备注"],
        })
    


# 合并bom中的多列
def del_str(datas, names):
    data_dict = {}
    for d, n in zip(datas, names):
        if d:
            data_dict[n] = int(d)
    return json.dumps(data_dict)

# 上传bom
def del_bom(data_obj, sheet_name):
    global data
    data.clear()
    data_head5 = pd.read_excel(data_obj, sheet_name=sheet_name, header=5)
    bb_names = data_head5.loc[0, "C301": "C396"]
    bc_names = data_head5.loc[0, "C401": "C497"]
    bd_names = data_head5.loc[0, "C601": "C697"]
    be_names = data_head5.loc[0, "C701": "C790"]
    excel_data = pd.read_excel(data_obj, sheet_name=sheet_name, header=[5, 7])
    obj_data = excel_data[excel_data["C103"]["Qty.\n数量"].map(str).str.contains("[1-9]+")]
    # obj_data.to_excel('./s1.xlsx')
    obj_data = obj_data.fillna('')
    # obj_data.to_excel("./static/t1.xlsx")
    for index, row in obj_data.iterrows():
        data.append({
            "id": index,
            "material_no": row["C102"]["MX Art. No."],
            "unit": row["C104"]["Unit\n单位"],
            "material_name": row["C105"]["Goods Description(external)\n货物描述（对外）"],
            "material_type": row["C107"]["Specification(internal)\n规格（对内）"],
            "m_system": sheet_name,
            "supply": row["C108"]["Supplier\n供应商"],
            "ba": row["C201"]["起点Ba"],
            "bb": del_str(row["C301": "C396"], bb_names),
            "bb_sum": int(row["C301": "C396"].map(lambda x: x if x else 0).sum()),
            "bb_con": row["C397"][0],
            "bb_res": row["C398"][0],
            "bc": del_str(row["C401": "C497"], bc_names),
            "bc_sum": int(row["C401": "C497"].map(lambda x: x if x else 0).sum()),
            "bd": del_str(row["C601": "C697"], bd_names),
            "bd_sum": int(row["C601": "C697"].map(lambda x: x if x else 0).sum()),
            "be_arrive": del_str(row["C701": "C790"], be_names),
            "be_sum": int(row["C701": "C790"].map(lambda x: x if x else 0).sum()),
            "bs": row["C792"]["现场采购Bs"],
            "bd2": row["C793"]["现场补发货Bd2"],
            "be_install": row["C794"]["安装量Be"],
            "be_loss": row["C795"]["损耗"],
            "be_res": row["C796"]["剩余总量"],
            "be_bb": row["C798"]["安装与设计对比"],
        })
    


# 上传产品
def del_product(data_obj):
    global data
    data.clear()
    excel_data = pd.ExcelFile(data_obj)
    
    # data_contain = pd.DataFrame()
    j = 8
    for sheet in excel_data.sheet_names:
        if sheet in bom_name:
            data_contain = pd.read_excel(data_obj, sheet_name=sheet, header=7)
            # data_contain = pd.concat([data_contain, d])
            data_contain = data_contain[data_contain["MX Art. No."].map(str).str.contains('\d{5,15}')]
            data_contain = data_contain.fillna('')
            for index, row in data_contain.iterrows():
                product_code = 'p' + str(j).rjust(9, '0')
                data.append({
                    "id": index,
                    "product_code" : product_code,
                    "material_no": str(row["MX Art. No."]),
                    "unit": row["Unit\n单位"],
                    "material_name": row["Goods Description(external)\n货物描述（对外）"],
                    # "des_inner": row["Goods Description (internal)\n货物描述（对内）"],
                    "material_type": row["Specification(internal)\n规格（对内）"],
                    "supply": row["Supplier\n供应商"],
                    "m_system": sheet,
                })
                j = j + 1
    


def del_nan(nan_datas):
    if str(nan_datas) == "nan":
        return None
    return nan_datas

# 上传项目
def del_projection(data_obj):
    global data
    data.clear()
    excel_data = pd.read_excel(data_obj, sheet_name="HT1#", header=7)
    df = excel_data[excel_data["合同号"].str.contains("^\d")]
    df.fillna('', inplace=True)
    for index, row in df.iterrows():
        data.append({
            "id": index,
            "con_year": row["合同年份"],
            "con_depart": row["合同文件夹部门"],
            "pro_no": row["合同号"],
            "pro_name": del_nan(row["项目名称"]),
            "depart_no": del_nan(row["部门"]),
            "pm": del_nan(row["项目PM "]),
            "pro_mer": del_nan(row["商务"]),
            "con_type": del_nan(row["项目类型"]),
            "pro_label": del_nan(row["合同标签"]),
            "pro_date": del_date(row["LX日期"]),
            "logit_status": row["物流是否关闭"],
            "pro_status": row["项目状态"],
        })
    

def del_number(datas):
    if datas:
        res = re.findall("^\d{1,6}\.?\d{1,3}$", str(datas))
        if res:
            return res[0]
    return 0


def del_guan(data_obj):
    global data
    data.clear()
    excel_data = pd.read_excel(data_obj, sheet_name="0A", header=3)
    df = excel_data[excel_data["SRD号"].notna()]
    df.fillna('', inplace=True)
    for index, row in df.iterrows():
        data_data = dict(
            no = index,
            manage_code = row[0],
            pro_no = row[2], 
            batch = row[3],
            product_num = del_number(row[4]),
            prod_task_content = row[5],
            product_code = row[6],
            order_date = del_date(row[7]),
            acc_date = del_date(row[8]),
            sj_date = del_date(row[9]),
            expect_date = del_date(row[10]),
            table0_update_date = del_date(row[11]),
            first_sign_date =del_date( row[12]),
            change_date = del_date(row[13]),
            responsible = row[14],
            inventory_code = row[16],
            status = row[17],
            warehousing_date = del_date(row[18]),
            warehousing_num = del_number(row[19]),
            warehousing_code =  str(row[20]).replace(".0", ''),
            change_record = str(row[21]),
            attribute = row[22],
            description = str(row[23]),
            jin1 = del_number(row[24]),
            warehousing_status = str(row[25]),
            assembly_method = row[26],
            last_deliver_date = del_date(row[27]),
            file_place = row[28],
            to_warehouse = del_number(row[29]),
            change_times = del_number(row[32]),
            need_1nz = row[33],
            under_construction = del_number(row[34]),
            success_num = del_number(row[35]),
            on_delivery_rate =  del_number(str(row[36]).replace("-", "")),
            yield_rate = del_number(row[37]),
            manage_order_no = str(row[38]),
            sales_order = row[40],
            assembly_cycle = del_number(row[41]),
            man_assembly_time =  del_number(row[42]),
            el_assembly_time =  del_number(row[43]),
            quality_check_time = del_number(row[44]),
            op_overlap_rate = del_number(row[45]),
            process_code = row[46],
            srd_num = del_number(row[47]),
            inventory_num = del_number(row[48]),
            warehouse_out_num = del_number(str(row[49]).replace(".0", "")),
        )
        data.append(data_data)
    


# 获取B表存储位置
def find_pro_path(pro_no, year, depart_place):
    sub_path = ''
    if int(year) < 2017:
        return
    # 2017 , 2018
    depart_path = os.path.join(base_path, f"Data{year}\\{depart_place}")
    for f in os.listdir(depart_path):
        new_pro_no = pro_no[-3:] + '_' + pro_no[:-3]
        if f.startswith(new_pro_no):
            sub_path = os.path.join(depart_path, f"{f}\\04_MaterialOrdering\\ML_all{pro_no}.xlsx")
            if os.path.exists(sub_path):
                return os.path.join(base_path, sub_path)
    return 



def merge_bom(file_name, sheet, pro_no):
    df = pd.read_excel(file_name, sheet_name=sheet, header=5)
    # df = df[df["C103"].map(str).str.contains("[1-9]+")]
    df = df.drop(1)
    df['system'] = sheet
    df['pro_no'] = pro_no
    return df



def del_json(columns, data):
    dict_data = {}
    for col, d in zip(columns, data):
        if d:
            dict_data[col] = d
    return dict_data


def judge_num(data):
    for d in data:
        if str(d).isdigit():
            return True
    return False

# def load_B(file_path, pro_no, all_data):
def load_B(file_path, pro_no):
    excel_data = pd.ExcelFile(file_path)
    for sheet in excel_data.sheet_names:
        try:
            if sheet == "1nz":
                b1nz_obj = Del_Load_1nz(file_path)
                b1nz_obj.del_1nz()
                b1nz_obj.load_1nz(pro_no)
                
            if sheet == "sjXQD":
                bsjxqd_obj = Del_load_sjxqd(file_path)
                bsjxqd_obj.del_sjxqd()
                bsjxqd_obj.load_sjxqd(pro_no)

            if sheet in bom_name:
                bom_obj = Del_load_bom(file_path)
                bom_obj.del_bom(pro_no, sheet)
                bom_obj.load_bom(pro_no)
        except Exception as e:
            continue

def make_product_code(inventory_code, unit, product_name, product_type, supply, m_system):
        print(f"==================a1====================")
        if not str(inventory_code).startswith("0"):
            pro_obj = Product.objects.filter(inventory_code=inventory_code).first()
            if pro_obj:
                return pro_obj.product_code
        
        last_id = Product.objects.all().order_by("-id").first().id
        new_pro_code = "p" + str(last_id+1).rjust(12, '0')
        Product.objects.create(product_code=new_pro_code, inventory_code=inventory_code, 
            product_name=product_name, product_type=product_type, unit=unit, supply=supply, pro_system=m_system)
        print(f"===================a2===================")
        return new_pro_code

def del_data(all_data):
    all_data = all_data[all_data["C103"] !=0]
    all_data = all_data[all_data["C103"].notna()]
    all_data.fillna('', inplace=True)
    # all_data.to_excel("./static/test3.xlsx")
    columns_text_bb = []
    columns_text_bc = []
    columns_text_bd = []
    columns_text_be = []
    datalist = []
    for index, row in all_data.iterrows():
        # if judge_num(row["C301":"C399"]):
        if row["C103"] == "公式":
            columns_text_bb = row["C301":"C399"]
            columns_text_bc = row["C401":"C499"]
            columns_text_bd = row["C601":"C699"]
            columns_text_be = row["C701":"C790"]
            continue
        
        m_system = choice_map[row["system"]]
        pro_obj = Projection.objects.filter(pro_no=row["pro_no"]).first()
        product_code = make_product_code(row["C102"], row["C104"], str(row["C105"])[:250], str(row["C107"])[:250], row["C108"], m_system)
        data = {
            "pro_no": pro_obj,
            "product_code": product_code,
            # "unit": row["C104"],
            # "product_name": str(row["C105"])[:250],
            # "product_type": str(row["C107"])[:250],
            "m_system": m_system,
            # "supply": row["C108"],
            "ba": row["C201"],
            "bb": del_json(columns_text_bb, row["C301":"C399"]),
            "bc": del_json(columns_text_bc, row["C401":"C499"]),
            "bd": del_json(columns_text_bd, row["C601":"C699"]),
            "be_arrive": del_json(columns_text_be, row["C701":"C790"]),
            "bs": del_null(row["C792"]),
            "bd2": del_null(row["C793"]),
            "be_install": del_null(row["C794"]),
            # "be_loss": del_null(row["C795"]),
            # "be_res": del_null(row["C796"]),
           
        }
        bom = Boms(**data)
        datalist.append(bom)
    Boms.objects.bulk_create(datalist)
    



def load_1nz(datalist, datas, num, pro_no):
    datalist.clear()
    for i in range(num):
        index = f"data[{i}]"
        b1nz = B1nz(
            pro_no=pro_no, 
            batch_no=datas[index+'[batch_no]'],
            description=datas[index+'[description]'],
            area=datas[index+'[area]'],
            design_date=del_date(datas[index+'[design_date]']),
            deliver_date=del_date(datas[index+'[deliver_date]']),
            itp_date=datas[index+'[itp_date]'],
            port=datas[index+'[port]'],
            trans_method=choice_map[datas[index+'[trans_method]']],
            grossWeight=del_null(datas[index+'[grossWeight]']),
            volume=del_null(datas[index+'[volume]']),
            ship_no=datas[index+'[ship_no]'],
            wayBill_no=datas[index+'[wayBill_no]'],
            arrive_date=del_date(datas[index+'[arrive_date]']),
            con_date=del_date(datas[index+'[con_date]']),
            nz_date=del_date(datas[index+'[nz_date]']),
            true_date=del_date(datas[index+'[true_date]']),
            mx_body=datas[index+'[mx_body]'],
            trans_des=choice_map[datas[index+'[trans_des]']],
            pack_des=datas[index+'[pack_des]'],
            three_status=choice_map[datas[index+'[three_status]']],
            directShipment=choice_map[datas[index+'[directShipment]']],
            trans_to=datas[index+'[trans_to]']
        )
        datalist.append(b1nz)
    B1nz.objects.bulk_update_or_create(datalist, need_fields, match_field=['pro_no', 'batch_no'])


def load_sjXQD(datalist, datas, num, pro_no):
    datalist.clear()
    for i in range(num):
        index = f"data[{i}]"
        bsjxqd = BsjXQDD(
            pro_no=pro_no,
            num=datas[index+'[id]'],
            sys_code=datas[index+'[sys_code]'],
            zgxy=datas[index+'[zgxy]'],
            content_zgxy=datas[index+'[content_zgxy]'],
            start_date=del_date(datas[index+'[start_date]']),
            close_date=del_date(datas[index+'[close_date]']),
            res_per=datas[index+'[res_per]'],
            audit_level=datas[index+'[audit_level]'],
            status=datas[index+'[status]'],
            date_seria=datas[index+'[date_seria]'],
            xqd0=datas[index+'[xqd0]'],
            xqd1=datas[index+'[xqd1]'],
            xqd2=datas[index+'[xqd2]'],
            xqd_remind=datas[index+'[xqd_remind]']
        )
        datalist.append(bsjxqd)
    BsjXQDD.objects.bulk_update_or_create(datalist, need_fields, match_field=['pro_no', 'num'])


def load_bom(datalist, datas, num, pro_no, mode):
    datalist.clear()      
    for i in range(num):
        index = f"data[{i}]"
        inventory_code = datas[index+'[material_no]']
        product_obj = Product.objects.filter(inventory_code=inventory_code).first()
        if not product_obj:
            msg = f"不存在的存货编码{inventory_code}"
            return JsonResponse({
                'status': 1,
                'msg': msg
            })
        product_code = product_obj.product_code
        bom = Boms(
            pro_no=pro_no,
            product_code=product_code,
            m_system=choice_map[mode],
            ba=del_null(datas[index+'[ba]']),
            bb=json.loads(datas[index+'[bb]']),
            bb_con=del_null(datas[index+'[bb_con]']),
            bb_res=del_null(datas[index+'[bb_res]']),
            bc=json.loads(datas[index+'[bc]']),
            bd=json.loads(datas[index+'[bd]']),
            be_arrive=json.loads(datas[index+'[be_arrive]']),
            bs=del_null(datas[index+'[bs]']),
            bd2=del_null(datas[index+'[bd2]']),
            be_install=del_null(datas[index+'[be_install]']),
            be_res=del_null(datas[index+'[be_res]'])
        )
        datalist.append(bom)
    Boms.objects.bulk_update_or_create(datalist, need_fields, match_field=['pro_no', 'product_code', 'm_system'])


def load_product(datalist, datas, num):
    datalist.clear()
    for i in range(num):
        index = f"data[{i}]"
        product = Product(
            product_code=datas[index+'[product_code]'],
            inventory_code=datas[index+'[material_no]'],
            product_name=datas[index+'[material_name]'],
            unit=datas[index+'[unit]'],
            product_type=datas[index+'[material_type]'],
            pro_system=choice_map[datas[index+'[m_system]']],
            supply=datas[index+'[supply]'],
        )
        datalist.append(product)
    Product.objects.bulk_update_or_create(datalist, need_fields, match_field='product_code')


def load_projection(datalist, datas, num):
    datalist.clear()
    for i in range(num):
        index = f"data[{i}]"
        data_dict = dict(
            con_year=datas[index+'[con_year]'],
            con_depart=datas[index+'[con_depart]'],
            pro_no=datas[index+'[pro_no]'],
            pro_name=datas[index+'[pro_name]'],
            pm=datas[index+'[pm]'],
            pro_mer=datas[index+'[pro_mer]'],
            con_type=datas[index+'[con_type]'],
            pro_label=datas[index+'[pro_label]'],
            pro_date=del_date(datas[index+'[pro_date]']),
            logit_status=datas[index+'[logit_status]'],
            pro_status=datas[index+'[pro_status]'],
            depart_no=datas[index+'[depart_no]']
        )
        projection = Projection(**data_dict)
        datalist.append(projection)
    Projection.objects.bulk_update_or_create(datalist,  need_fields, match_field='pro_no')
    
    print("===========================1")
    
    Product.objects.filter(Q(inventory_code__startswith="000000000") | Q(inventory_code__isnull=True)).delete()
    all_data = pd.DataFrame()
    for dataobj in Projection.objects.all():
        # if dataobj.logit_status == "否":
        # if dataobj.pro_no in pro_extra_no:
            file_path = find_pro_path(dataobj.pro_no, dataobj.con_year, dataobj.con_depart)
            try:
                if file_path:
                    # all_data = load_B(file_path, dataobj, all_data)
                    load_B(file_path, dataobj)
            except Exception as e:
                with open("./static/err.txt", 'a', encoding='utf-8') as f:
                    f.write(f"{dataobj.pro_no} load error ==============={e}\n")
                continue
    # del_data(all_data)
   
    
def load_guan(datalist, datas, num):
    datalist.clear()
    for i in range(num):
        index = f"data[{i}]"
        data_data = dict(
            manage_code = datas[index+'[manage_code]'],
            pro_no = datas[index+'[pro_no]'], 
            batch = datas[index+'[batch]'],
            product_num = datas[index+'[product_num]'],
            prod_task_content = datas[index+'[prod_task_content]'],
            product_code = datas[index+'[product_code]'],
            order_date = del_date(datas[index+'[order_date]']),
            acc_date = del_date(datas[index+'[acc_date]']),
            sj_date = del_date(datas[index+'[sj_date]']),
            expect_date = del_date(datas[index+'[expect_date]']),
            table0_update_date = del_date(datas[index+'[table0_update_date]']),
            first_sign_date = del_date(datas[index+'[first_sign_date]']),
            change_date = del_date(datas[index+'[change_date]']),
            responsible = datas[index+'[responsible]'],
            inventory_code = datas[index+'[inventory_code]'],
            status = datas[index+'[status]'],
            warehousing_date = del_date(datas[index+'[warehousing_date]']),
            warehousing_num = datas[index+'[warehousing_num]'],
            warehousing_code =  datas[index+'[warehousing_code]'],
            change_record = datas[index+'[change_record]'],
            attribute = datas[index+'[attribute]'],
            description = datas[index+'[description]'],
            jin1 = datas[index+'[jin1]'],
            warehousing_status = datas[index+'[warehousing_status]'],
            assembly_method = datas[index+'[assembly_method]'],
            last_deliver_date = del_date(datas[index+'[last_deliver_date]']),
            file_place = datas[index+'[file_place]'],
            to_warehouse = datas[index+'[to_warehouse]'],
            need_1nz = datas[index+'[need_1nz]'],
            change_times = datas[index+'[change_times]'],
            under_construction = datas[index+'[under_construction]'],
            success_num = datas[index+'[success_num]'],
            on_delivery_rate =  datas[index+'[on_delivery_rate]'],
            yield_rate = datas[index+'[yield_rate]'],
            manage_order_no = datas[index+'[manage_order_no]'],
            sales_order = datas[index+'[sales_order]'],
            man_assembly_time = datas[index+'[man_assembly_time]'],
            el_assembly_time =  datas[index+'[el_assembly_time]'],
            quality_check_time = datas[index+'[quality_check_time]'],
            op_overlap_rate = datas[index+'[op_overlap_rate]'],
            process_code = datas[index+'[process_code]'],
            srd_num = datas[index+'[srd_num]'],
            inventory_num = datas[index+'[inventory_num]'],
            warehouse_out_num =datas[index+'[warehouse_out_num]']
        )
        g = Guan(**data_data)
        datalist.append(g)
    Guan.objects.bulk_update_or_create(datalist, need_fields, match_field='manage_code')
