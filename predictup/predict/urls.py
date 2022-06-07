from django.contrib import admin
from django.urls import path, include
from .import views,yahoo2
from .import home_mpl_chart
urlpatterns = [
   path('',views.home_Page,name='home'),
   # path('dashboard/',views.dashboard, name='dashboard'),
   path('signup/', views.sign_up, name='signup'),
   path('login/', views.user_login, name='user_login'),
   path('profile/', views.user_profile, name='profile'),
   path('logout/', views.user_logout, name='logout'),
   path('changepass/', views.user_change_pass, name='changepass'),
   # path('index', views.Index.as_view(), name='index'),
   path('home_mpl/',home_mpl_chart.home_mpl,name='home_mpl'),

   path('chart_plot/',home_mpl_chart.chart_plot,name='chart_plot'),
   path('dashboard2/<my_name>/',yahoo2.dashboard, name = 'dashboard2'),
   # path('dash/', yahoo2.dash,name='dash'),


]
