import re
import json

from django.db.models import Q
from django.forms import ModelForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt

from B.models import  Boms
from B.views.common import choice_map
from Home.models import Product
from Home.views.output import get_keys


def del_data_(data, heads):
    result_data = []
    for h in heads:
        if not h in data.keys():
            result_data.append(0)
        else:
            result_data.append(data[h])
    return result_data

@xframe_options_exempt
def b_bom(req, pro_no, bsystem):
    # data = []
    # bb_keys = list(get_keys(pro_no, bsystem, 'bb'))
    # bc_keys = list(get_keys(pro_no, bsystem, 'bc'))
    # bd_keys = list(get_keys(pro_no, bsystem, 'bd'))
    # be_keys = list(get_keys(pro_no, bsystem, 'be'))
    # heads = {
    #     'bb': bb_keys,
    #     'bc': bc_keys,
    #     'bd': bd_keys,
    #     'be': be_keys,
    # }
    # for bom_obj in Boms.objects.filter(pro_no=pro_no, m_system=choice_map[bsystem]):
    #     product_obj = Product.objects.filter(product_code=bom_obj.product_code).first()
        
    #     data.append({
    #         'product_code': bom_obj.product_code,
    #         'inventory_code': bom_obj.inventory_code,
    #         'product_name': product_obj.product_name,
    #         'product_type': product_obj.product_type,
    #         'unit': product_obj.unit,
    #         'supply': product_obj.supply,
    #         'm_system': bsystem,
    #         'ba': bom_obj.ba,
    #         'bb': del_data_(bom_obj.bb, bb_keys),
    #         'bc': del_data_(bom_obj.bc, bc_keys),
    #         'bd': del_data_(bom_obj.bd, bd_keys),
    #         'be_arrive': del_data_(bom_obj.be_arrive, be_keys),
    #     })

    return render(req, 'b_bom.html', {'pro_no': pro_no, 'bsystem': bsystem})
    # return render(req, 'b_bom1.html', {'pro_no': pro_no, 'bsystem': bsystem, "data": data, 'heads': heads})


def del_data(data):
    sum_data = 0
    for key, value in data.items():
        sum_data += int(value)
    return sum_data


def del_null(data, attr):
    data_object = Product.objects.filter(product_code=data).first()
    if(data_object):
        if (attr == 'type'):
            return data_object.product_type
        elif(attr == 'name'):
            return data_object.product_name
    else:
        return ''





def del_num(d):
    if d:
        return int(d)
    else:
        return 0

def get_bom_data(req, pro_no, bsystem):
    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    condiction = req.GET.get("condiction")

    start = (page - 1) * limit
    end = page * limit
    data = []
    number = [*range(start, end)]
    con1 = Q(pro_no=pro_no) & Q(m_system=choice_map[bsystem])
    data_obj = Boms.objects.filter(con1)
    if condiction:
        con2 = Q(product_code=condiction) | Q(inventory_code=condiction) | Q(bc__has_key=condiction) | Q(bb__has_key=condiction)
        # data_obj = Boms.objects.filter(Q(pro_no=pro_no), Q(m_system=choice_map[bsystem]), Q(bc__has_key=condiction))    
        data_obj = Boms.objects.filter(con1 & con2)    
    for i, x in zip(number, data_obj[start: end]):
        product_obj = Product.objects.filter(product_code=x.product_code).first()
        inventory_code = "000000000"
        if product_obj:
            inventory_code = product_obj.inventory_code
        data.append({
            'num': i + 1,
            'id': x.id,
            'pro_no': str(x.pro_no),
            'product_code': x.product_code,
            'inventory_code': inventory_code,
            'pro_system': x.get_m_system_display(),
            'ba': x.ba,
            'bb': str(x.bb),
            'bb_sum': del_data(x.bb),
            'bb_con': x.bb_con,
            'bb_res': x.bb_res,
            'bc': str(x.bc),
            'bc_sum': del_data(x.bc),
            'bd': str(x.bd),
            'bd_sum': del_data(x.bd),
            'be_arrive': str(x.be_arrive),
            'be_arrive_sum': del_data(x.be_arrive),
            'bs': x.bs,
            'bd2': x.bd2,
            'be_loss': del_data(x.be_arrive) + x.bs + x.bd2 - x.be_install - x.be_res,
            'be_bd': del_data(x.be_arrive) - del_data(x.bd),
            'be_bb': x.be_install - del_data(x.bb),
            'product_type': del_null(x.product_code, 'type'),
            'product_name': del_null(x.product_code, 'name'),
        })
    
    
    content = {
        'code': 0,
        'msg': '',
        'count': data_obj.count(),
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

@xframe_options_exempt
def b_bom_add(req, pro_no, bsystem):
    if req.method == 'GET':
        form = BomForm()
        return render(req, 'b_bom_add.html', {'form': form, 'pro_no': pro_no, 'bsystem': bsystem})
    form = BomForm(data=req.POST)
    if form.is_valid():
        form.save()   
        return redirect('/b/bom/' + pro_no + '/' + bsystem)
    return render(req, 'b_bom_add.html', {'form': form, 'pro_no': pro_no, 'bsystem': bsystem})
    

@xframe_options_exempt
def b_bom_edit(req, pro_no, bsystem, id):
    data = Boms.objects.filter(id=id).first()
    if req.method == 'GET':
        form = BomForm(instance=data)
        return render(req, 'b_bom_edit.html', {'form': form, 'id': id, 'pro_no': pro_no, 'bsystem': bsystem})
    form = BomForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/b/bom/' + pro_no + '/' + bsystem)
    return render(req, 'b_bom_edit.html', {'form': form, 'id': id, 'pro_no': pro_no, 'bsystem': bsystem})
    


def b_bom_delete(req, pro_no, bsystem, id):
    Boms.objects.filter(id=id).delete()
    return redirect('/b/bom/' + pro_no + '/' + bsystem)