import re

from django.db.models import Q
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from B.models import  B1nz, Boms, BsjXQDD
from Home.models import Product


def meterial(req, pro_no):
    return render(req, 'material.html', {'pro_no': pro_no})


def get_1nz_data(req, pro_no):
    data = [{
        'id': x.id, 'pro_no':str(x.pro_no), 'batch_no': x.batch_no, 'description': x.description, 'area': x.area, 'design_date': x.design_date, 
        'deliver_date': x.deliver_date, 'itp_date': x.itp_date, 'port': x.port, 'trans_method': x.get_trans_method_display(), 
        'grossWeight': x.grossWeight, 'volume': x.volume, 'ship_no': x.ship_no, 'wayBill_no': x.wayBill_no, 'arrive_date':x.arrive_date, 
        'con_date': x.con_date, 'nz_date': x.nz_date, 'true_date': x.true_date, 'mx_body': x.mx_body, 'trans_des': x.get_trans_des_display(), 
        'pack_des': x.pack_des, 'three_status':x.get_three_status_display(), 'directShipment':x.get_directShipment_display(), 'trans_to':x.trans_to,
    } for x in B1nz.objects.filter(pro_no=pro_no)]
    
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data
    }
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


def b_1nz_add(req, pro_no):
    if req.method == 'GET':
        form = B1nzForm()
        return render(req, 'b_1nz_add.html', {'form': form, 'pro_no': pro_no})
    form = B1nzForm(data=req.POST)
    if form.is_valid():
        form.save()
    return redirect('/b/1nz/' + pro_no)


def b_1nz_edit(req, pro_no, id):
    data = B1nz.objects.filter(id=id).first()
    if req.method == 'GET':
        form = B1nzForm(instance=data)
        return render(req, 'b_1nz_edit.html', {'form': form, 'id': id, 'pro_no': pro_no})
    form = B1nzForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/b/1nz/' + pro_no)


def b_1nz_delete(req, pro_no, id):
    B1nz.objects.filter(id=id).delete()
    return redirect('/b/1nz/' + pro_no)


def get_sjxqd_data(req, pro_no):
    data = [{
        'id': x.id,  'num_1': x.num_1, 'num_2': x.num_2,
        'sys_code': x.sys_code, 'zgxy': x.zgxy, 'content_zgxy': x.content_zgxy,
        'start_date': x.start_date, 'close_date': x.close_date, 'res_per': x.res_per,
        'audit_level': x.audit_level, 'status': x.status, 'xqd': x.xqd, 'xqd_remind': x.xqd_remind
    } for x in BsjXQDD.objects.filter(pro_no=pro_no)]
    
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
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


def b_sjxqd_add(req, pro_no):
    if req.method == 'GET':
        form = BsjxqdForm()
        return render(req, 'b_sjxqd_add.html', {'form': form, 'pro_no': pro_no})
    form = BsjxqdForm(data=req.POST)
    if form.is_valid():
        form.save()
    return redirect('/b/sjxqd/' + pro_no)


def b_sjxqd_edit(req, pro_no, id):
    data = BsjXQDD.objects.filter(id=id).first()
    if req.method == 'GET':
        form = BsjxqdForm(instance=data)
        return render(req, 'b_sjxqd_edit.html', {'form': form, 'id': id, 'pro_no': pro_no})
    form = BsjxqdForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/b/sjxqd/' + pro_no)


def b_sjxqd_delete(req, pro_no, id):
    BsjXQDD.objects.filter(id=id).delete()
    return redirect('/b/sjxqd/' + pro_no)


@xframe_options_exempt
def b_bom(req, pro_no, bsystem):
    return render(req, 'b_bom.html', {'pro_no': pro_no, 'bsystem': bsystem})


def del_data(data):
    sum_data = 0
    if(data):
        for i in re.findall('\((\d{1,})\);?', str(data)):
            sum_data += int(i)
    return sum_data


def del_null(data, attr):
    data_object = Product.objects.filter(article_no=data).first()
    if(data_object):
        if (attr == 'type'):
            return data_object.product_type
        elif(attr == 'name'):
            return data_object.product_name
    else:
        return ''


m_system_dict = {
        'SGY01': 1,
        'SGY02': 2,
        'SGY03': 3,
        'SGCE': 4,
        'WNozzle': 5,
        'SGF': 6,
        'SGK10': 7,
        'SGK30': 8,
        'SGK40': 9,
        'SGJ10': 10,
        'SGJ20': 11,
        'GASNOzzle': 12,
        'SGA10': 13,
        'SGA20': 14,
        'SGA30': 15,
        'SGP': 16,
        'WaterPiping': 17,
        'GasPiping': 18,
        'Supports': 19,
        'InstAcc': 20,
}


def get_bom_data(req, pro_no, bsystem):
    data = [{
        'id': x.id,
        'pro_no': str(x.pro_no),
        'material_no': x.material_no,
        'm_system': x.get_m_system_display(),
        'ba': x.ba,
        'bb': x.bb,
        'bb_sum': del_data(x.bb),
        'bc': x.bc,
        'bc_sum': del_data(x.bc),
        'bd': x.bd,
        'bd_sum': del_data(x.bd),
        'material_type': del_null(x.material_no, 'type'),
        'material_name': del_null(x.material_no, 'name'),
    } for x in Boms.objects.filter(Q(pro_no=pro_no), Q(m_system=m_system_dict[bsystem]))]
    
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data
    }
    return JsonResponse(content)


class BomForm(ModelForm):
    class Meta:
        model = Boms
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'layui-input'}


def b_bom_add(req, pro_no, bsystem):
    if req.method == 'GET':
        form = BomForm()
        return render(req, 'b_bom_add.html', {'form': form, 'pro_no': pro_no, 'bsystem': bsystem})
    form = BomForm(data=req.POST)
    if form.is_valid():
        form.save()   
    else: 
        print(form.errors)
    return redirect('/b/bom/' + pro_no + '/' + bsystem)


def b_bom_edit(req, pro_no, bsystem, id):
    data = Boms.objects.filter(id=id).first()
    if req.method == 'GET':
        form = BomForm(instance=data)
        return render(req, 'b_bom_edit.html', {'form': form, 'id': id, 'pro_no': pro_no, 'bsystem': bsystem})
    form = BomForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/b/bom/' + pro_no + '/' + bsystem)


def b_bom_delete(req, pro_no, bsystem, id):
    Boms.objects.filter(id=id).delete()
    return redirect('/b/bom/' + pro_no + '/' + bsystem)