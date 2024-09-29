from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomSigninView, SignUpView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signin/', CustomSigninView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete')
]