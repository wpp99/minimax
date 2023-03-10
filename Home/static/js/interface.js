import {get_head} from "./common.js"

layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var path_name = location.href;
    var path_arr = path_name.split("/")
    var path_part = path_arr[path_arr.length - 1]

    var head = get_head(path_part.split("?")[0]);
    var data_url = "/bominterface/getData/"+path_part;

    render_table(data_url, head);
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

    $("#yy_search_btn").click(function(){
        var condiction = $("#yy_search").val();
        data_url = "/bominterface/getData/"+path_part + "&con="+condiction;
        render_table(data_url, head);
        // $.post('/yy/search', {}, function(str){
        //     layer.open({
        //       type: 1,
        //       content: str,
        //       title: "高级检索",
              
        //     });
        // });
    });

    // $("#Q5").click(function(){
    //     data_url = "/bominterface/getData/"+path_part + "?Q5=true";
    //     render_table(data_url, head);
    // });

    // $("#Q4").click(function(){
    //     data_url = "/bominterface/getData/"+path_part + "?Q4=true";
    //     render_table(data_url, head);
    // });

    // $("#Q7").click(function(){
    //     data_url = "/bominterface/getData/"+path_part + "?Q7=true";
    //     render_table(data_url, head);
    // });

    // $("#Q9_0").click(function(){
    //     data_url = "/bominterface/getData/"+path_part + "?Q90=true";
    //     render_table(data_url, head);
    // });

    // $("#Q9").click(function(){
    //     data_url = "/bominterface/getData/"+path_part + "?Q9=true";
    //     render_table(data_url, head);
    // });

   
});
  