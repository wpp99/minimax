import re, os
import json
from copy import deepcopy
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

from B.models import  B1nz, Boms, BsjXQDD, Projection
from Home.models import Product, Guan, SaleOutInventory, Inventory, PurchaseOrder
from B.views.common import choice_map, bom_name, bom_map, Del_Load_1nz, Del_load_bom, Del_load_sjxqd


data = []
need_fields = []


@xframe_options_exempt
def upload(req):    
    sheet_map = deepcopy(bom_map)
    sheet_map["1nz"] = 21
    sheet_map["sjXQD"] = 22
    sheet_map["product"] = 23
    sheet_map["projection"] = 24
    sheet_map["guan"] = 25
    sheet_map["warehouse"] = 26
    sheet_map["purchase"] = 27
    sheet_map["sale_out"] = 28
    return render(req, 'upload.html', {"sheet_name": sheet_map})

@csrf_exempt
def upload_del(req, sheet_name=None):
    """处理上传事件"""
    global data
    status = 0
    msg = "上传成功"
    file_obj = req.FILES.get('file')
    file_name = str(file_obj)
    upload_obj = Del_load_upload(file_obj)
    try:
        if sheet_name == '1nz':
            b1nz_obj = Del_Load_1nz(file_obj)
            data = b1nz_obj.del_1nz(file_name)
        elif sheet_name == 'sjXQD':
            b1nz_obj = Del_load_sjxqd(file_obj)
            data = b1nz_obj.del_sjxqd(file_name)
        elif sheet_name in bom_name:
            b1nz_obj = Del_load_bom(file_obj)
            data = b1nz_obj.del_bom(sheet_name)
        elif sheet_name == "product":
            upload_obj.del_product()
        elif sheet_name == "projection":
            upload_obj.del_projection()
        elif sheet_name == "guan":
            upload_obj.del_guan()
        elif sheet_name == "warehouse":
            upload_obj.del_warehouse()
        elif sheet_name == "purchase":
            upload_obj.del_purchase()
        elif sheet_name == "sale_out":
            upload_obj.del_sale_out()
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

def get_upload_data(req):
    """获取数据"""
    page = int(req.GET.get("page"))
    limit = int(req.GET.get("limit"))
    start = (page - 1) * limit
    end = page * limit
    
    global need_fields
    if data:
        need_fields = list(data[0].keys())
        need_fields.pop(0)
    content = {
        'code': 0,
        'data': data[start:end],
        'count': len(data)
        # 'msg': '获取成功',
    }
    return JsonResponse(content)

@csrf_exempt
def load_data(req, mode):
    """导入数据库"""
    datalist = []
    datas = req.POST
    msg = '导入失败'
    pro_no = Projection.objects.filter(pro_no=datas['pro_no']).first()
    num = int(datas['length'])
   
    try:
        if mode == '1nz':
            Del_load_upload().load_1nz(datalist, datas, num, pro_no)
        elif mode == 'sjXQD':
            Del_load_upload().load_sjXQD(datalist, datas, num, pro_no)
        elif mode in bom_name:
            Del_load_upload().load_bom(datalist, datas, num, pro_no, mode)
        elif mode == 'product':
            Del_load_upload().load_product(datalist, datas, num)
        elif mode == "projection":
            Del_load_upload().load_projection(datalist, datas, num)
        elif mode == "guan":
            Del_load_upload().load_guan(datalist, datas, num)
        elif mode == "warehouse":
            Del_load_upload().load_warehouse(data)
        elif mode == "purchase":
            Del_load_upload().load_purchase(data)
        elif mode == "sale_out":
            Del_load_upload().load_sale_out(data)

        msg = '导入成功'


    except Exception as e:
        print(e)
    
    content = {
        'msg': msg,
        'status': 0,
    }
    return JsonResponse(content)

