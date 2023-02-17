from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Q

from B.models import Projection
from B.views.common import make_header


@xframe_options_exempt
def projection(req):
    return render(req, 'projection.html')

# def projection_depart(req, depart):
#     return render(req, 'projection.html', {'depart': depart})

def get_pro_data(req, depart=None):
    # data = Projection.objects.all()
    limit = int(req.GET.get("limit"))
    page = int(req.GET.get("page"))
    start = (page - 1) * limit
    end = page * limit
    if depart:
        data_obj = Projection.objects.filter(Q(depart_no__startswith=depart) | Q(pro_no=depart))
    else:
        data_obj = Projection.objects.all()
    data = [{
        'id': x.id,
        'pro_no': x.pro_no, 
        'pro_name': x.pro_name,
        'depart_no': x.depart_no, 
        'pm': x.pm,
        'con_year':x.con_year,
        'con_depart':x.con_depart,
        'client_no': x.client_no, 
        'pro_date': x.pro_date, 
        'pro_tec': x.pro_tec, 
        'con_type': x.con_type,
        'logit_status': x.logit_status,
        'pro_mer': x.pro_mer, 
        'client': x.client, 
        'endUser': x.endUser, 
        'pro_area': x.pro_area, 
        'sm': x.sm, 
        'pro_status': x.pro_status,
        'pro_label': x.pro_label
    } for x in data_obj[start:end]]
    content = {
        'code': 0,
        'msg': '',
        'count': data_obj.count(),
        'data': data
    }
    return JsonResponse(content)






class ProjectionForm(ModelForm):
    class Meta:
        model = Projection
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {'class': 'layui-input'}

@xframe_options_exempt
def projection_add(req):
    if req.method == 'GET':
        form = ProjectionForm()
        return render(req, 'projection_add.html', {'form': form})
    form = ProjectionForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect('/projection')
    return render(req, 'projection_add.html', {'form': form})


@xframe_options_exempt
def projection_edit(req, id):
    data = Projection.objects.filter(id=id).first()
    if req.method == 'GET':
        form = ProjectionForm(instance=data)
        return render(req, 'projection_edit.html', {'form': form, 'id': id})
    form = ProjectionForm(data=req.POST, instance=data)
    if form.is_valid():
        form.save()
        return redirect('/projection')
    return render(req, 'projection_edit.html', {'form': form, 'id': id})


def  projection_delete(req, id):
    Projection.objects.filter(id=id).delete()
    return redirect('/projection')

