from django.contrib import admin
from toolshare.models import Usercorn, Tool, ToolShed, Request
from django.forms import TextInput, Textarea
from django.db import models
from django import forms
import datetime
"""
Defines the Form used to edit Tools in ToolShare's
Admin site
"""
class toolForm(forms.ModelForm):
    name = forms.CharField(max_length=20)
    owner = forms.IntegerField()
    borrower = forms.IntegerField(required = False)
    description = forms.CharField(label='Post', max_length=250, 
    widget = forms.Textarea(attrs={'rows':'10', 'cols': '30'}), required = False)
    location = forms.CharField(required=False)
    condition = forms.CharField(initial='G')
    registered = forms.DateField(initial=datetime.date.today)
    category = forms.CharField()
    shed = forms.CharField(required = False)
    dueDate = forms.DateField(required = False)
    
    class Meta:
        model = Tool
  
      
"""
Defines the Model used to represent a Users in ToolShare's
Admin site
"""
class userAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('username', ('first_name', 'last_name'),
                           'email','sharezone',('date_joined', 'last_login'),
                           'shed',
                           'is_staff')})
                ]
"""
Defines the Model used to represent a Tool in ToolShare's
Admin site
"""
class toolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name','owner','location','shed',
                           'category','registered', 'borrower', 'dueDate', ('description', 'condition'))})
                 ]
    form = toolForm

"""
Defines the Model used to represent a toolShed in ToolShare's
Admin site
"""
class toolShedAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name', ('manager',), 'sharezone', 'homeShare')})
                 ]
    
class requestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('rtype', 'rstatus', 'toolId', 'ownerId', 'borrowerId', 'message', 'dueDate', 'viewed_borrower', 'viewed_owner', )})
                 ]
                 
#Registers the Admin sections views
admin.site.register(Usercorn, userAdmin)
admin.site.register(Tool, toolAdmin)
admin.site.register(ToolShed, toolShedAdmin)
admin.site.register(Request, requestAdmin)


    #first_name = forms.CharField()
    #last_name = forms.CharField()
#    inlines = [ChoiceInline]
#    list_display = ('username', 'registered')
#    list_filter = ['registered']
#    search_fields = ['username']
#    date_hierarchy = 'registered'
    #formfield_overrides = {
    #    models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    #    models.CharField: {'widget': Textarea(attrs={'rows':30,'cols': 20})}