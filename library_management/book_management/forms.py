from typing import Any, Dict
from django import forms
from book_management.models import UserID, Books,BookRequest,men,Sports
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory


class UserIDform(forms.ModelForm):
    class Meta():
        model = UserID
        fields = ['user_type', ]
        widgets = {
            'user_type': forms.RadioSelect(),
        }



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['username', 'email', 'password']


class BooksForm(forms.ModelForm):
    class Meta():
        model = Books
        fields = ['Author', 'Name_Of_Book', 'Available']
        

BookFormSet = modelformset_factory(Books, form=BooksForm, extra=1)

 
        
class BookRequestForm(forms.ModelForm):
    
    class Meta:
        model = BookRequest
        fields = ['generated_for']
        labels = {'generated_for': 'Request For'}

    def __init__(self,user_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(user_type)
        if user_type == 'student':
            self.fields['generated_for'].queryset=User.objects.filter(userid__user_type='teacher')
            
class TeacherRequestForm(forms.ModelForm):
    class Meta:
        model=BookRequest
        fields=['book','generated_by','status']  


class BookRequestForm1(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        accepted_denied_statuses = [('accepted', 'Accepted'), ('denied', 'Denied')]
        self.fields['status'].choices = accepted_denied_statuses

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel File')


class SportForm(forms.ModelForm):
    
    class Meta:
        model=Sports
        fields=["sports_name","player_name"]

class MenForm(forms.ModelForm):
    class Meta:
        model=men
        fields=["player_type"] 
    
    
