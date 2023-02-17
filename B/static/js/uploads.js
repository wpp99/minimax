layui.use(function(){
    var upload = layui.upload;
    var element = layui.element;
    var layer = layui.layer;
    var table = layui.table;
    var $ = layui.$;
    var header_map = {
        "id": "序号",
        "batch_no": "批次号", 
        "description": "货物描述", 
        "area": "区域", 
        "design_date": "设计输入时间", 
        "deliver_date": "计划交货日期", 
        "itp_date": "Itp放行日期", 
        "port": "起运港", 
        "trans_method": "运输方式",
        "grossWeight": "毛重", 
        "volume": "体积", 
        "ship_no": "船名船次",
        "wayBill_no": "运单号",
        "arrive_date": "预计到港时间",
        "con_date": "定发运日期",
        "nz_date": "1nz发运日期",
        "true_date": "实际发货日期",
        "mx_body": "MX合同主体",
        "trans_des": "旅行说明",
        "pack_des": "单独包装说明",
        "three_status": "三部会审状态",
        "directShipment": "直运至",
        "trans_to": "发运地",
        "sys_code": "系统代码", 
        "zgxy": "ZGXY", 
        "content_zgxy": "sjxqd内容", 
        "start_date": "起始日期", 
        "close_date": "关闭日期", 
        "res_per": "责任人", 
        "audit_level": "审核级别", 
        "status": "状态", 
        "date_seria": "时间", 
        "sjxqd_remark": "sjxqd备注", 
        "xqd0": "XQD0", 
        "xqd1": "XQD1", 
        "xqd2": "XQD2", 
        "xqd_remind": "XQD12备注", 
        "material_no": "产品编码", 
        "material_name": "名称", 
        "material_type": "型号", 
        "m_system": "所属系统", 
        "ba": "ba",
        "bb": "设计量",
        "bb_sum": "设计量合计",
        "bb_con": "合同备件",
        "bb_res": "建造余量",
        "bc": "采购量",
        "bc_sum": "采购量合计",
        "bd": "发货量",
        "bd_sum": "发货量合计",
        "be_sum": "安装量量合计",
        "be_loss": "损失量",
        "be_bb": "安装设计比较",
    }

    var headers = {
        "1nz": [
            { field: "id", title: "序号", width: 80, sort: true },
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
            { fixed: "right", title: "操作", width: 150, align: "center", toolbar: "#barDemo", },
        ],
        "sjxqd": [
            { field: "id", title: "序号", width: 80, sort: true },
            { field: "sys_code", title: "系统代码", width: 100 },
            { field: "zgxy", title: "ZGXY", width: 180 },
            { field: "content_zgxy", title: "sjxqd内容", width: 280 },
            { field: "start_date", title: "起始日期", width: 180 },
            { field: "close_date", title: "关闭日期", width: 180 },
            { field: "res_per", title: "责任人", width: 180 },
            { field: "audit_level", title: "审核级别", width: 120 },
            { field: "status", title: "状态", width: 120 },
            { field: "date_seria", title: "时间", width: 120 },
            { field: "sjxqd_remark", title: "sjxqd备注", width: 120 },
            { field: "xqd0", title: "XQD0", width: 180 },
            { field: "xqd1", title: "XQD1", width: 180 },
            { field: "xqd2", title: "XQD2", width: 180 },
            { field: "xqd12_remind", title: "XQD12备注", width: 180 },
            { fixed: "right", title: "操作", width: 150, align: "center", toolbar: "#barDemo", },
        ],
        "boms": [
            { field: "id", title: "序号", width: 80, sort: true },
            { field: "material_no", title: "产品编码", width: 180, sort: true },
            { field: "material_name", title: "名称", width: 180 },
            { field: "material_type", title: "型号", width: 180, sort: true },
            { field: "m_system", title: "所属系统", width: 180 },
            { field: "ba", title: "ba", width: 80, sort: true },
            { field: "bb", title: "设计量", width: 80 },
            { field: "bb_sum", title: "设计量合计", width: 80, sort: true },
            { field: "bb_con", title: "合同备件", width: 80, sort: true },
            { field: "bb_res", title: "建造余量", width: 80, sort: true },
            { field: "bc", title: "采购量", width: 80 },
            { field: "bc_sum", title: "采购量合计", width: 80, sort: true },
            { field: "bd", title: "发货量", width: 80 },
            { field: "bd_sum", title: "发货量合计", width: 80, sort: true },
            { field: "be_arrive", title: "到货量", width: 80, sort: true },
            { field: "be_arrive_sum", title: "到货量合计", width: 80, sort: true },
            { field: "bs", title: "现场采购量", width: 80, sort: true },
            { field: "bd2", title: "现场补发货", width: 80, sort: true },
            { field: "be_res", title: "剩余总量", width: 80, sort: true },
            { field: "be_bd", title: "be-bd", width: 80, sort: true },
            { field: "be_loss", title: "损失量", width: 80, sort: true },
            { field: "be_bb", title: "安装设计比较", width: 80, sort: true },
            { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
        ],
        "product":[
            { field: "id", title: "序号", width: 80, sort: true },
            { field: "product_code", title: "产品编码", width: 180, sort: true },
            { field: "material_no", title: "存货编码", width: 180, sort: true },
            { field: "material_name", title: "名称", width: 180 },
            { field: "material_type", title: "型号", width: 180, sort: true },
            { field: "m_system", title: "所属系统", width: 180 },
            { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
        ],
        "projection":[
            { field: "id", title: "序号", width: 80, sort: true },
            { field: "con_year", title: "合同年份", width: 80, sort: true },
            { field: "con_depart", title: "合同部门位置", width: 80, sort: true },
            { field: "pro_no", title: "合同号", width: 180, sort: true },
            { field: "pro_name", title: "项目名称", width: 200, sort: true },
            { field: "depart_no", title: "部门编码", width: 80, sort: true },
            { field: "pm", title: "项目PM", width: 180, sort: true },
            { field: "pro_mer", title: "商务", width: 180, sort: true },
            { field: "con_type", title: "项目类型", width: 180, sort: true },
            { field: "pro_label", title: "合同标签", width: 180, sort: true },
            { field: "pro_date", title: "LX日期", width: 180, sort: true },
            { field: "logit_status", title: "物流是否关闭", width: 180, sort: true },
            { field: "pro_status", title: "项目状态", width: 180, sort: true },
            { fixed: "right", title: "操作", width: 180, align: "center", toolbar: "#barDemo"},
        ],
        "guan":[
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
        ]
    };
    
    var head;
    var new_data = {};
    var html_str = "";
    var sheet_name =  $("select option:selected").text();

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
            sheet_name = $("select option:selected").text();
            this.url = '/upload/del/' +  sheet_name;
            layer.load(); //上传loading
            // if (sheet_name === '1nz'){
            //     head = headers['1nz'];
            // }else if(sheet_name == 'sjXQD'){
            //     head = headers['sjxqd'];
            // }else if(sheet_name == 'product'){
            //     head = headers['product'];
            // }else{
                
            // }
            switch(sheet_name){
                case "1nz":
                    head = headers['1nz'];
                    break;
                case "sjXQD":
                    head = headers['sjxqd'];
                    break;
                case "product":
                    head = headers['product'];
                    break;
                case "projection":
                    head = headers['projection'];
                    break;
                case "guan":
                    head = headers["guan"];
                    break
                default:
                    head = headers['boms'];
            }
            // $(".sheetname-input").val('');
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
            url: "/upload/data", //数据接口（此处为静态数据，仅作演示）
            title: "upload",
            page: false, //开启分页
            toolbar: "true", //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
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
        sheet_name =  $("select option:selected").text();
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