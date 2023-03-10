import {render_table, get_page} from "./common.js"


layui.use(function () {
  // 得到需要的内置组件
  var layer = layui.layer; //弹层
  var table = layui.table; //表格
  var $ = layui.$;
  var dropdown = layui.dropdown;
  // var depart = document.getElementById('depart').innerHTML;
  var data_url = "/projection_data";
  // 搜索
  $('#search').click(function(){
    var depart = $("#depart_search").val();
    if (depart){
        render_table('/projection_data/'+depart);
    }else{
      // 如果搜索内容为空，返回全部数据
      render_table(data_url);
    }
  })

  // 添加
  $("#add_pro").click(function(){
    get_page("/projection_add", "添加项目", "/index");
  });
  
  // 执行一个 table 实例
  render_table(data_url, "项目表", "projection");

  // 单元格工具事件
  table.on("tool(test)", function (obj) {
    //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
    var data = obj.data; 
    var layEvent = obj.event; 
    var loadIndex;
    if (layEvent === "btable") {
        // var btable = document.getElementById('projection_b');
        // parent.location.href = "/projection_b/" + data.pro_no;
        window.open("/projection_b/" + data.pro_no);
    }else if (layEvent === "more"){
        dropdown.render({
            elem: this //触发事件的 DOM 对象
            ,show: true //外部事件触发即显示
            ,data: [
              {
                title: '编辑'
                ,id: 'edit'
              },
              {
                title: '删除'
                ,id: 'del'
              },
              {
                  title: '导入B表',
                  id: 'load_b'
              },
              {
                title: '导出B表'
                , id: 'output'
              }
            ]
            ,click: function(menudata){
              if(menudata.id === 'del'){
                  layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) {
                    $.get("/projection_delete/" + data.id, function () {
                      obj.del();
                      layer.msg("删除成功");
                    });
                    layer.close(index);
                  });
              } else if(menudata.id === 'edit'){
                  get_page("/projection_edit/"+ data.id, "编辑项目", "/index");
              }else if(menudata.id === 'output'){
                  
                  $.ajax({
                      type: "GET",
                      url: "/b/output",
                      data: {
                          pro_no: data.pro_no,
                      },
                      beforeSend: function(){
                          loadIndex = layer.load(1, {
                              shade: [0.1, "#fff"]
                          });
                      },
                      complete: function(){
                          layer.close(loadIndex);
                      },
                      success: function(result, state, xhr){
                          layer.msg("导出成功");
                          window.location.href = '/b/output?pro_no='+ data.pro_no;
                      },
                  })
              }else if(menudata.id === 'load_b'){
                  $.ajax({
                      type: 'GET',
                      url: '/b/load',
                      data: {pro_no: data.pro_no},
                      beforeSend: function(){
                          loadIndex = layer.load(1, {
                              shade: [0.1, "#fff"]
                          });
                      },
                      complete: function(){
                          layer.close(loadIndex);
                      },
                      success: function(res){
                          layer.msg(res.msg);
                      }
                  })
              }
            }
            ,align: 'right' //右对齐弹出（v2.6.8 新增）
            ,style: 'box-shadow: 1px 1px 10px rgb(0 0 0 / 12%);' //设置额外样式
        })
    }
  });

});


