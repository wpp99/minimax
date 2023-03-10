import {render_table, get_page} from "./common.js"

layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var data_url;
    var pro_system = $("#pro_system").text();
    // var data = {'condiction_name': '', 'pro_system': pro_system}
    var data_1 = {'condiction': '', 'prosystem': pro_system};
    // if(pro_system != 'None'){
    //     data_url = "/product/prosystem/data/" + pro_system; 
    // }else{
    //     data_url = "/product/data_all/all";
    // }

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
        data_1["condiction"] = product_name;
        render_table('/product/data', data_1);
    })
  
    // 执行一个 table 实例
    render_table('/product/data', data_1);
    

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
    function render_table(url, data){
      table.render({
        elem: "#demo",
        height: 720,
        url: url, //数据接口（此处为静态数据，仅作演示）
        where: data,
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
              { field: "product_code", title: "产品编码", width: 180,  align: "center", sort: true },
              { field: "inventory_cod", title: "存货编码", width: 180, sort: true,  align: "center" },
              { field: "product_name", title: "产品名称", width: 180, sort: true,  align: "center" },
              { field: "unit", title: "单位", width: 80,  align: "center" },
              { field: "product_type", title: "型号", width: 180,  align: "center" },
              { field: "pro_system", title: "所属系统", width: 180,  align: "center" },
              { field: "supply", title: "供应商", width: 180,  align: "center" },
              { field: "place_no", title: "座位号", width: 180,  align: "center" },
              { field: "num", title: "现有库存", width: 120, sort: true,  align: "center" },
              { field: "detail", title: "详细描述", width: 120, sort: true,  align: "center" },
              { field: "id", title: "id", width: 80, sort: true,  align: "center" },
              { fixed: "right", title: "操作",  align: "center", toolbar: "#barDemo", width: 180}
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
                  $(iframe).attr('src', '/product/prosystem/'+pro_system);
                  return false;
              }
          });
      });
    };
  });
  