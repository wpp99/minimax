layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var pro_no = document.getElementById("pro_no").innerHTML;
    var bsystem = $('#bsystem').text()

    var add_url = "/b/bom/add/" + pro_no + '/' + bsystem;
    var edit_url = "/b/bom/edit/" + pro_no + "/" + bsystem + '/';
    var delete_url = "/b/bom/delete/" + pro_no + "/" + bsystem + '/';
    var data_url = "/b/bom/data/" + pro_no + '/' + bsystem;

    // 添加
    $("#add_material").click(function () {
        get_page(add_url, "添加bom");
    });

    // 查询
    
    $("#bom_search").click(function(){
        var text = $("#bom_search_text").val();
        
        render_table(data_url+"?condiction="+text);
        
    });

    // 执行一个 table 实例
    render_table(data_url);
  
  
    // 单元格工具事件
    table.on("tool(test)", function (obj) {
      //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
      var data = obj.data, //获得当前行数据
          layEvent = obj.event; //获得 lay-event 对应的值
     
      if (layEvent === "edit") {
        get_page(edit_url + data.id, "编辑bom");
      } else if (layEvent === "delete") {
        layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) {
          $.get(delete_url + data.id, function () {
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
          $(iframe).attr('src', '/b/bom/'+pro_no+'/'+bsystem);
          return false;
        }
        });
    });
    }

    function render_table(url){
      table.render({
        elem: "#demo",
        height: 720,
        url: url, //数据接口（此处为静态数据，仅作演示）
        title: "bom",
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
                { field: "product_code", title: "产品编码", width: 180, sort: true },
                { field: "inventory_code", title: "存货编码", width: 180, sort: true },
                { field: "product_name", title: "名称", width: 180 },
                { field: "product_type", title: "型号", width: 180, sort: true },
                { field: "pro_system", title: "所属系统", width: 180 },
                { field: "ba", title: "ba", width: 80, sort: true },
                { field: "bb", title: "设计量", width: 80 },
                { field: "bb_sum", title: "设计量合计", width: 80, sort: true },
                { field: "bb_con", title: "合同备件", width: 80, sort: true },
                { field: "bb_res", title: "建造余量", width: 80, sort: true },
                // { field: "bc", title: "采购量", width: 80 , templet: '#temp1'},
                { field: "bc", title: "采购量", width: 80},
                { field: "bc_sum", title: "采购量合计", width: 80, sort: true },
                { field: "bd", title: "发货量", width: 80 },
                { field: "bd_sum", title: "发货量合计", width: 80, sort: true },
                { field: "be_arrive", title: "到货量", width: 80, sort: true },
                { field: "be_arrive_sum", title: "到货量合计", width: 80, sort: true },
                { field: "bs", title: "现场采购量", width: 80, sort: true },
                { field: "bd2", title: "现场补发货", width: 80, sort: true },
                { field: "be_bd", title: "be-bd", width: 80, sort: true },
                { field: "be_loss", title: "损失量", width: 80, sort: true },
                { field: "be_bb", title: "安装设计比较", width: 80, sort: true },
                { field: "id", title: "id", width: 80, sort: true},
                { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
            ],
        ],
    });
    }
    
});
  