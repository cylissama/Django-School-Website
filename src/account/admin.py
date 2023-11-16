from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import *

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email', 'username')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

#registers the app into the admin site for easy use
admin.site.register(Account, AccountAdmin)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(LetterGrades)
