layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var path_name = location.pathname
    var path_arr = path_name.split("/")
    var path_part = path_arr[path_arr.length - 1]
    var header = {
        "1nz": [
            //表头
            // {type: 'checkbox', fixed: 'left'},
            { field: "id", title: "序号", width: 80, sort: true,  align: "center" },
            { field: "pro_no", title: "项目号", width: 180, sort: true,  align: "center" },
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
            // { fixed: "right", title: "操作", width: 120, align: "center", toolbar: "#barDemo"}
        ],
        "sjxqd":[ 
            { field: "pro_no", title: "项目号", width: 120, sort: true },
            { field: "num", title: "序号", width: 60, sort: true },
            { field: "sys_code", title: "系统代码", width: 100 },
            { field: "zgxy", title: "ZGXY", width: 180 },
            { field: "content_zgxy", title: "sjxqd内容", width: 280 },
            { field: "start_date", title: "起始日期", width: 150 },
            { field: "close_date", title: "关闭日期", width: 150 },
            { field: "res_per", title: "责任人", width: 100 },
            { field: "audit_level", title: "审核级别", width: 100 },
            { field: "status", title: "状态", width: 100 },
            { field: "date_seria", title: "时间", width: 120 },
            { field: "sjxqd_remark", title: "sjxqd备注", width: 120 },
            { field: "xqd0", title: "XQD0", width: 60 },
            { field: "xqd1", title: "XQD1", width: 60 },
            { field: "xqd2", title: "XQD2", width: 60 },
            { field: "xqd12_remind", title: "XQD12备注", width: 180 },
            { field: "id", title: "id", width: 80, sort: true },
        ],
        "bom_sum":[
            { field: "id", title: "序号", width: 80, sort: true,  align: "center" },
            { field: "product_code", title: "产品编码", width: 120, sort: true,  align: "center" },
            { field: "inventory_code", title: "存货编码", width: 120, sort: true,  align: "center" },
            { field: "pro_sys_bc", title: "项目号|系统|批次",  width: 1300, sort: true,  align: "center" },
            { field: "submit_date", title: "提交日期",  width: 120, sort: true,  align: "center" },
            
        ],

    }

    var head;
    var data_url = "/bominterface/getData/"+path_part;
    switch(path_part){
        case "ALL1nz":
            head = header["1nz"];
            break
        case "sjXqdall":
            head = header["sjxqd"];
            break
        case "bom_all":
            head = header["bom_sum"];
            break
        default:
            head = [];
    }

    
    render_table(data_url, head)
    // 渲染表格
    function render_table(url, head){
        table.render({
            elem: "#demo",
            height: 720,
            url: url, //数据接口（此处为静态数据，仅作演示）
            title: "订货表",
            page: true, //开启分页
            limit: 30,
            limits: [20, 30, 50, 100],
            toolbar: "true", //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
            // ,defaultToolbar: ['filter', 'print', 'exports']
            totalRow: false, //开启合计行
            loading: true,
            cols: [
                head
            ],
        });
    };

    
    

});
  