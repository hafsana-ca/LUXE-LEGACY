from django.urls import path
from Webapp import views

urlpatterns = [
    path('homepage/',views.homepage, name="homepage"),
    path('products/<str:category>/', views.product_list, name='product_list'),
    path('about_page/',views.about_page, name="about_page"),
    path('contact_page/',views.contact_page, name="contact_page"),
    path('contact_form/',views.contact_form, name="contact_form"),
    path('all_products/',views.all_products, name="all_products"),
    path('single_product/<int:pro_id>/',views.single_product, name="single_product"),
    path('single_product_name/<str:product_name>/', views.single_product_name, name='single_product_name'),
    path('filtered_product/<str:cat_name>/',views.filtered_product, name="filtered_product"),
    path('',views.web_login, name="web_login"),
    path('web_register/',views.web_register, name="web_register"),
    path('register_details/',views.register_details, name="register_details"),
    path('UserLogin/',views.UserLogin, name="UserLogin"),
    path('user_logout/',views.user_logout, name="user_logout"),
    path('add_cart/',views.add_cart, name="add_cart"),
    path('cart_page/',views.cart_page, name="cart_page"),
    path('delete_item/<int:dataid>/',views.delete_item, name="delete_item"),
    path('checkout_page/',views.checkout_page, name="checkout_page"),
    path('add_order/',views.add_order, name="add_order"),
    path('payment_page/',views.payment_page, name="payment_page"),
    path('wishlist_page/',views.wishlist_page, name="wishlist_page"),
    path('delete_wishlist/<int:dataid>/',views.delete_wishlist, name="delete_wishlist"),
    path('add_to_wishlist/',views.add_to_wishlist, name="add_to_wishlist"),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),

]