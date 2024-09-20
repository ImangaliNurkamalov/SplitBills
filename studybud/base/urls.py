from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),  # This line calls the new register view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_group/', views.create_group, name='create_group'),
    path('add_expense/<int:group_id>/', views.add_expense, name='add_expense'),
]



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.home, name="home"),
# ]