from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from Home.models import Product, Inventory
from B.views.common import bom_map_inverse, bom_map



@xframe_options_exempt
def product(req, pro_system=None):
    """渲染product页面"""
    return render(req, 'product.html', {"pro_system": pro_system})



def get_product_data(req):
    """获取产品数据"""
    condiction_name = req.GET.get("condiction")
    pro_system = req.GET.get("prosystem")

    page = int(req.GET.get('page'))
    limit = int(req.GET.get('limit'))
    start = (page - 1) * limit
    end = page * limit 
    numbers = [*range(start, end)]
    data = []
    con2 = Q(product_name__contains=condiction_name) | Q(product_code=condiction_name) | Q(inventory_code__startswith=condiction_name)
    if pro_system != 'all':
        con1 = Q(pro_system=bom_map[pro_system])
        data_obj = Product.objects.filter(con1)
        if condiction_name:
            data_obj = Product.objects.filter(con1, con2)
    else: 
        
        data_obj = Product.objects.all()
        if condiction_name:
            data_obj = Product.objects.filter(con2)
    for i, x in  zip(numbers, data_obj[start:end]):
        invetory_obj = Inventory.objects.filter(product_code=x.product_code).first()
        data.append({
            'no': i + 1,
            'id': x.id,
            'product_code': x.product_code, 
            'inventory_cod': x.inventory_code, 
            'product_name': x.product_name,
            'unit': x.unit,
            'product_type': x.product_type, 
            'pro_system': x.get_pro_system_display(), 
            'supply': x.supply, 
            'place_no': x.place_no, 
            'num': invetory_obj.inven_now_num if invetory_obj else 0, 
            'detail': x.detail, 
        })
    content = {
        'code': 0,
        'msg': '',
        'count': data_obj.count(),
        'data': data
    }
    return JsonResponse(content)
    

def get_product_mat(req, condiction):
    """根据产品号返回名称"""
    product_obj = Product.objects.filter(Q(product_code=condiction) | Q(inventory_code=condiction)).first()
    
    if product_obj:
        data = product_obj.product_type
        inventory_code = product_obj.inventory_code
    else:
        data = '无此产品编码'
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data,
        'inventory_code': inventory_code
    }
    return JsonResponse(content)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {'class': 'layui-input'}


@xframe_options_exempt
def product_add(req, pro_system):
    if req.method == 'GET':
        form = ProductForm()
        last_id = Product.objects.all().order_by("-id").first().id
        product_code = 'p' + str(last_id+3).rjust(9, '0')
        return render(req, 'product_add.html', {'form': form, "pro_system": pro_system, "product_code": product_code})
    condiction = Product.objects.filter(Q(product_code=req.POST['product_code']) | Q(inventory_code__startswith=req.POST['inventory_code']))
    form = ProductForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect('/product/prosystem/'+ pro_system)
    return render(req, 'product_add.html', {'form': form, "pro_system": pro_system, "product_code": product_code})


@xframe_options_exempt
def product_edit(req, pro_system, id):
    data = Product.objects.filter(id=id).first()
    if req.method == 'GET':
        form = ProductForm(instance=data)
        return render(req, 'product_edit.html', {'form': form, 'id': id, "pro_system": pro_system})
    form = ProductForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/product/prosystem/'+ pro_system)
    return render(req, 'product_edit.html', {'form': form, 'id': id, "pro_system": pro_system})


def product_delete(req, pro_system, id):
    Product.objects.filter(id=id).delete()
    return redirect('/product/prosystem/'+ pro_system)



