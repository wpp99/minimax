from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt

from B.models import  BsjXQDD

def get_sjxqd_data(req, pro_no):
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit

    data_obj = BsjXQDD.objects.filter(pro_no=pro_no)
    if pro_no == "all_sjxqd":
        data_obj = BsjXQDD.objects.all()
    data = [{
        'num': x.num, 'id': x.id, "pro_no": str(x.pro_no),
        'sys_code': x.sys_code, 'zgxy': x.zgxy, 'content_zgxy': x.content_zgxy,
        'start_date': x.start_date, 'close_date': x.close_date, 'res_per': x.res_per,
        'audit_level': x.audit_level, 'status': x.status, 'sjxqd_remark': x.sjxqd_remark,
        'xqd0': x.xqd0, 'date_seria': x.date_seria,
        'xqd1': x.xqd1, 
        'xqd2': x.xqd2, 
        'xqd12_remind': x.xqd_remind
    } for x in data_obj[start: end]]
    
    content = {
        'code': 0,
        'msg': '',
        'count': data_obj.count(),
        'data': data
    }
    return JsonResponse(content)


class BsjxqdForm(ModelForm):
    class Meta:
        model = BsjXQDD
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'layui-input'}

@xframe_options_exempt
def b_sjxqd(req, pro_no):
    return render(req, 'b_sjxqd.html', {'pro_no': pro_no})

@xframe_options_exempt
def b_sjxqd_add(req, pro_no):
    if req.method == 'GET':
        form = BsjxqdForm()
        return render(req, 'b_sjxqd_add.html', {'form': form, 'pro_no': pro_no})
    form = BsjxqdForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect('/b/sjxqd/' + pro_no)
    return render(req, 'b_sjxqd_add.html', {'form': form, 'pro_no': pro_no})


@xframe_options_exempt
def b_sjxqd_edit(req, pro_no, id):
    data = BsjXQDD.objects.filter(id=id).first()
    if req.method == 'GET':
        form = BsjxqdForm(instance=data)
        return render(req, 'b_sjxqd_edit.html', {'form': form, 'id': id, 'pro_no': pro_no})
    form = BsjxqdForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/b/sjxqd/' + pro_no)
    return render(req, 'b_sjxqd_add.html', {'form': form, 'pro_no': pro_no})


def b_sjxqd_delete(req, pro_no, id):
    BsjXQDD.objects.filter(id=id).delete()
    return redirect('/b/sjxqd/' + pro_no)
