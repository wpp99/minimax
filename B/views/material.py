from django.shortcuts import render, HttpResponse


def meterial(req, pro_no):
    return render(req, 'material.html', {'pro_no': pro_no})
