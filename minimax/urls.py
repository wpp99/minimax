"""minimax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from B.views import b1nz, bsjxqd, boms, material, uploads
from Home.views import index, projection, product, bom_interface, guan, three_meeting, notice, output

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index),
    path('index', index.index),
    path('test', index.test1),

    path('notice', notice.notice),


    path('projection', projection.projection),
    path('projection_data', projection.get_pro_data),
    path('projection_data/<str:depart>', projection.get_pro_data),
    path('projection_add', projection.projection_add),
    path('projection_edit/<int:id>', projection.projection_edit),
    path('projection_delete/<int:id>', projection.projection_delete),

    path('product', product.product),
    path('product/prosystem/<str:pro_system>', product.product),
    path('product/data', product.get_product_data),
    # path('product/data_all/all', product.get_product_data),
    # path('product/data/<str:condiction_name>', product.get_product_data),
    # path('product/prosystem/data/<str:pro_system>', product.get_product_data),
    path('product_data/<str:condiction>', product.get_product_mat),
    path('product/add/<str:pro_system>', product.product_add),
    path('product/edit/<str:pro_system>/<int:id>', product.product_edit),
    path('product/delete/<str:pro_system>/<int:id>', product.product_delete),

    path('threemeeting', three_meeting.three_meeting),
    path('meeting/add', three_meeting.meeting_add),
    path('meeting/edit/<int:id>', three_meeting.meeting_edit),
    path('meeting/delete/<int:id>', three_meeting.meeting_delete),
    # path('meeting/close/<int:id>', three_meeting.meeting_close),
    path('threemeeting/adddata', three_meeting.get_meeting_data),
    path('threemeeting/onpurchase', three_meeting.three_meeting),
    path('threemeeting/extract/purchase_data', three_meeting.extract_meet_data),
    path('threemeeting/purchase/data', three_meeting.get_purchase_data),
    path('threemeeting/thistime', three_meeting.three_meeting),
    path('threemeeting/not_start', three_meeting.three_meeting),
    path('threemeeting/data/<str:his_this>', three_meeting.get_meeting_product_data),
    
    path('bominterface/ALL1nz', bom_interface.bom_interface),
    path('bominterface/sjXqdall', bom_interface.bom_interface),
    path('bominterface/bom_all', bom_interface.bom_sum),
    path('bominterface/bom_submit', bom_interface.bom_submit),
    path('bominterface/yongyou', bom_interface.bom_interface),
    path('bominterface/batch_compart', bom_interface.bom_interface),
    path('bominterface/material_out', bom_interface.bom_interface),
    path('bominterface/getData/<str:interface>', bom_interface.get_interface_data),

    path('guan', guan.guan),
    path('guan/data', guan.get_guan_data),
    path('guan/add', guan.guan_add),
    path('guan/edit/<str:id>', guan.guan_edit),
    path('guan/delete/<str:id>', guan.guan_delete),


    path('projection_b/<str:pro_no>', material.meterial),

    path('b/1nz/data/<str:pro_no>', b1nz.get_1nz_data),
    path('b/1nz/batch/data/<str:pro_no>', b1nz.get_batch_data),
    path('b/1nz/<str:pro_no>', b1nz.b_1nz),
    path('b/1nz/add/<str:pro_no>', b1nz.b_1nz_add),
    path('b/1nz/edit/<str:pro_no>/<int:id>', b1nz.b_1nz_edit),
    path('b/1nz/delete/<str:pro_no>/<int:id>', b1nz.b_1nz_delete),
    
    path('b/sjxqd/data/<str:pro_no>', bsjxqd.get_sjxqd_data),
    path('b/sjxqd/<str:pro_no>', bsjxqd.b_sjxqd),
    path('b/sjxqd/add/<str:pro_no>', bsjxqd.b_sjxqd_add),
    path('b/sjxqd/edit/<str:pro_no>/<int:id>', bsjxqd.b_sjxqd_edit),
    path('b/sjxqd/delete/<str:pro_no>/<int:id>', bsjxqd.b_sjxqd_delete),
   
    path('b/bom/<str:pro_no>/<str:bsystem>', boms.b_bom),
    path('b/bom/data/<str:pro_no>/<str:bsystem>', boms.get_bom_data),
    path('b/bom/add/<str:pro_no>/<str:bsystem>', boms.b_bom_add),
    path('b/bom/edit/<str:pro_no>/<str:bsystem>/<int:id>', boms.b_bom_edit),
    path('b/bom/delete/<str:pro_no>/<str:bsystem>/<int:id>', boms.b_bom_delete),

    path('upload', uploads.upload),
    path('upload/del/<str:sheet_name>', uploads.upload_del),
    path('upload/data', uploads.get_upload_data),
    path('upload/load/<str:mode>', uploads.load_data),

    path('b/output', output.output),
    path('b/load', output.load_btable),
    path('edit_inventory_code', output.add_inventory_code),
]
