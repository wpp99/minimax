import pandas as pd
import os, re, json
from datetime import datetime

from B.models import Projection, B1nz, Boms, BsjXQDD
from Home.models import Product
from django.core.files.uploadedfile import TemporaryUploadedFile

# 映射choices
choice_map = {
    "海运 By Sea": 1,
    "海运\nBy Sea": 1,
    "空运 By Air": 2,
    "空运\nBy Air": 2,
    "陆运 By Truck": 3,
    "陆运": 3,
    "陆运\nBy Truck": 3,
    "陆运\nBy Land": 3,
    "快递 By Express": 4,
    "快递\nBy Express": 4,
    "快递/Express": 4,
    '象征性发货': 1,
    '必须发': 2,
    '不能早发': 3,
    '能早发早发': 4,
    '正常发货': 5,
    '按计划正常发货': 5,
    '合同规定交付时间': 5,
    '按正常交货天书计算': 5,
    '需检验非标ITP': 6,
    '标准ITP': 7,
    '非标ITP': 8,
    '需检验标准ITP': 9,
    '未开始': 1,
    '已完成': 2,
    '未通过': 3,
    '取消': 4,
    '特殊通道': 5,
    '本次会审': 6,
    '非直运': 1,
    '目的地': 2,
    '待发区': 3,
}


bom_map = {
    'SGY01': 1,
    'SGY02': 2,
    'SGY03': 3,
    'SGCE': 4,
    'WNozzle': 5,
    'SGF': 6,
    'SGK10': 7,
    'SGK30': 8,
    'SGK40': 9,
    'SGJ10': 10,
    'SGJ20': 11,
    'GasNozzle': 12,
    'SGA10': 13,
    'SGA20': 14,
    'SGA30': 15,
    'SGP': 16,
    'WaterPiping': 17,
    'GasPiping': 18,
    'Supports': 19,
    'InstAcc': 20,
}

bom_map_inverse = {v: k for k, v in bom_map.items()}


choice_map = dict(choice_map, **bom_map)

# 系统名称
bom_name = bom_map.keys()


def make_header(model_obj):
    header = []
    for field in  model_obj._meta.fields:
        header.append('{field: %s, title: %s, width: 100, sort: true}' % (field.name, field.verbose_name))
    header.append('{fixed: "right",  width: 200, align: "center", toolbar: "#barDemo"}')
    return header


class Del_Load_1nz:
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.res_datalist = []
        self.need_fields = []

    def b1nz_three(self, d):
        if d in choice_map.keys():
            return d
        elif isinstance(d, datetime):
            if datetime.now() > d:
                return "未开始"
            else:
                return "已完成"
        elif str(d) == 'N/A':
            return "取消"
        return "未开始"
    
    def del_date(self, date_data):
        """处理时间"""
        res = re.findall("(\d{4}-\d{2}-\d{2})", str(date_data))
        if res:
            return res[0]
        return None

    def del_map(self, d):
        """choice 映射"""
        if d in choice_map.keys():
            return choice_map[d]
        return 1    
    
    def del_num_null(self, d):
        """处理为空的数值字段"""
        if isinstance(d, datetime):
            return 0
        res = re.findall("([0-9]\d*\.?\d*)", str(d))
        if res:
            return float(res[0])
        return 0

    def del_1nz(self, file_name=None):
        header = 7
        if file_name:
            t_pro = file_name.replace("ML_all", '').replace(".xlsx", '')
            if t_pro == "9889212001" or t_pro == "8409212002":
                header = 8
        
        excel_data = pd.read_excel(self.file_obj, sheet_name='1nz', header=header)
        
        df = excel_data[excel_data.iloc[:, 2].str.contains('DY\d{3}[a-zA-Z]?$', na=False)]
        df = df.fillna('')
        df[df.iloc[:, 23] == "N/A"] = "取消"
        for index, row in df.iterrows():
            self.res_datalist.append(dict(
                batch_no = row.iloc[2],   
                description = str(row.iloc[3])[:250],
                area = str(row.iloc[4])[:90], 
                design_date = self.del_date(row.iloc[5]),     
                deliver_date = self.del_date(row.iloc[6]),      
                itp_date = row.iloc[7],   
                port = row.iloc[8],
                trans_method = row.iloc[9],   
                grossWeight = self.del_num_null(row.iloc[10]),  
                volume = self.del_num_null(row.iloc[11]), 
                ship_no = row.iloc[12],   
                wayBill_no = row.iloc[13],  
                arrive_date = self.del_date(row.iloc[14]),      
                con_date = self.del_date(row.iloc[17]),     
                nz_date = self.del_date(row.iloc[18]),    
                true_date = self.del_date(row.iloc[19]),      
                mx_body = row.iloc[20],     
                trans_des = row.iloc[21],    
                pack_des = row.iloc[22],      
                three_status = self.b1nz_three(row.iloc[23]),   
                directShipment = row.iloc[24],
                trans_to = row.iloc[25],
            ))
        return self.res_datalist
    
    def load_1nz(self, pro_no):
        B1nz.objects.filter(pro_no=pro_no).delete()
        datalist = []
        self.need_fields = list(self.res_datalist[0].keys())
        self.need_fields.append("pro_no")
        
        for dataitme in self.res_datalist:
            # with open("./static/b1nz.txt", "a", encoding="utf-8") as f:
            #     f.writelines(str(dataitme)+"\n")
            dataitme["pro_no"] = pro_no
            dataitme["three_status"] = self.del_map(dataitme["three_status"])
            dataitme["directShipment"] = self.del_map(dataitme["directShipment"])
            dataitme["trans_des"] = self.del_map(dataitme["trans_des"])
            dataitme["trans_method"] = self.del_map(dataitme["trans_method"])
            b1nz = B1nz(**dataitme)
            datalist.append(b1nz)
        # B1nz.objects.bulk_update_or_create(datalist, self.need_fields, match_field=['pro_no', 'batch_no'])
        B1nz.objects.bulk_create(datalist)


