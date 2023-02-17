layui.use(function () {
  // 得到需要的内置组件
  var layer = layui.layer; //弹层
  var table = layui.table; //表格
  var $ = layui.$;
  var pro_no = document.getElementById("pro_no").innerHTML;

  // 绑定添加事件
  $("#add_b1nz").click(function(){
    get_page("/b/1nz/add/" + pro_no, "添加1nz");
  });

  // 执行一个 table 实例
  table.render({
      elem: "#demo",
      height: 720,
      url: "/b/1nz/data/" + pro_no, //数据接口（此处为静态数据，仅作演示）
      title: "1nz",
      page: true, //开启分页
      limit: 20,
      limits: [10, 20, 30, 50, 100],
      toolbar: "true", //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
      // ,defaultToolbar: ['filter', 'print', 'exports']
      totalRow: false, //开启合计行
      loading: true,
      cols: [
          [
            //表头
            // {type: 'checkbox', fixed: 'left'},
            { field: "num", title: "序号", width: 80, sort: true },
            { field: "pro_no", title: "项目号", width: 120, sort: true },
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
          get_page("/b/1nz/edit/" + pro_no + "/" + data.id, "编辑1nz");
      } else if (layEvent === "delete") {
          layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) {
              $.get("/b/1nz/delete/" + pro_no + "/" + data.id, function () {
                  obj.del();
                  layer.msg("删除成功");
              });
              layer.close(index);
          });
      }


  });

  


  function b1nzremark(){
      var datalist = table.getData("#demo");
      console.log(datalist);
      datalist.forEach(item => {
          
      });
  }

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
          $(iframe).attr('src', '/b/1nz/'+pro_no);
          return false;
        }
      });
    });
  }

  
});


