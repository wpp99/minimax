layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var pro_no = document.getElementById("pro_no").innerHTML;
  
    // 绑定添加事件
    $("#add_sjxqd").click(function(){
        get_page("/b/sjxqd/add/" + pro_no, "添加sjxqd")
    });
  
    // 执行一个 table 实例
    table.render({
        elem: "#demo",
        height: 720,
        url: "/b/sjxqd/data/" + pro_no, //数据接口（此处为静态数据，仅作演示）
        title: "sjxqd",
        page: true, //开启分页
        limit: 30,
        limits: [10, 20, 30, 50, 100],
        toolbar: "true", //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
        // ,defaultToolbar: ['filter', 'print', 'exports']
        totalRow: false, //开启合计行
        loading: true,
        cols: [
            [
            //表头
            // {type: 'checkbox', fixed: 'left'},
            
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
            { field: "pro_no", title: "项目号", width: 120, sort: true },
            { field: "id", title: "id", width: 80, sort: true },
            { fixed: "right", title: "操作", width: 150, align: "center", toolbar: "#barDemo", },
            ],
        ],
    });
  
    // 单元格工具事件
    table.on("tool(test)", function (obj) {
      //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
      var data = obj.data, //获得当前行数据
          layEvent = obj.event; //获得 lay-event 对应的值
     
      if (layEvent === "edit") {
            get_page("/b/sjxqd/edit/" + pro_no + "/" + data.id, "编辑sjXQD");
      } else if (layEvent === "delete") {
            layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) {
                $.get("/b/sjxqd/delete/" + pro_no + "/" + data.id, function () {
                    obj.del();
                    layer.msg("删除成功");
                });
                layer.close(index);
            });
      }
    });
    
    // 弹出层
    function get_page(url, title){
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
                content: str,
                cancel: function(index, layero){
                    layer.close(index);
                    iframe = parent.document.getElementsByTagName('iframe');
                    $(iframe).attr('src', '/b/sjxqd/'+pro_no);
                    return false;
                }
            });
          });
    }
  });
  