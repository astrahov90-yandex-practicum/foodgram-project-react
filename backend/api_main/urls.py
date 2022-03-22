from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from users.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('api.urls')),
    path('auth/token/login/', views.obtain_auth_token, name='token'),
    path('auth/token/logout/', LogoutView.as_view(), name='logout'),
]
