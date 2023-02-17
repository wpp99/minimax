from datetime import datetime, timedelta

from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet




class Projection(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # 项目号
    pro_no = models.CharField(max_length=20, verbose_name='项目号', unique=True)
    # 项目名称
    pro_name = models.CharField(max_length=100, verbose_name='项目名称', null=True, blank=True)
    # 部门编码
    depart_no = models.CharField(max_length=10, verbose_name='部门编码', null=True, blank=True)
    # 客户编码
    client_no = models.CharField(max_length=10, verbose_name='客户编码', null=True, blank=True)

    pm = models.CharField(max_length=20, verbose_name="项目经理", null=True, blank=True)
    # 日期
    pro_date = models.DateField(verbose_name='立项日期', null=True, blank=True)
    # 合同年份
    con_year = models.CharField(verbose_name="合同年份", max_length=5, null=True, blank=True)
    # 合同部门位置
    con_depart = models.CharField(verbose_name="合同部门位置", max_length=10, null=True, blank=True)
    # 项目类型
    con_type = models.CharField(verbose_name="项目类型", max_length=4, null=True, blank=True)
    # 物流状态
    logit_status = models.CharField(verbose_name="物流状态", max_length=10, null=True, blank=True)
    # 项目状态
    pro_status = models.CharField(verbose_name="项目状态", max_length=20, null=True, blank=True)
    # 技术负责人
    pro_tec = models.CharField(max_length=20, verbose_name='技术负责人', null=True, blank=True)
    # 商务负责人
    pro_mer = models.CharField(max_length=20, verbose_name='商务负责人', null=True, blank=True)
    # 客户名称
    client = models.CharField(max_length=100, verbose_name='客户名称', null=True, blank=True)
    # 最终用户
    endUser = models.CharField(max_length=255, verbose_name='最终用户', null=True, blank=True)
    # 项目所在地
    pro_area = models.CharField(max_length=20, verbose_name='项目所在地', null=True, blank=True)
    # SM
    sm = models.CharField(max_length=10, verbose_name='sm', null=True, blank=True)
    # 合同标签
    pro_label = models.CharField(max_length=10, verbose_name='合同标签', null=True, blank=True)
    
    def __str__(self):
        return self.pro_no


class B1nz(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # 项目号
    pro_no = models.ForeignKey(verbose_name='项目号', to='Projection', to_field='pro_no', on_delete=models.CASCADE)
    # 批次号
    batch_no = models.CharField(verbose_name='批次号', max_length=10)
    # 货物描述
    description = models.CharField(verbose_name='货物描述', max_length=255, null=True, blank=True)
    # 区域
    area = models.CharField(verbose_name='区域', max_length=100, null=True, blank=True)
    # 设计输入资料提供时间
    design_date = models.DateField(verbose_name='设计输入时间', null=True, blank=True)
    # 计划交货日期
    deliver_date = models.DateField(verbose_name='计划交货日期', null=True, blank=True)
    # Itp放行日期
    itp_date = models.CharField(verbose_name='Itp放行日期', max_length=100, null=True, blank=True)
    # 起运港
    port = models.CharField(verbose_name='起运港', max_length=100, null=True, blank=True)
    # 运输方式
    trans_choices = (
        (1, 'By sea'),
        (2, 'By air'),
        (3, 'By truck'),
        (4, 'By express')
    )
    trans_method = models.SmallIntegerField(verbose_name='运输方式', choices=trans_choices, null=True, blank=True)
    # 毛重
    grossWeight = models.FloatField(verbose_name='毛重', null=True, blank=True)
    # 体积
    volume = models.FloatField(verbose_name='体积', null=True, blank=True)
    # 船名船次
    ship_no = models.CharField(verbose_name='船名船次', max_length=50, null=True, blank=True)
    # 运单号
    wayBill_no = models.CharField(verbose_name='运单号', max_length=50, null=True, blank=True)
    # 预计到港时间
    arrive_date = models.DateField(verbose_name='预计到港时间', null=True, blank=True)
    # 合同签定发运日期
    con_date = models.DateField(verbose_name='定发运日期', null=True, blank=True)
    # 初版1nz 预测发运日期
    nz_date = models.DateField(verbose_name='1nz发运日期', null=True, blank=True)
    # 实际发货日期
    true_date = models.DateField(verbose_name='实际发货日期', null=True, blank=True)
    # MX 合同主体
    mx_body = models.CharField(verbose_name='MX合同主体', max_length=20, null=True, blank=True)
    # 旅行说明
    trans_des_choices = (
        (1, '象征性发货'),
        (2, '必须发'),
        (3, '不能早发'),
        (4, '能早发早发'),
        (5, '按计划正常发货'),
        (6, '需检验非标ITP'),
        (7, '标准ITP'),
        (8, '非标ITP'),
        (9, '需检验标准ITP'),
    )
    trans_des = models.SmallIntegerField(verbose_name='旅行说明', choices=trans_des_choices, null=True, blank=True)
    # 单独包装说明
    pack_des = models.CharField(verbose_name='单独包装说明', max_length=255, null=True, blank=True)
    # 三部会审状态
    three_choices = (
        (1, '未开始'),
        (2, '已完成'),
        (3, '未通过'),
        (4, '取消'),
        (5, '特殊通道'),
        (6, '本次会审'),
    )
    three_status = models.SmallIntegerField(verbose_name='三部会审状态', choices=three_choices, null=True, blank=True)
    # 直运至
    direct_choices = (
        (1, '非直运'),
        (2, '目的地'),
        (3, '待发区'),
    )
    directShipment = models.SmallIntegerField(verbose_name='直运至', choices=direct_choices, null=True, blank=True)
    # 发运地
    trans_to = models.CharField(verbose_name='发运地', max_length=50, null=True, blank=True)


class BsjXQDD(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # 项目号
    pro_no = models.ForeignKey(verbose_name='项目号', to='Projection', to_field='pro_no', on_delete=models.CASCADE)
    # 序号
    num = models.CharField(verbose_name='序号', max_length=30, null=True, blank=True)
    # 系统代码
    sys_code = models.CharField(verbose_name='系统代码', max_length=30, null=True, blank=True)
    # ZGXY
    zgxy = models.CharField(verbose_name='ZGXY', max_length=255, null=True, blank=True)
    # sjxqd内容
    content_zgxy = models.CharField(verbose_name='sjxqd内容', max_length=255, null=True, blank=True)
    # 起始日期
    start_date = models.DateField(verbose_name='起始日期', null=True, blank=True)
    # 关闭日期
    close_date = models.DateField(verbose_name='关闭日期', null=True, blank=True)
    # 责任人
    res_per = models.CharField(verbose_name='责任人', max_length=20, null=True, blank=True)
    # 审核级别
    audit_level = models.CharField(verbose_name='审核级别', max_length=30, null=True, blank=True)
    # 
    sjxqd_remark = models.CharField(verbose_name="sjxqd备注", max_length=255, null=True, blank=True) 
    # 状态
    status = models.CharField(verbose_name='状态', max_length=35, null=True, blank=True)
    # 日期序列
    date_seria = models.CharField(verbose_name='日期序列', max_length=255, null=True, blank=True)
    # XQD
    xqd0 = models.CharField(verbose_name='xqd0', max_length=5, null=True, blank=True)
    xqd1 = models.CharField(verbose_name='xqd1', max_length=5, null=True, blank=True)
    xqd2 = models.CharField(verbose_name='xqd2', max_length=5, null=True, blank=True)
    # XQD12备注
    xqd_remind = models.CharField(verbose_name='xqd备注', max_length=255, null=True, blank=True)


class Boms(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # 项目号
    pro_no = models.ForeignKey(verbose_name='项目号', to='Projection', to_field='pro_no', on_delete=models.CASCADE)
    # 产品编码
    product_code = models.CharField(verbose_name='产品编码', max_length=20)
    inventory_code = models.CharField(verbose_name='存货编码', max_length=20, default='')
    # 所属系统
    m_system_choices = (
        (1, 'SGY01'),
        (2, 'SGY02'),
        (3, 'SGY03'),
        (4, 'SGCE'),
        (5, 'WNozzle'),
        (6, 'SGF'),
        (7, 'SGK10'),
        (8, 'SGK30'),
        (9, 'SGK40'),
        (10, 'SGJ10'),
        (11, 'SGJ20'),
        (12, 'GasNozzle'),
        (13, 'SGA10'),
        (14, 'SGA20'),
        (15, 'SGA30'),
        (16, 'SGP'),
        (17, 'WaterPiping'),
        (18, 'GasPiping'),
        (19, 'Supports'),
        (20, 'InstAcc'),
    )
    m_system = models.SmallIntegerField(verbose_name='所属系统', choices=m_system_choices)
    # Ba
    ba = models.IntegerField(verbose_name='ba', null=True, blank=True)
    # Bb
    bb = models.JSONField(verbose_name='设计量',  null=True, blank=True, default=dict)
    bb_con = models.IntegerField(verbose_name="合同备件", default=0, blank=True)
    bb_res = models.IntegerField(verbose_name="建造余量", default=0, blank=True)
    bc = models.JSONField(verbose_name='采购量', max_length=255, null=True, blank=True, default=dict)
    bd = models.JSONField(verbose_name='发货量', max_length=255, null=True, blank=True, default=dict)
    be_arrive = models.JSONField(verbose_name='到货量', max_length=255, null=True, blank=True, default=dict)
    bs = models.IntegerField(verbose_name="现场采购量", default=0, blank=True)
    bd2 = models.IntegerField(verbose_name="现场补发货", default=0, blank=True)
    be_install = models.IntegerField(verbose_name='安装量',  default=0, blank=True)
    be_res = models.IntegerField(verbose_name='剩余量', default=0)


