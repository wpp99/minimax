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
    get_page("/projection_add", "添加项目");
  });
  
  // 执行一个 table 实例
  render_table(data_url);

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
                  get_page("/projection_edit/"+ data.id, "编辑项目");
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
                          // // console.log(xhr);
                          // let fileName = xhr.getResponseHeader('Content-Disposition').split(';')[1].split('=')[1].replace(/\"/g, '')
                          // let type = xhr.getResponseHeader("content-type");

                          // //结果数据类型处理
			                    // let blob = new Blob([result], { type: type });

                          // let link = document.createElement("a");
                          // link.download = fileName;
				                  // link.style.display = "none"
				                  // link.href = URL.createObjectURL(blob);

				                  // document.body.appendChild(link);
				                  // link.click(); //执行下载
				                  // URL.revokeObjectURL(link.href);//释放url
				                  // document.body.removeChild(link);//释放标签


                          // u = document.createElement('a');
                          // u.href = result;
                          // document.body.append(u);
                          // u.click();
                          // document.body.remove(u);
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

  // 渲染表格
  function render_table(url){
    table.render({
      elem: "#demo",
      height: 720,
      url: url, //数据接口（此处为静态数据，仅作演示）
      title: "项目表",
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
      cols: [
        [
          //表头
          // {type: 'checkbox', fixed: 'left'},
          { field: "id", title: "序号", width: 80, sort: true },
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
          { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo", },
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
          parent.location.href = '/index';
          return false;
        }
      });
    });
  };

});


