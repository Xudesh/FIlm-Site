from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', auth_views.LoginView.as_view(), name='login')
    path('', view=Home, name='home'),
    
    path('<int:day>/<int:month>/<int:year>/<slug:slug>/', view=post_detail, name='post_detail'),
    path('<int:post_id>/share/', view=Post_share, name='post_share'),
    path('<int:post_id>/post_comment/', view=Post_comment, name='post_comment'),
    

    path('register/', view=Register, name='register'),
    path('login/', view=user_login, name='login'),
    path('logout/', view=logout, name='logout'),
    path('edit/', view=edit, name='edit'),

    path('password_change/', view=password_change, name='password_change'),
    path('password_change/done/', view=password_change_done, name='password_change_done'),
    
    # Сброс пароля
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact/', view=contact, name='contact')
]