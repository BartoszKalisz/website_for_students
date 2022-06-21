from django import forms
from django.forms import widgets
from . models import *
from django.contrib.auth.forms import UserCreationForm

class NotatkiForm(forms.ModelForm):
    class Meta:
        model = Notatki
        fields = ['tytuł','opis']

class DateInput(forms.DateInput):
    input_type = 'date'

class ListaForm(forms.ModelForm):
    class Meta:
        model = Lista
        widgets = {'termin':DateInput()}
        fields = ['przedmiot','tytuł','opis','termin','czy_skonczony']

    
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Search : ")


class LinijkaForm(forms.Form):
    CHOICES = [('długość','Długość'),('masa','Masa'),('temperatura','Temperatura')]
    przeliczanie_jednostek_miary = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)


class LinijkaLengthForm(forms.Form):
    CHOICES = [('jard','Jard'),('stopa','Stopa'),('mila','Mila'),('milimetr','Milimetr'),('centymetr','Centymetr'),('metr','Metr'),('decymetr','Decymetr'),('kilometr','Kilometr')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number','placeholder':'Wpisz liczbę : '}
    ))
    wartość_1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

    wartość_2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )


class LinijkaMassForm(forms.Form):
    CHOICES = [('funt','Funt'),('kilogram','Kilogram'),('uncja','Uncja'),('tona','Tona'),('gram','Gram'),('miligram','MiliGram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number','placeholder':'Wpisz liczbę : '}
    ))
    wartość_1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

    wartość_2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

class Linijka_miary_temperatury(forms.Form):
    CHOICES = [('celcjusz','Celcjusz'),('kelvin','Kelvin'),('fahrenheit','Fahrenheit')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {'type':'number','placeholder':'Wpisz liczbę : '}
    ))
    wartość_1 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )

    wartość_2 = forms.CharField(
        label='', widget=forms.Select(choices=CHOICES)
    )
    

class Rejestracja_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']