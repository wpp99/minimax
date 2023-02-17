from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def notice(req):
    return render(req, "notice.html")