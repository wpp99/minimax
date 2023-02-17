function isDigit(data){
    var reg = /^[1-9][0-9]*$/gi;
    if (reg.test(data)){
        return true
    }else{
        return false
    }
}

var laydate = layui.laydate; //日期
lay("input[id$='date']").each(function(){
    laydate.render({
    elem: this,
    })
});


$(".m-add").click(function(){
    var m1_con_obj = $(this).siblings('div').children('.m-1');
    var m1_con = $(this).siblings('div').children('.m-1').val();
    var m2_con_obj = $(this).siblings('div').children('.m-2');
    var m2_con = $(this).siblings('div').children('.m-2').val();
    var con_input = $(this).parent().next('div').children('.m-to').children('textarea');
    if(m1_con && m2_con){
        if (! isDigit(m2_con)){
            alert('只能为数字');
            m2_con_obj.val('');
            return 
        }
        result = JSON.parse(con_input.val())
        result[m1_con] = Number(m2_con)
        con_input.val(JSON.stringify(result))
        
        m1_con_obj.val('');
        m2_con_obj.val('');
    }else{
        alert('不能为空');
    }
});

// 处理选择框
var pro_no = $('.pro_no').attr('id');
var bsystem = $(".bsystem").attr('id');
$("select").find("option[value="+pro_no+"]").attr("selected",true); 
$("select").find("option:contains("+bsystem+")").attr("selected",true); 

// 搜索产品号
$("#material_no_input input").blur(function(){
    var material_no = $(this).val();
    if (material_no){
        $.get('/product_data/'+ material_no, function(res){
            $("#material_type").text(res['data']);
            $("#id_inventory_code").val(res.inventory_code);
        });
    }
});

$("#bc_batch").blur(function(){
    var batch = $(this).val();
    $.ajax({
        type: 'GET',
        url: '/b/1nz/batch/data/'+pro_no,
        data: {batch: batch},
        success: function(res){
            if (res){
                alert(res.msg);
                $("#bc_batch").val('');
            }
        }
    })
});