class Del_load_sjxqd:
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.res_datalist = []
        self.extra_pro = [
            '9889132001', '9888232007', '9839151001', '5889112005', '9889242001',]
   
    def del_date(self, date_data):
        """处理时间"""
        res = re.findall("(\d{4}-\d{2}-\d{2})", str(date_data))
        if res:
            return res[0]
        return None
    
    def del_date_seria(self, date_datas):
        """合并多列时间"""
        date_datas[date_datas.isnull()] = ''
        strings = ""
        for date_ in date_datas[:-1]:
            if date_:
                strings += str(self.del_date(date_))
                strings += ";"
        return strings
    
    def del_sjxqd(self, file_name=None):
        """处理数据"""
        header = 6
        if file_name:
            t_pro = file_name.replace("ML_all", '').replace(".xlsx", '')
        else:
            t_pro = os.path.split(self.file_obj)[1].replace("ML_all", '').replace(".xlsx", '')
        if t_pro == "9887142040":
            header = 7225
        excel_data = pd.read_excel(self.file_obj, sheet_name='sjXQD', header=header)
        obj_data = excel_data[excel_data.iloc[:, 4].notna()]
        obj_data = obj_data.fillna('')

        for index, row in obj_data.iterrows():
            
            if t_pro in self.extra_pro:
                start_date = self.del_date(row["起始日期\n（合同契约）"])
                end_date = self.del_date(row["终止/关闭日期\n（合同契约）"])
                sjXQD = str(row["sjXQD"])[:250]
                date_seria = self.del_date(row["日期1":])
                xqd_remind = row["备注\nRemark"]
                audit_level = None
                zgxy = None
                status = None
            else:
                start_date = self.del_date(row[5])
                end_date =  self.del_date(row["关闭/最迟日期"])
                sjXQD = str(row[4])[:250]
                date_seria = self.del_date_seria(row["日期1": "sjXQD要点及备注\nRemark"])
                xqd_remind = row["XQD1,2备注"]
                audit_level = row["审核\n级别"]
                zgxy = row[3]
                status = row[9]
            
            self.res_datalist.append({
                'num': str(row[1])[:25],
                "sys_code": str(row[2])[:25],
                "zgxy": zgxy,
                "content_zgxy": sjXQD,
                "start_date": start_date,
                "close_date": end_date,
                "res_per": row["责任人"],
                "audit_level": audit_level,
                "status":status,
                "date_seria": date_seria,
                "sjxqd_remark": row["sjXQD要点及备注\nRemark"],
                "xqd0":row["XQD0"],
                "xqd1":row["XQD1"],
                "xqd2":row["XQD2"],
                "xqd_remind":xqd_remind,
            })
        return self.res_datalist
   
    def load_sjxqd(self, pro_no):
        BsjXQDD.objects.filter(pro_no=pro_no).delete()
        """导入数据库"""
        datalist = []
        for dataitme in self.res_datalist:
            dataitme["pro_no"] = pro_no
            bom = BsjXQDD(**dataitme)
            datalist.append(bom)
        BsjXQDD.objects.bulk_create(datalist)



