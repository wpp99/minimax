import {get_head, header_map} from "./common.js"

layui.use(function(){
    var upload = layui.upload;
    var element = layui.element;
    var layer = layui.layer;
    var table = layui.table;
    var $ = layui.$;
    

    var head;
    var new_data = {};
    var html_str = "";
    var sheet_name =  $(".upload_name option:selected").text();

    // 上传文件
    upload.render({
        
        elem: '#test1' //绑定元素
        ,url: '/upload/del/' +  $("select option:selected").text() //上传接口
        ,accept: 'file'  // 文件类型
        ,size: 5000         // 文件大小
        ,data: {id: 1}
        ,exts: 'xlsx|xls'  // 结合accpet 使用
        ,auto: false     // 选完之后制动上传
        ,bindAction: '.preview'
        ,multiple:false    //
        // ,number:0    // 同时可上传的文件数量 0： 没有限制
        ,drag: true
        ,choose: function(obj){
             //将每次选择的文件追加到文件队列
            var files = obj.pushFile();
            
            //预读本地文件，如果是多文件，则会遍历。(不支持ie8/9)
            obj.preview(function(index, file, result){
                // console.log(index); //得到文件索引
                // console.log(file); //得到文件对象
                // console.log(result); //得到文件base64编码，比如图片
                
            //obj.resetFile(index, file, '123.jpg'); //重命名文件名，layui 2.3.0 开始新增
            
            //这里还可以做一些 append 文件列表 DOM 的操作
            
            //obj.upload(index, file); //对上传失败的单个文件重新上传，一般在某个事件中使用
            //delete files[index]; //删除列表中对应的文件，一般在某个事件中使用
            });
        }

        ,before: function(obj){
            // sheet_name = $(".sheetname-input").val();
            sheet_name = $(".upload_name option:selected").text();
            this.url = '/upload/del/' +  sheet_name;
            layer.load(); //上传loading
            head = get_head(sheet_name);
            
        }

        // ,progress: function(n, elem, res, index){
        //     var percent = n + '%' //获取进度百分比
        //     element.progress('demo', percent); //可配合 layui 进度条元素使用

        //     console.log(elem); //得到当前触发的元素 DOM 对象。可通过该元素定义的属性值匹配到对应的进度条。
        //     console.log(res); //得到 progress 响应信息
        //     console.log(index); //得到当前上传文件的索引，多文件上传时的进度条控制，如：
        //     element.progress('demo-'+ index, n + '%'); //进度条
        // }

        ,done: function(res){
          //上传完毕回调
            if (! res.status){
                render_table(head);
            }
            layer.msg(res.msg);
            layer.closeAll('loading'); //关闭loading
        }

        // ,allDone: function(obj){
        //     console.log(obj.total); //得到总文件数
        //     console.log(obj.successful); //请求成功的文件数
        //     console.log(obj.aborted); //请求失败的文件数
        // }

        
        ,error: function(res){
            
          //请求异常回调
            layer.closeAll('loading'); //关闭loading
        }
    });

    // 渲染表格
    function render_table(head){
        table.render({
            elem: "#demo",
            height: 720,
            url: "/upload/data", 
            title: "upload",
            page: true, 
            limit: 30,
            limits: [20, 30, 50, 100],
            toolbar: "true", 
            // ,defaultToolbar: ['filter', 'print', 'exports']
            totalRow: false, //开启合计行
            loading: true,
            cols: [
              head
            ],
        });
    
    }

    // 单元格工具事件
    table.on("tool(test)", function (obj) {
        //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        var data = obj.data, //获得当前行数据
            layEvent = obj.event; //获得 lay-event 对应的值
    
        if (layEvent === "edit") {
            layui.each(data, function(key, value){
                html_str += `
                <div class="layui-form-item">
                <label class="layui-form-label">${header_map[key]}</label>
                <div class="layui-input-block">
                    <input type="text" name="" value="${value}" autocomplete="off" class="layui-input data-form" data-attr="${key}">
                    </div>
                </div>
                `
            });
            
            html_str += `
                    <div class="layui-form-item ">
                        <div class="layui-input-block">
                            <button class="layui-btn submit">立即提交</button>
                            <button type="reset" class="layui-btn layui-btn-primary reset">重置</button>
                        </div>
                    </div>
                `
            var index = layer.open({
                type: 1,
                title: "编辑",
                skint: "demo-class",
                area: ["400px", "300px"],
                offset: "auto",
                anim: 0, //  弹出动画
                isOutAnim: true,
                maxmin: true,
                resize: true,
                content: html_str,
            });

            $(".submit").click(function(){
                $(".data-form").each(function(){
                    var label = $(this).attr('data-attr');
                    var value = $(this).val();
                    new_data[label] = value;
                });
                layer.close(index);
                obj.update(new_data);
            });
            
            html_str = "";
            new_data = {};
        } else if (layEvent === "delete") {
            layer.confirm("确认删除", { icon: 3, title: "提示" }, function (index) { 
                obj.del();
                layer.msg("删除成功");
                layer.close(index);
            });
        }
        

    });

    // 导入
    $(".load").click(function(){
        var datalist = table.getData("demo");
        var length = Object.keys(datalist).length;
        var location_href = parent.location.pathname;
        sheet_name =  $(".upload_name option:selected").text();
        var loadIndex;
        $.ajax({
            type: "post",
            url: "/upload/load/" + sheet_name,
            data: {
                "data": datalist,
                "length": length,
                "pro_no": location_href.substring(location_href.lastIndexOf('/')+1, location_href.length),
            },
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
    });

    // 导出
    $(".edit_inventory_code").click(function(){
        $.ajax({
            type: 'GET',
            url: "/edit_inventory_code",
            beforeSend: function(){
                loadIndex = layer.load(1, {
                    shade: [0.1, '#fff']
                })
            },
            complete: function () {
                layer.close(loadIndex);
            },
            success: function(res){
                layer.msg(res.msg);
            }
        })
    });

    
   
});