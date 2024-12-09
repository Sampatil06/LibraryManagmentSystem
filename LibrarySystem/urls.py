from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from library.views import home  # Import home view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),  # Include app-level URLs
    path('', home, name='home'),  # Root URL points to home view
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Login URL
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
]
