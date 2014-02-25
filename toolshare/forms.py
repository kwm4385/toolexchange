from django import forms
from django.forms import ModelForm
from toolshare.models import Tool, ToolShed, Request
from django.core.validators import MinValueValidator, MaxValueValidator

"""
Defines the Form is used by Registration in the ToolShare
System
"""
class RegisterForm(forms.Form):
    firstname = forms.CharField(label="First name", max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    lastname = forms.CharField(label="Last name", max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    zip = forms.IntegerField(validators=[MinValueValidator(10000),MaxValueValidator(99999)],label="Zip code", widget=forms.TextInput(attrs={'class' : 'form-control'}))
                             
"""
Defines the Form that is used to Add a Tool into the ToolShare
System
"""
class ToolForm(ModelForm):
    class Meta:
        model = Tool
        fields = ('name', 'description', 'condition', 'category', 'image',)
    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = "form-control"
        self.fields['description'].widget.attrs['class'] = "form-control"
        self.fields['condition'].widget.attrs['class'] = "form-control"
        self.fields['category'].widget.attrs['class'] = "form-control"
        
"""
Defines the Form that is used to add a Shed into the ToolShare
System
"""
class ShedForm(ModelForm):
    class Meta:
        model=ToolShed
        fields=('name','location','homeShare')
    def __init__(self,*args, **kwargs):
        super(ShedForm, self).__init__(*args,**kwargs)
        self.fields['name'].widget.attrs['class'] ="form-control"
        self.fields['location'].widget.attrs['class'] ="form-control"
#        self.fields['homeShare'].widget.attrs['class'] ="form-control"
        
"""
Defines the Form that is used to Login into the ToolShare system
"""
class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class' : 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class' : 'form-control'}))


"""
Defines the Form that is used to search for available tools
"""
class ToolIndexForm(forms.Form):
   name = forms.CharField(label="Tool Name", max_length=20, widget=forms.TextInput(attrs={'class' : 'form-control'}))

"""
Defines the Form that is used to add a Request to the system
"""
class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ('message',)
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['class'] = "form-control"

