
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt

from B.models import  B1nz


def get_1nz_data(req, pro_no):
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit
    data = []
    number = [*range(start, end)]
    data_obj = B1nz.objects.filter(pro_no=pro_no)
    if pro_no == "all_1nz":
        data_obj = B1nz.objects.all()
    data = [{
        "num": i+1, 'id': x.id, 'pro_no':str(x.pro_no), 'batch_no': x.batch_no, 'description': x.description, 'area': x.area, 'design_date': x.design_date, 
        'deliver_date': x.deliver_date, 'itp_date': x.itp_date, 'port': x.port, 'trans_method': x.get_trans_method_display(), 
        'grossWeight': x.grossWeight, 'volume': x.volume, 'ship_no': x.ship_no, 'wayBill_no': x.wayBill_no, 'arrive_date':x.arrive_date, 
        'con_date': x.con_date, 'nz_date': x.nz_date, 'true_date': x.true_date, 'mx_body': x.mx_body, 'trans_des': x.get_trans_des_display(), 
        'pack_des': x.pack_des, 'three_status':x.get_three_status_display(), 'directShipment':x.get_directShipment_display(), 'trans_to':x.trans_to,
    } for i, x in zip(number, data_obj[start:end])]
    
    content = {
        'code': 0,
        'msg': '',
        'count': data_obj.count(),
        'data': data
    }
    return JsonResponse(content)


def get_batch_data(req, pro_no):
    batch = req.GET.get('batch')
    batchs = [b1nz_obj.batch_no for b1nz_obj in B1nz.objects.filter(pro_no=pro_no)]
    content = {
        'code': 0,
        'msg': ''
    }
    if not batch in batchs:
        content['msg'] = "没有该批次"
        content['code'] = 1
    return JsonResponse(content)        
    

@xframe_options_exempt
def b_1nz(req, pro_no):
    return render(req, 'b_1nz.html', {'pro_no': pro_no})


class B1nzForm(ModelForm):
    class Meta:
        model = B1nz
        fields = ['pro_no', 'batch_no' ,'description', 'area','design_date', 'deliver_date', 'itp_date', 'port', 'trans_method', 'grossWeight',
                'volume', 'ship_no', 'wayBill_no', 'arrive_date', 'con_date', 'nz_date', 'true_date', 'mx_body', 
                'trans_des', 'pack_des', 'three_status', 'directShipment', 'trans_to']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'layui-input'}


@xframe_options_exempt
def b_1nz_add(req, pro_no):
    if req.method == 'GET':
        form = B1nzForm()
        return render(req, 'b_1nz_add.html', {'form': form, 'pro_no': pro_no})
    form = B1nzForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect('/b/1nz/' + pro_no)
    return render(req, 'b_1nz_add.html', {'form': form, 'pro_no': pro_no})


@xframe_options_exempt
def b_1nz_edit(req, pro_no, id):
    data = B1nz.objects.filter(id=id).first()
    if req.method == 'GET':
        form = B1nzForm(instance=data)
        return render(req, 'b_1nz_edit.html', {'form': form, 'id': id, 'pro_no': pro_no})
    form = B1nzForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/b/1nz/' + pro_no)
    return render(req, 'b_1nz_edit.html', {'form': form, 'id': id, 'pro_no': pro_no})


def b_1nz_delete(req, pro_no, id):
    B1nz.objects.filter(id=id).delete()
    return redirect('/b/1nz/' + pro_no)