class Del_load_upload:
    def __init__(self, data_obj=None):
        self.base_path = '\\\\192.168.1.88\\contract'
        self.data = []
        self.need_fields = []
        self.data_obj = data_obj

    def del_null(self, d):
        """将数字为空的置为0"""
        if d:
            return d
        return 0
    
    def del_date(self, date_data):
        """格式化时间"""
        r1 = re.findall("(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4})", str(date_data))
        if r1:
            return r1[0][2] + "-" + r1[0][0] + "-" + r1[0][1]

        res = re.findall("(\d{4}-\d{2}-\d{2})", str(date_data))
        if res:
            return res[0]
        return None

    def del_product(self ):
        """上传产品"""
        global data
        data.clear()
        excel_data = pd.ExcelFile(self.data_obj)
        
        # data_contain = pd.DataFrame()
        j = 8
        for sheet in excel_data.sheet_names:
            if sheet in bom_name:
                data_contain = pd.read_excel(self.data_obj, sheet_name=sheet, header=7)
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
        
    def del_projection(self):
        """上传项目"""
        global data
        data.clear()
        excel_data = pd.read_excel(self.data_obj, sheet_name="HT1#", header=7)
        df = excel_data[excel_data["合同号"].str.contains("^\d")]
        df.fillna('', inplace=True)
        for index, row in df.iterrows():
            data.append({
                "id": index,
                "con_year": row["合同年份"],
                "con_depart": row["合同文件夹部门"],
                "pro_no": row["合同号"],
                "pro_name": row["项目名称"],
                "depart_no": row["部门"],
                "pm":row["项目PM "],
                "pro_mer": row["商务"],
                "con_type": row["项目类型"],
                "pro_label": row["合同标签"],
                "pro_date": self.del_date(row["LX日期"]),
                "logit_status": row["物流是否关闭"],
                "pro_status": row["项目状态"],
            })
        
    def del_number(self, datas):
        if datas:
            res = re.findall("^\d{1,6}\.?\d{1,3}$", str(datas))
            if res:
                return res[0]
        return 0

    def del_guan(self):
        global data
        data.clear()
        excel_data = pd.read_excel(self.data_obj, sheet_name="0A", header=3)
        df = excel_data[excel_data["SRD号"].notna()]
        df.fillna('', inplace=True)
        for index, row in df.iterrows():
            data_data = dict(
                no = index,
                manage_code = row[0],
                pro_no = row[2], 
                batch = row[3],
                product_num = self.del_number(row[4]),
                prod_task_content = row[5],
                product_code = row[6],
                order_date = self.del_date(row[7]),
                acc_date = self.del_date(row[8]),
                sj_date = self.del_date(row[9]),
                expect_date = self.del_date(row[10]),
                table0_update_date = self.del_date(row[11]),
                first_sign_date =self.del_date( row[12]),
                change_date = self.del_date(row[13]),
                responsible = row[14],
                inventory_code = row[16],
                status = row[17],
                warehousing_date = self.del_date(row[18]),
                warehousing_num = self.del_number(row[19]),
                warehousing_code =  str(row[20]).replace(".0", ''),
                change_record = str(row[21]),
                attribute = row[22],
                description = str(row[23]),
                jin1 = self.del_number(row[24]),
                warehousing_status = str(row[25]),
                assembly_method = row[26],
                last_deliver_date = self.del_date(row[27]),
                file_place = row[28],
                to_warehouse = self.del_number(row[29]),
                change_times = self.del_number(row[32]),
                need_1nz = row[33],
                under_construction = self.del_number(row[34]),
                success_num = self.del_number(row[35]),
                on_delivery_rate =  self.del_number(str(row[36]).replace("-", "")),
                yield_rate = self.del_number(row[37]),
                manage_order_no = str(row[38]),
                sales_order = row[40],
                assembly_cycle = self.del_number(row[41]),
                man_assembly_time =  self.del_number(row[42]),
                el_assembly_time =  self.del_number(row[43]),
                quality_check_time = self.del_number(row[44]),
                op_overlap_rate = self.del_number(row[45]),
                process_code = row[46],
                srd_num = self.del_number(row[47]),
                inventory_num = self.del_number(row[48]),
                warehouse_out_num = self.del_number(str(row[49]).replace(".0", "")),
            )
            data.append(data_data)

    def del_warehouse(self):
        global data
        data.clear()
        excel_file = pd.read_excel(self.data_obj, header=1)
        excel_file = excel_file[excel_file["存货编码"].notna()]
        excel_file["预计入库数量合计"].fillna(0, inplace=True)
        excel_file["待发货数量"].fillna(0, inplace=True)
        excel_file["可用数量"].fillna(0, inplace=True)
        excel_file["现存数量"].fillna(0, inplace=True)
        excel_file.fillna("", inplace=True)
        for index, row in excel_file.iterrows():
            product_code = Del_load_bom().make_product_code(row["存货编码"], row["主计量单位"], row["存货名称"], row["规格型号"], None, None)
            data.append({
                "product_code": product_code,
                "warehouse_code": row["仓库编码"],
                "warehouse_name": row["仓库名称"],
                "inventory_code": row["存货编码"],
                "inventory_name": row["存货名称"],
                "inven_now_num": row["现存数量"],
                "to_inventory_num": row["预计入库数量合计"],
                "inven_delivery_num": row["待发货数量"],
                "inven_class_code": row["存货分类代码"],
                "inven_class_name": row["存货分类名称"],
                "inven_con_code": row["存货合同号"],
                "need_flow_code": row["需求跟踪号"],
            })

    def del_purchase(self):
        global data
        data.clear()
        excel_file = pd.read_excel(self.data_obj)
        excel_file = excel_file[excel_file["业务类型"].notna()]
        excel_file["数量"].fillna(0, inplace=True)
        excel_file["累计入库数量"].fillna(0, inplace=True)
        excel_file["cum_towarehouse_num"].fillna(0, inplace=True)
        excel_file.fillna("", inplace=True)
        for index, row in excel_file.iterrows():
            product_code = Del_load_bom().make_product_code(row["存货编号"], row["主计量"], row["存货名称"], row["规格型号"], None, None)
            data.append({
                "product_code": product_code,
                "business_type": row["业务类型"],
                "purchase_type": row["采购类型"],
                "order_code": row["订单编号"],
                "inventory_code": row["存货编号"],
                "purchase_num": row["数量"],
                "upper_order_code": row["上游单据号"],
                "prepared_by": row["制单人"],
                "reviewed_by": row["审核人"],
                "order_date": row["日期"],
                "audit_date": row["审核时间"],
                "arrive_date": row["计划到货日期"],
                "remark": row["行备注"],
                "pro_batch": row["项目DY批次号"],
                "depart": row["部门"],
                "warehouse_status": row["入库状态"],
                "pro_des": row["项目描述"],
                "arrive_status": row["到货状态"],
                "drictship": row["直运至"],
                "cum_towarehouse_num": row["累计入库数量"],
            })

    def del_sale_out(self):
        global data
        data.clear()
        excel_file = pd.read_excel(self.data_obj)
        excel_file = excel_file[excel_file["仓库编码"].notna()]
        excel_file.fillna('', inplace=True)
        for index, row in excel_file.iterrows():
            product_code = Del_load_bom().make_product_code(row["存货编码"], row["主计量单位"], row["存货名称"], row["规格型号"], None, None)
            data.append({
                "product_code": product_code,
                "warehouse_code": row["仓库编码"],
                "warehouse_name": row["仓库"],
                "warehouse_out_code": row["出库单号"],
                "inventory_code": row["存货编码"],
                "out_num": row["数量"],
                "pro_batch": row["DY批次号"],
                "depart": row["销售部门"],
                "order_code": row["来源订单号"],
                "prepared_by": row["制单人"],
                "reviewed_by": row["审核人"],
                "out_date": row["出库日期"],
                "audit_date": row["审核时间"],
                "out_type": row["出库类别"],
            })

    def find_pro_path(self, pro_no, year, depart_place):
        """获取B表存储位置"""
        sub_path = ''
        if int(year) < 2017:
            return
        # 2017 , 2018
        depart_path = os.path.join(self.base_path, f"Data{year}\\{depart_place}")
        for f in os.listdir(depart_path):
            new_pro_no = pro_no[-3:] + '_' + pro_no[:-3]
            if f.startswith(new_pro_no):
                sub_path = os.path.join(depart_path, f"{f}\\04_MaterialOrdering\\ML_all{pro_no}.xlsx")
                if os.path.exists(sub_path):
                    return os.path.join(self.base_path, sub_path)
        return 

    def load_B(self, file_path, pro_no):
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
                    bom_obj.del_bom(sheet)
                    bom_obj.load_bom(pro_no)
            except Exception as e:
                continue

    def load_1nz(self, datalist, datas, num, pro_no):
        datalist.clear()
        for i in range(num):
            index = f"data[{i}]"
            b1nz = B1nz(
                pro_no=pro_no, 
                batch_no=datas[index+'[batch_no]'],
                description=datas[index+'[description]'],
                area=datas[index+'[area]'],
                design_date=self.del_date(datas[index+'[design_date]']),
                deliver_date=self.del_date(datas[index+'[deliver_date]']),
                itp_date=datas[index+'[itp_date]'],
                port=datas[index+'[port]'],
                trans_method=choice_map[datas[index+'[trans_method]']],
                grossWeight=self.del_null(datas[index+'[grossWeight]']),
                volume=self.del_null(datas[index+'[volume]']),
                ship_no=datas[index+'[ship_no]'],
                wayBill_no=datas[index+'[wayBill_no]'],
                arrive_date=self.del_date(datas[index+'[arrive_date]']),
                con_date=self.del_date(datas[index+'[con_date]']),
                nz_date=self.del_date(datas[index+'[nz_date]']),
                true_date=self.del_date(datas[index+'[true_date]']),
                mx_body=datas[index+'[mx_body]'],
                trans_des=choice_map[datas[index+'[trans_des]']],
                pack_des=datas[index+'[pack_des]'],
                three_status=choice_map[datas[index+'[three_status]']],
                directShipment=choice_map[datas[index+'[directShipment]']],
                trans_to=datas[index+'[trans_to]']
            )
            datalist.append(b1nz)
        B1nz.objects.bulk_update_or_create(datalist, need_fields, match_field=['pro_no', 'batch_no'])

    def load_sjXQD(self, datalist, datas, num, pro_no):
        datalist.clear()
        for i in range(num):
            index = f"data[{i}]"
            bsjxqd = BsjXQDD(
                pro_no=pro_no,
                num=datas[index+'[id]'],
                sys_code=datas[index+'[sys_code]'],
                zgxy=datas[index+'[zgxy]'],
                content_zgxy=datas[index+'[content_zgxy]'],
                start_date=self.del_date(datas[index+'[start_date]']),
                close_date=self.del_date(datas[index+'[close_date]']),
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

    def load_bom(self, datalist, datas, num, pro_no, mode):
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
                ba=self.del_null(datas[index+'[ba]']),
                bb=json.loads(datas[index+'[bb]']),
                bb_con=self.del_null(datas[index+'[bb_con]']),
                bb_res=self.del_null(datas[index+'[bb_res]']),
                bc=json.loads(datas[index+'[bc]']),
                bd=json.loads(datas[index+'[bd]']),
                be_arrive=json.loads(datas[index+'[be_arrive]']),
                bs=self.del_null(datas[index+'[bs]']),
                bd2=self.del_null(datas[index+'[bd2]']),
                be_install=self.del_null(datas[index+'[be_install]']),
                be_res=self.del_null(datas[index+'[be_res]'])
            )
            datalist.append(bom)
        Boms.objects.bulk_update_or_create(datalist, need_fields, match_field=['pro_no', 'product_code', 'm_system'])

    def load_product(self, datalist, datas, num):
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

    def load_projection(self, datalist, datas, num):
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
                pro_date=self.del_date(datas[index+'[pro_date]']),
                logit_status=datas[index+'[logit_status]'],
                pro_status=datas[index+'[pro_status]'],
                depart_no=datas[index+'[depart_no]']
            )
            projection = Projection(**data_dict)
            datalist.append(projection)
        Projection.objects.bulk_update_or_create(datalist,  need_fields, match_field='pro_no')
        
        
        Product.objects.filter(Q(inventory_code__startswith="000000000") | Q(inventory_code__isnull=True)).delete()
        for dataobj in Projection.objects.all():
            if dataobj.logit_status == "否":
                file_path = self.find_pro_path(dataobj.pro_no, dataobj.con_year, dataobj.con_depart)
                try:
                    if file_path:
                        self.load_B(file_path, dataobj)
                except Exception as e:
                    with open("./static/err.txt", 'a', encoding='utf-8') as f:
                        f.write(f"{dataobj.pro_no} load error ==============={e}\n")
                    continue
        
    def load_guan(self, datalist, datas, num):
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
                order_date = self.del_date(datas[index+'[order_date]']),
                acc_date = self.del_date(datas[index+'[acc_date]']),
                sj_date = self.del_date(datas[index+'[sj_date]']),
                expect_date = self.del_date(datas[index+'[expect_date]']),
                table0_update_date = self.del_date(datas[index+'[table0_update_date]']),
                first_sign_date = self.del_date(datas[index+'[first_sign_date]']),
                change_date = self.del_date(datas[index+'[change_date]']),
                responsible = datas[index+'[responsible]'],
                inventory_code = datas[index+'[inventory_code]'],
                status = datas[index+'[status]'],
                warehousing_date = self.del_date(datas[index+'[warehousing_date]']),
                warehousing_num = datas[index+'[warehousing_num]'],
                warehousing_code =  datas[index+'[warehousing_code]'],
                change_record = datas[index+'[change_record]'],
                attribute = datas[index+'[attribute]'],
                description = datas[index+'[description]'],
                jin1 = datas[index+'[jin1]'],
                warehousing_status = datas[index+'[warehousing_status]'],
                assembly_method = datas[index+'[assembly_method]'],
                last_deliver_date = self.del_date(datas[index+'[last_deliver_date]']),
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

    def load_warehouse(self, dd):
        Inventory.objects.all().delete()
        obj_list = []
        print(len(dd))
        for data_item in dd:
            print("i")
            i_obj = Inventory(**data_item)
            obj_list.append(i_obj)
        Inventory.objects.bulk_create(obj_list)

    def load_purchase(self, data):
        obj_list = []
        for data_item in data:
            i_obj = PurchaseOrder(**data_item)
        obj_list.append(i_obj)
        PurchaseOrder.objects.bulk_create(obj_list)

    def load_sale_out(self, data):
        obj_list = []
        for data_item in data:
            i_obj = SaleOutInventory(**data_item)
        obj_list.append(i_obj)
        SaleOutInventory.objects.bulk_create(obj_list)