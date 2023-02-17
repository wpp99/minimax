from django.shortcuts import render
from B.models import Projection
from B.views.common import make_header
from django.views.decorators.clickjacking import xframe_options_exempt
from Home.models import Bom_sum_record


def index(req):
    return render(req, 'index.html')


@xframe_options_exempt
def test1(req):
    last_date = Bom_sum_record.objects.order_by("-id").first().submit_date
    data_obj = Bom_sum_record.objects.filter(submit_date = last_date)
    return render(req, "test.html", {"datas": data_obj,})