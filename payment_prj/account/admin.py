from django.contrib import admin
from account.models import Account, KYC
from userauths.models import User
from import_export.admin import ImportExportModelAdmin


@admin.register(Account)
class AccountAdminModel(ImportExportModelAdmin):
    list_editable = ['account_status', 'account_balance']
    list_display = ['user', 'account_number', 'account_status', 'account_balance']
    list_filter = ['account_status']


@admin.register(KYC)
class KYCAdminModel(ImportExportModelAdmin):
    search_fields = ['full_name']
    list_display = ['user', 'full_name']

