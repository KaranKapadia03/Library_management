from django.urls import path, include
from book_management import views

app_name = "book_management"

urlpatterns = [
    path('', views.BookTableView.as_view(), name='FormsShow'),    
    path('register/', views.UserRegisterCreateView.as_view(), name="UserRegisterCreateView"),
    path('login/',views.user_login,name='login'),
    path("add_book/", views.FormFIll.as_view(), name='FormFIll'),
    path("register/userprofile/",views.profileview.as_view(),name='userprofile'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('FORMEY/',views.FOREMY1.as_view(),name='FORMEY'),
    path('FORMEY2/',views.SportsTableshow.as_view(),name='FORMEY2'),
    #  path('trf/',views.TeacherRequest.as_view(),name='trf'),
    # path('trf/updaterequestview/<pk>',views.UpdateRequestView.as_view(),name='UpdateRequestView'),
    path('book/<pk>/', include([
        path('detail/', views.BookDetailView.as_view(), name='BookDetailView'),
        path('update/', views.Updateview.as_view(), name='UpdateView'),
        path('delete/', views.Deleteview.as_view(), name='DeleteView'),
        path('BookRequested/',views.BookRequested.as_view(),name="BookRequested"),
    ])),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('mul/',views.AddMultipleBookView.as_view(),name='addMultipleBookView'),
    path('TeacherRequestAnswere/',views.TeacherRequestAnswere.as_view(),name='TeacherRequestAnswere'),
    path('FORMEY/',views.FOREMY1.as_view(),name="FORMEY1"),
    path('trf/', include([
        path('', views.TeacherRequest.as_view(), name='trf'),
        path('book_request/<pk>/', views.UpdateRequestView.as_view(), name='updateRequestView'),
        path("StudentRequestAnsweres/",views.StudentRequestAnsweres.as_view(),name='StudentRequestAnsweres'),
    ])),
    # path('<pk>/', views.BookDetailView.as_view(), name='DV'),
    # path('update/<pk>/', views.UpdateView.as_view(), name='UV'),
    # path('delete/<pk>/', views.DeleteView.as_view(), name='DEL'),
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    #  path('logout-redirect/', views.LogoutRedirectView.as_view(), name='logout_redirect'),

]
