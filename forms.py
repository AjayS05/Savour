import email
from unicodedata import category
from wsgiref.validate import validator
from django import forms
from django.contrib.auth.models import User
from .models import MenuCategory, MenuItems, UserProfileInfo, ContactUs
from django.core.validators import EmailValidator


class UserForm(forms.ModelForm):


    class Meta():
        model = User
        fields = ('username','email','password')
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your username', 'label':''}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email ID' ,'required': 'True'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter at least one capital, one digit and one symbol(@/./+/-/_)'}),
        }


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('contactno',)
        widgets={
            'contactno': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter your Contact number'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta():
        model = MenuCategory
        fields= ('CatName',)

class ItemForm(forms.ModelForm):
    category=[]

    for i in MenuCategory.objects.values_list('CatName'):
        category.append([i[0],i[0]])

    menuitems= forms.ChoiceField(choices= category)
    class Meta():
        model = MenuItems
        fields= ('ItemName', 'ItemRate', 'ItemImage', 'speciality')


class ContactUsForm(forms.ModelForm):
    choices=[['Suggestion','Suggestion'],['Query', 'Query'], ['Complaint','Complaint']]
    feedbackType= forms.ChoiceField(choices=choices)

    class Meta():
        model= ContactUs
        fields= ('FullName', 'Email', 'MobileNumber','feedbackType', 'QueryText')
        widgets= {
            'FullName': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your name'}),
            'Email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter your name'}),
            'MobileNumber': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter your 10-digit Mobile Number'}),
            'feedbackType': forms.Select(attrs={'class':'form-control'}),
            'QueryText': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Type in your query', 'rows':'3'}),
        }
