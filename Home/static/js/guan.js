// import get_page from "/Home/static/js/common"

layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var data_url= "/guan/data";
    var pro_system = $("#pro_system").text();

   

    // 添加产品
    $('#add_product').click(function(){
        get_page("/product/add/"+pro_system, "添加产品");
    });

    // 错误提示
    if ($("err-msg").text()){
      layer.msg($("err-msg").text());
    };
    

    // 搜索
    $('.search-btn').click(function(){
        var product_name = $('.search-input').val();
        if (product_name){
            render_table('/product/data/'+ product_name);
        }else{
          // 如果搜索内容为空，返回全部数据
            render_table(data_url);
        }
    })
  
    // 执行一个 table 实例
    render_table(data_url);
    

    // 单元格工具事件
    table.on("tool(test)", function (obj) {
      //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        var data = obj.data, //获得当前行数据
          layEvent = obj.event; //获得 lay-event 对应的值
        if (layEvent === "edit") {
          get_page("/product/edit/"+ pro_system + '/' + data.id, "编辑产品");
        } else if (layEvent === "delete") {
          layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) {
            $.get("/product/delete/" + pro_system + "/"+ data.id, function () {
              obj.del();
              layer.msg("删除成功");
            });
            layer.close(index);
          });
        } else if (layEvent === "detail") {
          layer
        }
    });

    // 渲染表格
    function render_table(url){
      table.render({
        elem: "#demo",
        height: 720,
        url: url, //数据接口（此处为静态数据，仅作演示）
        title: "产品表",
        page: true, //开启分页
        limit: 30,
        limits: [20, 30, 40, 50, 100],
        toolbar: true, //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
        // ,defaultToolbar: ['filter', 'print', 'exports']
        totalRow: false, //开启合计行
        loading: true,
        cols: [
          [
              //表头
              // {type: 'checkbox', fixed: 'left'},
              
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
        ],
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
                  $(iframe).attr('src', '/product/'+pro_system);
                  return false;
              }
          });
      });
    };
  });
  