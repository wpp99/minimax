from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from B.models import Projection, B1nz, Boms
from Home.models import Product
from django.db.models import Q
from B.views import del_data
# Create your views here.
def index(req):
    return render(req, 'index.html')


@xframe_options_exempt
def projection(req):
    return render(req, 'projection.html')

# def projection_depart(req, depart):
#     return render(req, 'projection.html', {'depart': depart})

def get_pro_data(req, depart=None):
    # data = Projection.objects.all()
    if depart:
        data_obj = Projection.objects.filter(depart_no=depart)
    else:
        data_obj = Projection.objects.all()
    data = [{
        'id': x.id,
        'pro_no': x.pro_no, 
        'pro_name': x.pro_name,
        'depart_no': x.depart_no, 
        'client_no': x.client_no, 
        'pro_date': x.pro_date, 
        'pro_tec': x.pro_tec, 
        'pro_mer': x.pro_mer, 
        'client': x.client, 
        'endUser': x.endUser, 
        'pro_area': x.pro_area, 
        'sm': x.sm, 
        'pro_label': x.pro_label
    } for x in data_obj]
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data
    }
    return JsonResponse(content)



class ProjectionForm(ModelForm):
    class Meta:
        model = Projection
        fields = ['pro_no', 'pro_name', 'depart_no', 'client_no', 
                'pro_date', 'pro_tec', 'pro_mer', 'client', 'endUser', 'pro_area', 'sm', 'pro_label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {'class': 'layui-input', 'lay-verify': 'required'}


def projection_add(req):
    if req.method == 'GET':
        form = ProjectionForm()
        return render(req, 'projection_add.html', {'form': form})
    form = ProjectionForm(data=req.POST)
    if form.is_valid():
        form.save()
    return redirect('/projection')


def projection_edit(req, id):
    data = Projection.objects.filter(id=id).first()
    if req.method == 'GET':
        form = ProjectionForm(instance=data)
        return render(req, 'projection_edit.html', {'form': form, 'id': id})
    form = ProjectionForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/projection')


def  projection_delete(req, id):
    Projection.objects.filter(id=id).delete()
    return redirect('/projection')



@xframe_options_exempt
def product(req):
    return render(req, 'product.html')


def get_product_data(req, product_name=None):
    if product_name:
        data_obj = Product.objects.filter(product_name__contains=product_name)
    else: 
        data_obj = Product.objects.all()
    data = [{
        'id': x.id,
        'article_no': x.article_no, 
        'product_name': x.product_name,
        'product_type': x.product_type, 
        'supply': x.supply, 
        'num': x.num, 
    } for x in data_obj]
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data
    }
    return JsonResponse(content)
    

def get_product_mat(req, material_no):
    product_obj = Product.objects.filter(article_no=material_no).first()
    
    if product_obj:
        data = product_obj.product_type
    else:
        data = '无此订货号'
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data
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
            field.widget.attrs = {'class': 'layui-input', 'lay-verify': 'required'}


def product_add(req):
    if req.method == 'GET':
        form = ProductForm()
        return render(req, 'product_add.html', {'form': form})
    form = ProductForm(data=req.POST)
    if form.is_valid():
        form.save()
    return redirect('/product')


def product_edit(req, id):
    data = Product.objects.filter(id=id).first()
    if req.method == 'GET':
        form = ProductForm(instance=data)
        return render(req, 'product_edit.html', {'form': form, 'id': id})
    form = ProductForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/product')


def product_delete(req, id):
    Product.objects.filter(id=id).delete()
    return redirect('/product')

@xframe_options_exempt
def purchase(req):
    return render(req, 'purchase.html')


def get_purchase_data(req):
    # 1筛选本次会审批次
    data = []
    i = 1
    for b1nz_object in B1nz.objects.filter(three_status=6):
        pro_no = b1nz_object.pro_no
        batch = b1nz_object.batch_no
        deliver_date = b1nz_object.deliver_date
        port = b1nz_object.port
        trans_method = b1nz_object.get_trans_method_display()
        directShipment = b1nz_object.get_directShipment_display()
        trans_to = b1nz_object.trans_to
        depart_no = Projection.objects.filter(pro_no=pro_no).first().depart_no
        for boms_object in Boms.objects.filter(Q(bc__contains=batch)):
            material_no = boms_object.material_no
            bc = boms_object.bc
            product_object = Product.objects.filter(article_no = material_no).first()
            product_name = product_object.product_name
            product_type = product_object.product_type
            supply = product_object.supply
            num = product_object.num
            data.append({
                'id': i,
                'pro_no': str(pro_no),
                'batch': batch,
                'deliver_date': deliver_date,
                'port': port,
                'trans_method': trans_method,
                'directShipment': directShipment,
                'trans_to': trans_to,
                'depart_no': depart_no,
                'material_no': material_no,
                'product_name': product_name,
                'product_type': product_type,
                'supply': supply,
                'bc_num': del_data(bc),
                'num': num
            })
            i = i + 1
    content = {
        'code': 0,
        'msg': '',
        'count': len(data),
        'data': data
    }
    return JsonResponse(content)