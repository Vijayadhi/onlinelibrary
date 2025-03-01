from django.urls import path

from backend.views import index, admin_login, user_signup, admin_dashboard, student_reg, ad_change_password, user_login, \
    perfom_logout, manage_books, update_book, delete_book, add_author, manage_author, update_author, delete_author, \
    add_category, manage_category, delete_category, update_category, add_books, issue_new_book, manage_issued_books, \
    update_issued_book, student_detail, update_status, current_st_detail, list_books, profile, user_change_password

urlpatterns = [
    path('', user_login),
    path('user_login', user_login),
    path('student_reg', student_reg),
    path("update_status/<int:pk>/", update_status, name="update_status"),
    path('<int:pk>/detail_student', student_detail),
    path('admin_login', admin_login),
    path('admin_dashboard', admin_dashboard),
    path('user_signup', user_signup),
    path('ad_change_password', ad_change_password),
    path('detail_issued',current_st_detail),
    path('list_books', list_books),
    path('profile', profile),
    path('user_change_password', user_change_password),

    path('index', index),
    path('logout', perfom_logout),

    path('add_author', add_author),
    path('<int:pk>/update_author', update_author),
    path('delete_author/<int:pk>', delete_author),
    path('manage_author', manage_author),

    path('add_category', add_category),
    path('<int:pk>/update_category', update_category),
    path('delete_category/<int:pk>', delete_category),
    path('manage_category', manage_category),

    path('manage_books', manage_books),
    path('add_book', add_books),
    path('<int:pk>/update_book', update_book),
    path('delete_book/<int:pk>', delete_book, name='delete_book'),

    path('issue_book', issue_new_book),
    path('manage_issued', manage_issued_books),
    path('<int:pk>/update_issued', update_issued_book)



]
