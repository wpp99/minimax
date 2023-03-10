export var headers = {
    "1nz": [
        { field: "id", title: "序号", width: 80, sort: true },
        { field: "batch_no", title: "批次号", width: 80 },
        { field: "description", title: "货物描述", width: 80 },
        { field: "area", title: "区域", width: 80 },
        { field: "design_date", title: "设计输入时间", width: 80 },
        { field: "deliver_date", title: "计划交货日期", width: 80 },
        { field: "itp_date", title: "Itp放行日期", width: 80 },
        { field: "port", title: "起运港", width: 80 },
        { field: "trans_method", title: "运输方式", width: 80 },
        { field: "grossWeight", title: "毛重", width: 80 },
        { field: "volume", title: "体积", width: 80 },
        { field: "ship_no", title: "船名船次", width: 80 },
        { field: "wayBill_no", title: "运单号", width: 80 },
        { field: "arrive_date", title: "预计到港时间", width: 80 },
        { field: "con_date", title: "定发运日期", width: 80 },
        { field: "nz_date", title: "1nz发运日期", width: 80 },
        { field: "true_date", title: "实际发货日期", width: 80 },
        { field: "mx_body", title: "MX合同主体", width: 80 },
        { field: "trans_des", title: "旅行说明", width: 80 },
        { field: "pack_des", title: "单独包装说明", width: 80 },
        { field: "three_status", title: "三部会审状态", width: 80 },
        { field: "directShipment", title: "直运至", width: 80 },
        { field: "trans_to", title: "发运地", width: 80 },
        { fixed: "right", title: "操作", width: 150, align: "center", toolbar: "#barDemo", },
    ],
    "sjxqd": [
        { field: "id", title: "序号", width: 80, sort: true },
        { field: "sys_code", title: "系统代码", width: 100 },
        { field: "zgxy", title: "ZGXY", width: 180 },
        { field: "content_zgxy", title: "sjxqd内容", width: 280 },
        { field: "start_date", title: "起始日期", width: 180 },
        { field: "close_date", title: "关闭日期", width: 180 },
        { field: "res_per", title: "责任人", width: 180 },
        { field: "audit_level", title: "审核级别", width: 120 },
        { field: "status", title: "状态", width: 120 },
        { field: "date_seria", title: "时间", width: 120 },
        { field: "sjxqd_remark", title: "sjxqd备注", width: 120 },
        { field: "xqd0", title: "XQD0", width: 180 },
        { field: "xqd1", title: "XQD1", width: 180 },
        { field: "xqd2", title: "XQD2", width: 180 },
        { field: "xqd12_remind", title: "XQD12备注", width: 180 },
        { fixed: "right", title: "操作", width: 150, align: "center", toolbar: "#barDemo", },
    ],
    "boms": [
        { field: "id", title: "序号", width: 80, sort: true },
        { field: "inventory_code", title: "存货编码", width: 180, sort: true },
        { field: "product_name", title: "名称", width: 180 },
        { field: "product_type", title: "型号", width: 180, sort: true },
        { field: "unit", title: "单位", width: 80, sort: true },
        { field: "supply", title: "供应商", width: 80, sort: true },
        { field: "m_system", title: "所属系统", width: 180 },
        { field: "ba", title: "ba", width: 80, sort: true },
        { field: "bb", title: "设计量", width: 80 },
        { field: "bb_sum", title: "设计量合计", width: 80, sort: true },
        { field: "bb_con", title: "合同备件", width: 80, sort: true },
        { field: "bb_res", title: "建造余量", width: 80, sort: true },
        { field: "bc", title: "采购量", width: 80 },
        { field: "bc_sum", title: "采购量合计", width: 80, sort: true },
        { field: "bd", title: "发货量", width: 80 },
        { field: "bd_sum", title: "发货量合计", width: 80, sort: true },
        { field: "be_arrive", title: "到货量", width: 80, sort: true },
        { field: "be_arrive_sum", title: "到货量合计", width: 80, sort: true },
        { field: "bs", title: "现场采购量", width: 80, sort: true },
        { field: "bd2", title: "现场补发货", width: 80, sort: true },
        { field: "be_res", title: "剩余总量", width: 80, sort: true },
        { field: "be_bd", title: "be-bd", width: 80, sort: true },
        { field: "be_loss", title: "损失量", width: 80, sort: true },
        { field: "be_bb", title: "安装设计比较", width: 80, sort: true },
        { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
    ],
    "product":[
        { field: "id", title: "序号", width: 80, sort: true },
        { field: "product_code", title: "产品编码", width: 180, sort: true },
        { field: "material_no", title: "存货编码", width: 180, sort: true },
        { field: "material_name", title: "名称", width: 180 },
        { field: "material_type", title: "型号", width: 180, sort: true },
        { field: "m_system", title: "所属系统", width: 180 },
        { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
    ],
    // "projection":[
    //     { field: "id", title: "序号", width: 80, sort: true },
    //     { field: "con_year", title: "合同年份", width: 80, sort: true },
    //     { field: "con_depart", title: "合同部门位置", width: 80, sort: true },
    //     { field: "pro_no", title: "合同号", width: 180, sort: true },
    //     { field: "pro_name", title: "项目名称", width: 200, sort: true },
    //     { field: "depart_no", title: "部门编码", width: 80, sort: true },
    //     { field: "pm", title: "项目PM", width: 180, sort: true },
    //     { field: "pro_mer", title: "商务", width: 180, sort: true },
    //     { field: "con_type", title: "项目类型", width: 180, sort: true },
    //     { field: "pro_label", title: "合同标签", width: 180, sort: true },
    //     { field: "pro_date", title: "LX日期", width: 180, sort: true },
    //     { field: "logit_status", title: "物流是否关闭", width: 180, sort: true },
    //     { field: "pro_status", title: "项目状态", width: 180, sort: true },
    //     { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
    // ],
    "guan":[
        { field: "no", title: "序号", width: 80, sort: true,  align: "center" },
        { field: "manage_code", title: "管理单号", width: 80, sort: true,  align: "center" },
        { field: "pro_no", title: "项目号", width: 80, sort: true,  align: "center" },
        { field: "batch", title: "批次", width: 80, sort: true,  align: "center" },
        { field: "product_num", title: "产品数量", width: 80, sort: true,  align: "center" },
        { field: "prod_task_content", title: "生产任务综述", width: 80, sort: true,  align: "center" },
        { field: "product_code", title: "产品编号", width: 80, sort: true,  align: "center" },
        { field: "order_date", title: "邮件下单", width: 80, sort: true,  align: "center" },
        { field: "acc_date", title: "接单日期", width: 80, sort: true,  align: "center" },
        { field: "sj_date", title: "SJ日期", width: 80, sort: true,  align: "center" },
        { field: "expect_date", title: "期望交期", width: 80, sort: true,  align: "center" },
        { field: "table0_update_date", title: "0号表更新日期", width: 80, sort: true,  align: "center" },
        { field: "first_sign_date", title: "首签交期", width: 80, sort: true,  align: "center" },
        { field: "change_date", title: "交期变更", width: 80, sort: true,  align: "center" },
        { field: "responsible", title: "责任人", width: 80, sort: true,  align: "center" },
        { field: "inventory_code", title: "存货编码", width: 80, sort: true,  align: "center" },
        { field: "status", title: "状态", width: 80, sort: true,  align: "center" },
        { field: "warehousing_date", title: "入库日期", width: 80, sort: true,  align: "center" },
        { field: "warehousing_num", title: "实际入库数量", width: 80, sort: true,  align: "center" },
        { field: "warehousing_code", title: "入库单号", width: 80, sort: true,  align: "center" },
        { field: "change_record", title: "变更记录", width: 80, sort: true,  align: "center" },
        { field: "attribute", title: "属性", width: 80, sort: true,  align: "center" },
        { field: "description", title: "描述", width: 80, sort: true,  align: "center" },
        { field: "jin1", title: "1#", width: 80, sort: true,  align: "center" },
        { field: "warehousing_status", title: "到货状态", width: 80, sort: true,  align: "center" },
        { field: "assembly_method", title: "组装方式", width: 80, sort: true,  align: "center" },
        { field: "last_deliver_date", title: "最新交期", width: 80, sort: true,  align: "center" },
        { field: "file_place", title: "FB文件夹", width: 80, sort: true,  align: "center" },
        { field: "to_warehouse", title: "待入库", width: 80, sort: true,  align: "center" },
        { field: "need_1nz", title: "1nz需求", width: 80, sort: true,  align: "center" },
        { field: "change_times", title: "变更次数", width: 80, sort: true,  align: "center" },
        { field: "under_construction", title: "在建", width: 80, sort: true,  align: "center" },
        { field: "success_num", title: "产成品", width: 80, sort: true,  align: "center" },
        { field: "on_delivery_rate", title: "准时交付率", width: 80, sort: true,  align: "center" },
        { field: "yield_rate", title: "良品率", width: 80, sort: true,  align: "center" },
        { field: "manage_order_no", title: "管理单号", width: 80, sort: true,  align: "center" },
        { field: "sales_order", title: "销售订单", width: 80, sort: true,  align: "center" },
        { field: "assembly_cycle", title: "组装周期", width: 80, sort: true,  align: "center" },
        { field: "man_assembly_time", title: "机械组装工时", width: 80, sort: true,  align: "center" },
        { field: "el_assembly_time", title: "电气组装工时", width: 80, sort: true,  align: "center" },
        { field: "quality_check_time", title: "质检检验工时", width: 80, sort: true,  align: "center" },
        { field: "op_overlap_rate", title: "工序重叠率", width: 80, sort: true,  align: "center" },
        { field: "process_code", title: "工艺卡号", width: 80, sort: true,  align: "center" },
        { field: "srd_num", title: "SRD数量", width: 80, sort: true,  align: "center" },
        { field: "inventory_num", title: "库存", width: 80, sort: true,  align: "center" },
        { field: "warehouse_out_num", title: "销售出库", width: 80, sort: true,  align: "center" },
        { fixed: "right", title: "操作",  align: "center", toolbar: "#barDemo", width: 180},
    ],
    "warehouse":[
        { field: "no", title: "序号", width: 80, sort: true,  align: "center" },
        { field: "product_code", title: "产品编码", width: 180, sort: true,  align: "center" },
        { field: "inventory_code", title: "存货编码", width: 180, sort: true,  align: "center" },
        { field: "inventory_name", title: "存货名称", width: 180, sort: true,  align: "center" },
        { field: "warehouse_code", title: "仓库编码", width: 180, sort: true,  align: "center" },
        { field: "warehouse_name", title: "仓库名称", width: 180, sort: true,  align: "center" },
        { field: "inven_now_num", title: "现存数量", width: 80, sort: true,  align: "center" },
        { field: "to_inventory_num", title: "预计入库量", width: 80, sort: true,  align: "center" },
        { field: "inven_delivery_num", title: "待发货量", width: 80, sort: true,  align: "center" },
        { field: "inven_class_code", title: "存货分类代码", width: 180, sort: true,  align: "center" },
        { field: "inven_class_name", title: "存货分类名称", width: 80, sort: true,  align: "center" },
        { field: "inven_con_code", title: "存货合同号", width: 180, sort: true,  align: "center" },
        { field: "need_flow_code", title: "需求跟踪号", width: 180, sort: true,  align: "center" },
        { fixed: "right", title: "操作",  align: "center", toolbar: "#barDemo", width: 180},
    ],
    "purchase":[
        { field: "no", title: "序号", width: 80, sort: true,  align: "center" },
        { field: "ac_set", title: "账套", width: 80, sort: true,  align: "center" },
        { field: "pro_batch", title: "项目批次号", width: 180, sort: true,  align: "center" },
        { field: "pro_des", title: "项目描述", width: 180, sort: true,  align: "center" },
        { field: "depart", title: "部门", width: 80, sort: true,  align: "center" },
        { field: "order_code", title: "订单号", width: 180, sort: true,  align: "center" },
        { field: "product_code", title: "产品编码", width: 180, sort: true,  align: "center" },
        { field: "inventory_code", title: "存货编码", width: 180, sort: true,  align: "center" },
        { field: "business_type", title: "业务类型", width: 180, sort: true,  align: "center" },
        { field: "purchase_type", title: "采购类型", width: 180, sort: true,  align: "center" },
        { field: "purchase_num", title: "数量", width: 80, sort: true,  align: "center" },
        { field: "upper_order_code", title: "上游单据号", width: 180, sort: true,  align: "center" },
        { field: "prepared_by", title: "制单人", width: 80, sort: true,  align: "center" },
        { field: "order_date", title: "订单日期", width: 180, sort: true,  align: "center" },
        { field: "reviewed_by", title: "审核人", width: 180, sort: true,  align: "center" },
        { field: "audit_date", title: "审核时间", width: 180, sort: true,  align: "center" },
        { field: "arrive_date", title: "计划入库日期", width: 180, sort: true,  align: "center" },
        { field: "warehouse_status", title: "入库状态", width: 180, sort: true,  align: "center" },
        { field: "arrive_status", title: "到货状态", width: 180, sort: true,  align: "center" },
        { field: "cum_towarehouse_num", title: "累计入库数量", width: 180, sort: true,  align: "center" },
        { field: "remark", title: "备注", width: 80, sort: true,  align: "center" },
        { fixed: "right", title: "操作",  align: "center", toolbar: "#barDemo", width: 180},
    ],
    "sale_out":[
        { field: "no", title: "序号", width: 80, sort: true,  align: "center" },
        { field: "pro_batch", title: "项目批次号", width: 180, sort: true,  align: "center" },
        { field: "depart", title: "销售部门", width: 180, sort: true,  align: "center" },
        { field: "product_code", title: "产品编码", width: 180, sort: true,  align: "center" },
        { field: "inventory_code", title: "存货编码", width: 180, sort: true,  align: "center" },
        { field: "ac_set", title: "账套", width: 80, sort: true,  align: "center" },
        { field: "warehouse_code", title: "仓库编码", width: 80, sort: true,  align: "center" },
        { field: "warehouse_name", title: "仓库名称", width: 180, sort: true,  align: "center" },
        { field: "warehouse_out_code", title: "出库单号", width: 180, sort: true,  align: "center" },
        { field: "out_num", title: "数量", width: 80, sort: true,  align: "center" },
        { field: "out_date", title: "出库日期", width: 180, sort: true,  align: "center" },
        { field: "order_code", title: "来源订单号", width: 180, sort: true,  align: "center" },
        { field: "reviewed_by", title: "审核人", width: 80, sort: true,  align: "center" },
        { field: "audit_date", title: "审核时间", width: 180, sort: true,  align: "center" },
        { field: "out_type", title: "出库类型", width: 180, sort: true,  align: "center" },
        { field: "srd_pro_code", title: "srd产品编号", width: 180, sort: true,  align: "center" },
        { fixed: "right", title: "操作",  align: "center", toolbar: "#barDemo", width: 180},
    ],
    "bom_sum":[
        { field: "id", title: "序号", width: 80, sort: true,  align: "center" },
        { field: "product_code", title: "产品编码", width: 120, sort: true,  align: "center" },
        { field: "inventory_code", title: "存货编码", width: 120, sort: true,  align: "center" },
        { field: "pro_sys_bc", title: "项目号|系统|批次",  width: 1300, sort: true,  align: "center" },
        { field: "submit_date", title: "提交日期",  width: 120, sort: true,  align: "center" },
        { fixed: "right", title: "操作",  align: "center", toolbar: "#barDemo", width: 180},
    ],
    "projection":[
        // {type: 'checkbox', fixed: 'left'},
        { field: "no", title: "序号", width: 70 },
        { field: "pro_no", title: "项目号", width: 150 },
        { field: "pro_name", title: "项目名称", width: 200, sort: true },
        { field: "depart_no", title: "部门编码", width: 80, sort: true },
        { field: "pm", title: "项目PM", width: 85, sort: true },
        { field: "client_no", title: "客户编码", width: 80 },
        { field: "con_year", title: "合同年份", width: 85, sort: true },
        { field: "con_depart", title: "合同部门位置", width: 80, sort: true },
        { field: "pro_date", title: "日期", width: 120, sort: true },
        { field: "pro_tec", title: "技术负责人", width: 130 },
        { field: "pro_mer", title: "商务负责人", width: 100 },
        { field: "client", title: "客户名称", width: 135 },
        { field: "endUser", title: "最终用户", width: 135 },
        { field: "pro_area", title: "项目所在地", width: 135 },
        { field: "con_type", title: "项目类型", width: 85, sort: true },
        { field: "sm", title: "SM", width: 85 },
        { field: "logit_status", title: "物流是否关闭", width: 85, sort: true },
        { field: "pro_status", title: "项目状态", width: 85, sort: true },
        { field: "pro_label", title: "合同标签", width: 85, sort: true },
        { field: "id", title: "ID", width: 80, sort: true },
        { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo", },
    ],
};

export function get_head(condiction){
    console.log(condiction);
    var head;
    switch(condiction){
        case "1nz":
            head = headers['1nz'];
            break;
        case "sjXQD":
            head = headers['sjxqd'];
            break;
        case "ALL1nz":
            head = headers["1nz"];
            break;
        case "sjXqdall":
            head = headers["sjxqd"];
            break;
        case "bom_all":
            head = headers["bom_sum"];
            break;
        case "product":
            head = headers['product'];
            break;
        case "projection":
            head = headers['projection'];
            break;
        case "guan":
            head = headers["guan"];
            break
        case "warehouse":
            head = headers["warehouse"];
            break
        case "purchase":
            head = headers["purchase"];
            break
        case "sale_out":
            head = headers["sale_out"];
            break
        default:
            head = headers['boms'];
    }
    return head
};

export var header_map = {
    "id": "序号",
    "product_code": "产品编码",
    "material_no": "存货编码",
    "material_name": "名称",
    "material_type": "型号",
    "m_system": "所属系统",
    "con_year": "合同年份",
    "con_depart": "合同部门位置",
    "pro_name": "项目名称",
    "depart_no": "部门编码",
    "pm": "项目PM",
    "pro_mer": "商务",
    "con_type": "项目类型",
    "pro_label": "合同标签",
    "pro_date": "LX日期",
    "logit_status": "物流是否关闭",
    "pro_status": "项目状态",
    "manage_code": "管理单号",
    "product_num": "产品数量",
    "prod_task_content": "生产任务综述",
    "order_date": "邮件下单",
    "sj_date": "SJ日期",
    "expect_date": "期望交期",
    "batch_no": "批次号", 
    "description": "货物描述", 
    "area": "区域", 
    "design_date": "设计输入时间", 
    "deliver_date": "计划交货日期", 
    "itp_date": "Itp放行日期", 
    "port": "起运港", 
    "trans_method": "运输方式",
    "grossWeight": "毛重", 
    "volume": "体积", 
    "ship_no": "船名船次",
    "wayBill_no": "运单号",
    "arrive_date": "预计到港时间",
    "con_date": "定发运日期",
    "nz_date": "1nz发运日期",
    "true_date": "实际发货日期",
    "mx_body": "MX合同主体",
    "trans_des": "旅行说明",
    "pack_des": "单独包装说明",
    "three_status": "三部会审状态",
    "directShipment": "直运至",
    "trans_to": "发运地",
    "sys_code": "系统代码", 
    "zgxy": "ZGXY", 
    "content_zgxy": "sjxqd内容", 
    "start_date": "起始日期", 
    "close_date": "关闭日期", 
    "res_per": "责任人", 
    "audit_level": "审核级别", 
    "status": "状态", 
    "date_seria": "时间", 
    "sjxqd_remark": "sjxqd备注", 
    "xqd0": "XQD0", 
    "xqd1": "XQD1", 
    "xqd2": "XQD2", 
    "xqd_remind": "XQD12备注", 
    "inventory_code": "存货编码", 
    "product_name": "名称", 
    "product_type": "型号", 
    "unit": "单位", 
    "m_system": "所属系统", 
    "supply": "供应商", 
    "ba": "ba",
    "bb": "设计量",
    "bb_sum": "设计量合计",
    "bb_con": "合同备件",
    "bb_res": "建造余量",
    "bc": "采购量",
    "bc_sum": "采购量合计",
    "bd": "发货量",
    "bd_sum": "发货量合计",
    "be_sum": "安装量量合计",
    "be_loss": "损失量",
    "be_bb": "安装设计比较",
};

// 渲染表格
export function render_table(url, title, head_key){
    var head = headers[head_key];
    var table = layui.table;
    table.render({
        elem: "#demo",
        // height: height,
        url: url, //数据接口（此处为静态数据，仅作演示）
        title: title,
        skin: "line",
        even: true,
        page: true, //开启分页
        limit: 20,
        limits: [20, 30, 50, 100],
        toolbar: "true", //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
        defaultToolbar: ['filter', 'print', 'exports', {
            output: '导出',
            layEvent: "output",
            icon: "layui-icon-down"
        }],
        // defaultToolbar: ['filter'],
        totalRow: false, //开启合计行
        loading: true,
        cols: [head],
    })
};

// 弹出层
export function get_page(url, title, cancel_url){
    var layer = layui.layer;
    var $ = layui.$;
    $.get(url, function (str) {
        layer.open({
            type: 1,
            title: title,
            skint: "demo-class",
            area: ["400px", "300px"],
            offset: "auto",
            anim: 0, //  弹出动画
            isOutAnim: true,
            maxmin: true,
            resize: true,
            // content: $('#projection_add'),
            content: str,
            cancel: function(index, layero){
                layer.close(index);
                parent.location.href = cancel_url;
                return false;
            }
        });
    });
};
