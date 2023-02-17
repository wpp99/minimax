from datetime import datetime, timedelta

from django.db import models
from B.models import Boms
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


def get_next_week2_date():
    now_date = datetime.now()
    day_num = now_date.isoweekday()
    next_week2 = now_date + timedelta(days=9-day_num)
    return next_week2.strftime("%Y-%m-%d")


class Projection(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # 项目号
    pro_no = models.CharField(max_length=20, verbose_name='项目号', unique=True)
    # 项目名称
    pro_name = models.CharField(max_length=255, verbose_name='项目名称')
    # 部门编码
    depart_no = models.CharField(max_length=10, verbose_name='部门编码')
    # 客户编码
    client_no = models.CharField(max_length=10, verbose_name='客户编码')
    # 日期
    pro_date = models.DateField(verbose_name='日期')
    # 技术负责人
    pro_tec = models.CharField(max_length=20, verbose_name='技术负责人')
    # 商务负责人
    pro_mer = models.CharField(max_length=40, verbose_name='商务负责人')
    # 客户名称
    client = models.CharField(max_length=40, verbose_name='客户名称')
    # 最终用户
    endUser = models.CharField(max_length=40, verbose_name='最终用户')
    # 项目所在地
    pro_area = models.CharField(max_length=40, verbose_name='项目所在地')
    # SM
    sm = models.CharField(max_length=10, verbose_name='sm')
    # 合同标签
    pro_label = models.CharField(max_length=10, verbose_name='合同标签')
    
    def __str__(self):
        return self.pro_no


class Product(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # 产品编码
    product_code = models.CharField(verbose_name='产品编码', max_length=15, unique=True)
    # 存货编码
    inventory_code = models.CharField(verbose_name='存货编码', max_length=15, null=True, blank=True)
    # 名称
    product_name = models.CharField(verbose_name='名称', max_length=255, default='', null=True, blank=True)
    # 单位
    unit = models.CharField(verbose_name='单位', max_length=20, default='个', null=True, blank=True)
    # 型号
    product_type = models.CharField(verbose_name="型号", max_length=255, null=True, blank=True)
    # 所属系统
    pro_system = models.SmallIntegerField(verbose_name="所属系统", choices=Boms.m_system_choices, null=True, blank=True)
    # 供应商
    supply = models.CharField(verbose_name='供应商', max_length=100, null=True, blank=True)
    # 供应商编码
    # 供应类型
    # 座位号
    place_no = models.CharField(verbose_name='座位号', max_length=15, null=True, blank=True)
    # 现有库存 
    inventory_num = models.IntegerField(verbose_name='现有库存', default=0)
    # 备注
    # 详细描述
    detail = models.TextField(verbose_name="详细描述", null=True, blank=True)


class Guan(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    pro_no = models.CharField(verbose_name="批次", max_length=30, null=True, blank=True)
    batch = models.CharField(verbose_name="批次", max_length=30, null=True, blank=True)
    product_num = models.IntegerField(verbose_name="产品数量", null=True, blank=True)
    prod_task_content = models.CharField(verbose_name="生产任务综述", max_length=255, null=True, blank=True)
    product_code = models.CharField(verbose_name="产品编号", max_length=20, null=True, blank=True)
    order_date = models.DateField(verbose_name="邮件下单", null=True, blank=True)
    acc_date = models.DateField(verbose_name="接单日期", null=True, blank=True)
    sj_date = models.DateField(verbose_name="SJ日期", null=True, blank=True)
    expect_date = models.DateField(verbose_name="期望交期", null=True, blank=True)
    table0_update_date = models.DateField(verbose_name="0号表更新日期", null=True, blank=True)
    first_sign_date = models.DateField(verbose_name="首签交期", null=True, blank=True)
    change_date = models.DateField(verbose_name="交期变更", null=True, blank=True)
    responsible = models.CharField(verbose_name="责任人", max_length=20, null=True, blank=True)
    inventory_code = models.CharField(verbose_name="存货编码", max_length=20, null=True, blank=True)
    status = models.CharField(verbose_name="状态", max_length=20, null=True, blank=True)
    warehousing_date = models.DateField(verbose_name="入库日期", null=True, blank=True)
    warehousing_num = models.IntegerField(verbose_name="实际入库数量", null=True, blank=True)
    warehousing_code = models.CharField(verbose_name="入库单号", max_length=20, null=True, blank=True)
    change_record = models.CharField(verbose_name="变更记录", max_length=255, null=True, blank=True)
    attribute = models.CharField(verbose_name="属性", max_length=20, null=True, blank=True)
    description = models.CharField(verbose_name="描述", max_length=255, null=True, blank=True)
    jin1 = models.IntegerField(verbose_name="1#", null=True, blank=True)
    warehousing_status = models.CharField(verbose_name="到货状态", max_length=30, null=True, blank=True)
    assembly_method = models.CharField(verbose_name="组装方式", max_length=20, null=True, blank=True)
    last_deliver_date = models.DateField(verbose_name="最新交期", null=True, blank=True)
    file_place = models.CharField(verbose_name="FB文件夹", max_length=255, null=True, blank=True)
    to_warehouse = models.IntegerField(verbose_name="待入库", null=True, blank=True)
    change_times = models.IntegerField(verbose_name="变更次数", null=True, blank=True)
    under_construction = models.IntegerField(verbose_name="在建", null=True, blank=True)
    success_num = models.IntegerField(verbose_name="产成品", null=True, blank=True)

    need_1nz = models.CharField(verbose_name="1nz需求", max_length=30, null=True, blank=True)
    manage_order_no = models.CharField(verbose_name="管理单号", max_length=20, null=True, blank=True)
    sales_order = models.CharField(verbose_name="销售订单", max_length=20, null=True, blank=True)
    manage_code = models.CharField(verbose_name="管理单号", max_length=50, null=True, blank=True)
    process_code = models.CharField(verbose_name="工艺卡号", max_length=20, null=True, blank=True)

    on_delivery_rate = models.FloatField(verbose_name="准时交付率", null=True, blank=True)
    yield_rate = models.FloatField(verbose_name="良品率", null=True, blank=True)
    man_assembly_time = models.FloatField(verbose_name="机械组装工时", null=True, blank=True)
    el_assembly_time = models.FloatField(verbose_name="电气组装工时", null=True, blank=True)
    quality_check_time = models.FloatField(verbose_name="质检检验工时", null=True, blank=True)
    op_overlap_rate = models.FloatField(verbose_name="工序重叠率", null=True, blank=True)
    
    inventory_num = models.IntegerField(verbose_name="库存", null=True, blank=True)
    warehouse_out_num = models.IntegerField(verbose_name="销售出库", null=True, blank=True)
    assembly_cycle = models.IntegerField(verbose_name="组装周期", null=True, blank=True)
    srd_num = models.IntegerField(verbose_name="SRD数量", null=True, blank=True)


class Bom_sum_record(models.Model):
     objects = BulkUpdateOrCreateQuerySet.as_manager()
     product_code = models.CharField(max_length=20, verbose_name="产品编码")
     inventory_code = models.CharField(max_length=20, verbose_name="存货编码")
     pro_sys_bc = models.JSONField(verbose_name="项目号|系统|bc")
     total_sum = models.IntegerField(verbose_name="总数")
     submit_date = models.DateField(verbose_name="提取时间", default=datetime.now().strftime("%Y-%m-%d"))


class ThreePartMeet(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    threemeet_code = models.CharField(verbose_name="三部会审编码", max_length=20)
    depart = models.CharField(verbose_name="部门", max_length=20)
    pro_no = models.CharField(verbose_name="项目号", max_length=20)
    batch = models.CharField(verbose_name="批次", max_length=50)
    participants = models.CharField(verbose_name="参加人员", max_length=30)
    meet_date = models.DateField(verbose_name="时间", default=get_next_week2_date())
    status_choices = (
        (1, "未开始"),
        (2, "全部通过"),
        (3, "部分通过"),
        (4, "已关闭"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1, blank=True)
    remark = models.CharField(verbose_name="备注", max_length=255, default='', blank=True)
    meet_sign_filepath = models.CharField(verbose_name="签字版文件路径", max_length=255, default='', blank=True)

class threePartRemark(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    three_product_code = models.CharField(verbose_name="流程号", max_length=40)
    threemeet_code = models.CharField(verbose_name="三部会审编码", max_length=20)
    product_code = models.CharField(verbose_name="产品编码", max_length=20)
    pro_no = models.CharField(verbose_name="项目号", max_length=20)
    depart = models.CharField(verbose_name="部门编码", max_length=10)
    batch = models.CharField(verbose_name="批次", max_length=10)
    num = models.IntegerField(verbose_name="数量")
    remark = models.CharField(verbose_name="备注", max_length=255, default="")


# 销售订单
class SaleOrder(models.Model):
    three_product_code = models.CharField(verbose_name="流程号", max_length=40)
    bom = models.CharField(verbose_name="bom", max_length=30)
    business_type = models.CharField(verbose_name="业务类型", max_length=10)
    order_number = models.CharField(verbose_name="订单号", max_length=20)
    prepared_by = models.CharField(verbose_name="制单人", max_length=10)
    order_date = models.DateField(verbose_name="订单日期")
    reviewed_by = models.CharField(verbose_name="审核人", max_length=10)
    audit_date = models.DateField(verbose_name="审核时间")
    close_by = models.CharField(verbose_name="关闭人", max_length=10)
    sale_num = models.IntegerField(verbose_name="数量")
    pre_delevery_date = models.DateField(verbose_name="预计发货日期")
    order_sub_id = models.CharField(verbose_name="订单子表ID", max_length=20)
    unship_num = models.IntegerField(verbose_name="未发货数量")
    un_order = models.IntegerField(verbose_name="未下达采购")
    close_date= models.DateField(verbose_name="关闭日期")



# 采购订单  1 3 6 9 11 13    预计入库量 Q9 
class PurchaseOrder(models.CharField):
    three_product_code = models.CharField(verbose_name="流程号", max_length=40)
    order_code = models.CharField(verbose_name="订单号", max_length=30)
    business_type = models.CharField(verbose_name="业务类型", max_length=10)
    purchase_type = models.CharField(verbose_name="采购类型", max_length=20)
    purchase_num = models.IntegerField(verbose_name="数量")
    upper_order_code = models.CharField(verbose_name="上游单据号", max_length=30)
    prepared_by = models.CharField(verbose_name="制单人", max_length=10)
    order_date = models.DateField(verbose_name="订单日期")
    reviewed_by = models.CharField(verbose_name="审核人", max_length=10)
    audit_date = models.DateField(verbose_name="审核时间")
    arrive_date = models.DateField(verbose_name="计划入库日期")
    warehouse_status = models.CharField(verbose_name="入库状态", max_length=10)
    remark = models.CharField(verbose_name="备注", max_length=255)


# 库存   现存量 Q7
class Inventory(models.Model):
    product_code = models.CharField(verbose_name="产品编码", max_length=20)
    inventory_code = models.CharField(verbose_name="存货编码", max_length=20)
    inventory_name = models.CharField(verbose_name="存货名称", max_length=255)

    warehouse_code = models.CharField(verbose_name="仓库编码", max_length=20)
    warehouse_name = models.CharField(verbose_name="仓库名称", max_length=100)

    # unit = models.CharField(verbose_name="单位", max_length=10)
    # specific_model = models.CharField(verbose_name="规格型号", max_length=255)

    inven_now_num = models.IntegerField(verbose_name="现存数量")
    to_inventory_num = models.IntegerField(verbose_name="预计入库量", null=True, blank=True)
    inven_delivery_num = models.IntegerField(verbose_name="待发货量", null=True, blank=True)
    inven_class_code = models.CharField(verbose_name="存货分类代码", max_length=20)
    inven_class_name = models.CharField(verbose_name="存货分类名称", max_length=255)
    inven_con_code = models.CharField(verbose_name="存货合同号", max_length=20)
    need_flow_code = models.CharField(verbose_name="需求跟踪号", max_length=20, null=True, blank=True)


# 销售出库订单 
class SaleOutInventory(models.Model):
    three_product_code = models.CharField(verbose_name="流程号", max_length=40)
    ac_set = models.CharField(verbose_name="账套", max_length=20)
    warehouse_code = models.CharField(verbose_name="仓库编码", max_length=20)
    warehouse_name = models.CharField(verbose_name="仓库名称", max_length=100)
    warehouse_out_code = models.CharField(verbose_name="出库单号", max_length=20)
    out_num = models.IntegerField(verbose_name="数量")
    out_date = models.DateField(verbose_name="出库日期")
    order_code = models.CharField(verbose_name="来源订单号", max_length=20)
    reviewed_by = models.CharField(verbose_name="审核人", max_length=10)
    audit_date = models.DateField(verbose_name="审核时间")
    out_type = models.CharField(verbose_name="出库类型", max_length=20)




