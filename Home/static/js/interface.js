import {get_head} from "./common.js"

layui.use(function () {
    // 得到需要的内置组件
    var layer = layui.layer; //弹层
    var table = layui.table; //表格
    var $ = layui.$;
    var path_name = location.pathname
    var path_arr = path_name.split("/")
    var path_part = path_arr[path_arr.length - 1]

    var head = get_head(path_part);
    var data_url = "/bominterface/getData/"+path_part;

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
  