from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from account.models import Account



class AccountCreationForm(forms.ModelForm):
    #A form for creating new users. Includes all the required fields, plus a repeated password.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('account_id',)
        # fields = ('account_id', 'identification',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        account = super(AccountCreationForm, self).save(commit=False)
        account.set_password(self.cleaned_data['password1'])
        if commit:
            account.save()
        return account


class AccountChangeForm(forms.ModelForm):
    # A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field.
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('account_id', 'password', 'email', 'identification', 'account_name', 'is_active','is_staff',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value. This is done here, rather than on the field, because the field does not have access to the initial value
        return self.initial['password']





class AccountAdmin (UserAdmin):
    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    # The fields to be used in displaying the User model. These override the definitions on the base UserAdmin that reference specific fields on auth.User.
    list_display = ('account_id','account_name', 'last_login', 'is_active', 'is_staff')
    list_filter = ('account_id', 'account_name',)
    fieldsets = (
        (None, {'fields': ('account_id', 'password', 'email', 'identification', 'account_name', 'coins', 'transaction_charges',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_id','password1', 'password2')}
        ),
    )
    search_fields = ('account_name', 'date_joined', 'last_login',)
    ordering = ('account_id','date_joined')
    readonly_fields = ('account_id', 'coins', 'transaction_charges', 'identification', 'last_login', 'date_joined', 'is_active', 'is_staff',)

    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Account, AccountAdmin)
# ... and, since we're not using Django's built-in permissions, unregister the Group model from admin.
admin.site.unregister(Group)