class Del_load_bom:
    
    def __init__(self, file_obj=None):
        self.file_obj = file_obj
        self.res_datalist = []
    
    def del_str(self, datas, names):
        """合并多列"""
        data_dict = {}
        for d, n in zip(datas[:-1], names[:-1]):
            res = re.findall("([1-9]\d*)", str(d))
            if res:
                if n in ['[自动]', '公式', 'Bb量\n公式']:
                    continue
                data_dict[n] = int(res[0])

        return json.dumps(data_dict)

    def del_num_null(self, d):
        if isinstance(d, datetime):
            return 0
        res = re.findall("([0-9]\d*\.?\d*)", str(d))
        if res:
            return float(res[0])
        return 0

    def del_bom(self, sheet_name):
        """处理数据"""
        # data_head5 = pd.read_excel(self.file_obj, sheet_name=sheet_name, header=5)
        df = pd.read_excel(self.file_obj, sheet_name=sheet_name, header=5)
        columns = df.iloc[0, :]
        bb_names = columns["C301": "C399"]
        bc_names = columns["C401": "C499"]
        bd_names = columns["C601": "C699"]
        be_names = columns["C701": "C790"]
        
        data = df[df["C103"].map(str).str.contains("[1-9]\d*")]
        data = data.fillna('')
        
        for index, row in data.iterrows():
            self.res_datalist.append({
                "inventory_code": row["C102"],
                "unit": row["C104"],
                "product_name": str(row["C105"])[:250],
                "product_type": str(row["C107"])[:250],
                "m_system": sheet_name,
                "supply": row["C108"],
                "ba": self.del_num_null(row["C201"]),
                "bb": self.del_str(row["C301":"C399"], bb_names),
                # "bb_sum": int(row["C301": "C396"].map(lambda x: x if x else 0).sum()),
                # "bb_con": row["C397"][0],
                # "bb_res": row["C398"][0],
                "bc": self.del_str(row["C401":"C499"], bc_names),
                # "bc_sum": int(row["C401": "C497"].map(lambda x: x if x else 0).sum()),
                "bd": self.del_str(row["C601":"C699"], bd_names),
                # "bd_sum": int(row["C601": "C697"].map(lambda x: x if x else 0).sum()),
                "be_arrive": self.del_str(row["C701":"C790"], be_names),
                # "be_sum": int(row["C701": "C790"].map(lambda x: x if x else 0).sum()),
                # "bs": self.del_num_null(row["C792"]["现场采购Bs"]),
                # "bd2": self.del_num_null(row["C793"]["现场补发货Bd2"]),
                # "be_install": self.del_num_null(row["C794"]["安装量Be"]),
                # "be_loss": row["C795"]["损耗"],
                # "be_res": self.del_num_null(row["C796"]["剩余总量"]),
                # "be_bb": row["C798"]["安装与设计对比"],
            })
        return self.res_datalist
        
    
    def make_product_code(self, inventory_code, unit, product_name, product_type, supply, m_system):
        if not str(inventory_code).startswith("00000000"):
            pro_obj = Product.objects.filter(inventory_code=inventory_code).first()
            if pro_obj:
                return pro_obj.product_code
        
        last_id = Product.objects.all().order_by("-id").first().id
        new_pro_code = "p" + str(last_id+3).rjust(12, '0')
        Product.objects.create(product_code=new_pro_code, inventory_code=inventory_code, 
            product_name=product_name, product_type=product_type, unit=unit, supply=supply, pro_system=m_system)
        return new_pro_code
        
    def load_bom(self, pro_no):
        # Boms.objects.filter(pro_no=pro_no).delete()
        """导入数据库"""
        datalist = []
        
        for dataitme in self.res_datalist:
            new_pro_code = self.make_product_code(dataitme["inventory_code"], dataitme["unit"], dataitme["product_name"], dataitme["product_type"], dataitme["supply"], choice_map[dataitme["m_system"]])
            
            del dataitme["unit"]
            del dataitme["product_name"]
            del dataitme["product_type"]
            del dataitme["supply"]

            dataitme["m_system"] = choice_map[dataitme["m_system"]]
            dataitme["pro_no"] = pro_no
            dataitme["product_code"] = new_pro_code
           
            print(new_pro_code)
            bom = Boms(**dataitme)
            datalist.append(bom)
        need_field = ['pro_no', 'm_system', 'product_code', 'inventory_code', 'ba', 'bb', 'bc', 'bd', 'be_arrive']
        Boms.objects.bulk_update_or_create(datalist, need_field, match_field=['pro_no', 'm_system', 'product_code'])
        # Boms.objects.bulk_create(datalist)
        