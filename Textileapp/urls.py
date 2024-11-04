from django.urls import path
from Textileapp import views

urlpatterns = [
    path("textile_index/",views.textile_index,name="textile_index"),
    path("textile_page/",views.textile_page,name="textile_page"),
    path("add_category/",views.add_category,name="add_category"),
    path("view_category/",views.view_category,name="view_category"),
    path("edit_category/<int:dr_id>/",views.edit_category,name="edit_category"),
    path("delete_category/<int:dr_id>/",views.delete_category,name="delete_category"),
    path("update_category/<int:data_id>/",views.update_category,name="update_category"),

#-----------------------------------------------------------------------------------------------

    path("product_page/",views.product_page,name="product_page"),
    path("add_products/",views.add_products,name="add_products"),
    path("view_product/",views.view_product,name="view_product"),
    path("edit_product/<int:dr_id>/",views.edit_product,name="edit_product"),
    path("delete_product/<int:dr_id>/",views.delete_product,name="delete_product"),
    path("update_product/<int:data_id>/", views.update_product, name="update_product"),

    path("adminlogin/", views.adminlogin, name="adminlogin"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_logout/", views.admin_logout, name="admin_logout"),


    path("contact_pg/", views.contact_pg, name="contact_pg"),
    path("view_contact/", views.view_contact, name="view_contact"),
    path('delete_contact/<int:dr_id>/', views.delete_contact, name="delete_contact"),
    path('view_registration/', views.view_registration, name="view_registration"),
    path('delete_registration/<int:dr_id>/', views.delete_registration, name="delete_registration"),

]