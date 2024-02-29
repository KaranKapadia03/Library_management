from django.contrib import admin
from book_management.models import UserID,Books,BookRequest,Sports,men


# Register your models here.

admin.site.register(UserID)
admin.site.register(Books)
admin.site.register(BookRequest)
admin.site.register(Sports)
admin.site.register(men)

