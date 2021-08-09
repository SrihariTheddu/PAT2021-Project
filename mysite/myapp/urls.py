from django.urls import path
from myapp.views import *

app_name = 'myapp'

urlpatterns = [

    #Default Home Page...............................................................................
    path("", HomePageView.as_view(), name="home"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("register/", RegisterUserView.as_view(), name="register"),

    # User Pre defined Operations....................................................................
    path('<int:pk>/dashboard/', StudentDashBoardView.as_view(), name='user-dashboard'),
    path('dashboard/add/', AddOJAccountView.as_view(), name="add-account"),
    path('dashboard/logout/',LogOutView.as_view(), name='logout'),
    path('dashboard/<int:pk>/profile/', UserProfileView.as_view(), name='profile'),
    path('dashboard/<int:pk>/accounts/all/', StudentOJAccountListView.as_view(), name='user-accounts'),
     path('dashboard/int<pk>/account/view/',AccountUpdatePageView.as_view(), name='update-account-view'),
    path('dashboard/account/update/',updateAccount, name='update-account'),


    #Admin pre-determined operations..................................................................
    path('myadmin/home/',AdminDashBoardView.as_view(),name='admin-dashboard'),
    path('myadmin/students/all',AdminStudentsListView.as_view(),name='admin-students'),
    path('myadmin/students/<slug:pk>/profile/',AdminStudentProfileView.as_view(),name='admin-profile-view'),
    path('myadmin/students/<str:pk>/performance/',AdminStudentPerformanceDetailView.as_view(),name='admin-performance-view'),
    path('myadmin/dashboard/<str:pk>/block/',AdminBlockAccountView,name='admin-block-account'),
    path('myadmin/filter/all',DataFilterView,name='data-filter'),
    path('myadmin/students/filter/all',StudentFilterView,name='student-filter'),
    path('myadmin/students/download/<str:host>&&<str:branch>/',DownloadAsCSVFile,name='admin-download-file'),
    path('paginate/filter/',paginateFilterData,name='paginate')

]