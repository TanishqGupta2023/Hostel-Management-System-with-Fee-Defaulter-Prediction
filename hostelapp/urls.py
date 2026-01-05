from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('admin/predict-fee-defaulter/', views.predict_fee_defaulter, name='predict_fee_defaulter'),
    # Room management (admin)
    path('rooms/', views.view_rooms, name='view_rooms'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('assign-room/<int:student_id>/', views.assign_room, name='assign_room'),
   path('custom-admin/view-students/', views.admin_view_fees, name='admin_view_students'),
    path('custom-admin/view-fees/', views.admin_view_fees, name='admin_view_fees'),
    path('auto-assign-rooms/', views.auto_assign_rooms, name='auto_assign_rooms'),
    path('custom-admin/delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    # Student management (admin)
    path('students/', views.view_students, name='view_students'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
   
    # Complaints
    path('complaints/submit/', views.submit_complaint, name='submit_complaint'),
path('complaints/', views.view_complaints, name='view_complaints'),  # for admin or list view
path('complaints/edit/<int:id>/', views.edit_complaint, name='edit_complaint'),
path('complaints/delete/<int:id>/', views.delete_complaint, name='delete_complaint'),
path('complaints/reply/<int:complaint_id>/', views.admin_reply_view, name='admin_reply'),
    path('predict-fee-defaulter/<int:student_id>/', views.predict_fee_defaulter, name='predict_fee_defaulter'),
path('complaints/', views.admin_complaint_list, name='admin_complaint_list'),

    
     path('student/fee-status/', views.student_fee_status, name='fee_status'),
    path('fee/pay/', views.pay_fee, name='pay_fee'),
    path('fee/receipt/', views.download_receipt, name='download_receipt'),
    path('custom-admin/fees/', views.admin_view_all_fees, name='admin_view_all_fees'),
    path('student/mock-pay/', views.mock_pay, name='mock_pay'),
     path('download-receipt/', views.download_receipt, name='download_receipt'),
        path('predict-fee-defaulters/', views.predict_fee_defaulter_list, name='predict_fee_defaulter_list'),
]