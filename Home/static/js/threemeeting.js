layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var path_name = location.pathname
    var path_arr = path_name.split("/")
    var path_part = path_arr[path_arr.length - 1]
    var headers = {
        "add": [
            { field: "no", title: "序号", width: 80, sort: true,  align: "center" },
            { field: "depart", title: "部门", width: 180, sort: true,  align: "center" },
            { field: "pro_no", title: "项目号", width: 180, sort: true,  align: "center" },
            { field: "batch", title: "批次号", width: 150, sort: true,  align: "center" },
            { field: "participants", title: "参加人员", width: 150, sort: true,  align: "center" },
            { field: "meet_date", title: "日期", width: 150, sort: true,  align: "center" },
            { field: "status", title: "状态", width: 150, sort: true,  align: "center" },
            { field: "remark", title: "备注", width: 150, sort: true,  align: "center" },
            { field: "meet_sign_filepath", title: "签字文件路径", width: 200, sort: true,  align: "center", templet: '#temp1' },
            { field: "id", title: "id", width: 80, sort: true,  align: "center" },
            { fixed: "right", title: "操作", width: 200, align: "center", toolbar: "#barDemo"}
        ],
        "both": [
            //表头
            // {type: 'checkbox', fixed: 'left'},
            { field: "no", title: "序号", width: 80, sort: true,  align: "center" },
            { field: "pro_no", title: "项目号", width: 180, sort: true,  align: "center" },
            { field: "batch", title: "批次号", width: 100, sort: true,  align: "center" },
            { field: "deliver_date", title: "交货日期", width: 120, sort: true,  align: "center" },
            { field: "port", title: "起运港", width: 100, sort: true,  align: "center" },
            { field: "trans_method", title: "运输方式", width: 100, sort: true,  align: "center" },
            { field: "directShipment", title: "直运至", width: 100, sort: true,  align: "center" },
            { field: "trans_to", title: "发货地", width: 100, sort: true,  align: "center" },
            { field: "depart_no", title: "部门编码", width: 100, sort: true,  align: "center" },
            { field: "product_code", title: "产品编码", width: 180,  align: "center", sort: true },
            { field: "product_name", title: "名称", width: 180, sort: true,  align: "center" },
            { field: "product_type", title: "型号", width: 180,  align: "center" },
            { field: "supply", title: "供应商", width: 180,  align: "center" },
            { field: "bc_num", title: "采购量", width: 100,  sort: true, align: "center" },
            { field: "inventory_num", title: "现有库存", width: 120, sort: true,  align: "center" },
            // { field: "loss_num", title: "缺货量", width: 120, sort: true,  align: "center" },
            // { fixed: "right", title: "操作", width: 120, align: "center", toolbar: "#barDemo"}
        ],
    }

    if (path_name === "/threemeeting"){
        render_table("/threemeeting/adddata", headers["add"]);
    }else if (path_name === "/threemeeting/onpurchase"){
        render_table("/threemeeting/purchase/data", headers["both"]);
    }else{
        render_table("/threemeeting/data/"+path_part, headers["both"]);
    }
    
    // 申请
    $(".apply").click(function(){
        get_page("/meeting/add", "添加会审");
    });

   
    

    // 设置threemeet_code 的默认值
    // 单元格工具事件
    table.on("tool(test)", function (obj) {
        //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        var data = obj.data, //获得当前行数据
            layEvent = obj.event; //获得 lay-event 对应的值
        if (layEvent === "edit") {
            get_page("/meeting/edit/" + data.id, "编辑");
        } else if (layEvent === "delete") {
            layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) {
                $.get("/meeting/delete/" + data.id, function () {
                    obj.del();
                    layer.msg("删除成功");
                });
                layer.close(index);
            });
        } else if (layEvent === "close") {
            get_page("/meeting/close/" + data.id, "关闭");
        }
    });
    
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
            cols: [head],
        });
    };

    // 弹出层
    function get_page(url, title){
        $.get(url, function (str) {
            layer.open({
                type: 1,
                title: title,
                skint: "demo-class",
                area: ["500px", "300px"],
                offset: "auto",
                anim: 0, //  弹出动画
                isOutAnim: true,
                maxmin: true,
                resize: true,
                closeBtn: 1,
                // content: $('#projection_add'),
                content: str,
                cancel: function(index, layero){
                    layer.close(index);
                    iframe = parent.document.getElementsByTagName('iframe');
                    $(iframe).attr('src', '/threemeeting');
                    return false;
                }
            });
        });
    };
    

});
  