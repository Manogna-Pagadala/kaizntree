from django.urls import path
from . import views
urlpatterns = [
path('login/',views.login_view,name='login'),
path('dashboard/', views.dashboard_view, name='dashboard'),
path('registration/', views.registration_view, name='registration'),
path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
path('create_account/', views.create_account, name='create_account'),
path('reset_password/', views.reset_password, name='reset_password'),
path('create_category/', views.create_category, name='create_category'),
path('check_category_name/', views.check_category_name, name='check_category_name'),
path('add_item/',views.add_item,name='add_item'),
path('your_search_view/',views.your_search_view,name='your_search_view'),
path('your_filter_view/',views.your_filter_view,name='your_filter_view'),
]
