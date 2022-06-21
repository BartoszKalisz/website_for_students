from django import contrib
from django.core.checks import messages
import django.db.models.query
from django.forms.widgets import FileInput
from django.shortcuts import redirect, render
from . forms import *
from django.contrib import messages
from django.views import generic
import requests
from django.contrib.auth.decorators import login_required

def strona_glowna(request):
    return render(request,'dashboard/strona_glowna.html')

@login_required
def notatki(request):
    if request.method == 'POST':
        form = NotatkiForm(request.POST)
        if form.is_valid():
            notatki = Notatki(uzytkownik=request.user,tytuł=request.POST['tytuł'],opis=request.POST['opis'])
            notatki.save()
        messages.success(request,f"Notatka została dodana pomyślnie")
    else:
        form = NotatkiForm()
    notatki = Notatki.objects.filter(uzytkownik=request.user)
    context = {'notatki':notatki,'form':form}
    return render(request,'dashboard/notatki.html',context)

@login_required
def usun_notatke(request,pk=None):
    Notatki.objects.get(id=pk).delete()
    return redirect("notatki")

class Notatki_szczegoly(generic.DetailView):
    model = Notatki

@login_required
def lista(request):
    if request.method == 'POST':
        form = ListaForm(request.POST)
        if form.is_valid():
            try:
                skonczony = request.POST['czy_skonczony']
                if skonczony == 'on':
                    skonczony = True
                else:
                    skonczony = False
            except:
                skonczony = False
            listy = Lista(
                uzytkownik = request.user,
                przedmiot = request.POST['przedmiot'],
                tytuł = request.POST['tytuł'],
                opis = request.POST['opis'],
                termin = request.POST['termin'],
                czy_skonczony = skonczony               
            )
            listy.save()
            messages.success(request,f"Zadanie domowe zostało dodane pomyślnie")
    else:
        form = ListaForm()
    lista = Lista.objects.filter(uzytkownik=request.user)
    if len(lista) == 0:
        czy_skonczona_lista = True
    else:
        czy_skonczona_lista = False
    context = {
        'listy':lista,
        'lista_done':czy_skonczona_lista,
        'form':form
        }
    return render(request,'dashboard/lista.html',context)

@login_required
def zaktualizuj_liste(request,pk=None):
    lista = Lista.objects.get(id=pk)
    if lista.czy_skonczony == True:
        lista.czy_skonczony = False
    else:
        lista.czy_skonczony = True
    lista.save()
    return redirect("lista")

@login_required
def usun_liste(request,pk=None):
    Lista.objects.get(id=pk).delete()
    print("XDD")
    return redirect("lista")

def linijka(request):
    if request.method == 'POST':
        form = LinijkaForm(request.POST)
        if request.POST['przeliczanie_jednostek_miary'] == 'długość':
            dlugosc = LinijkaLengthForm()
            context = {
                'form':form,
                'm_form':dlugosc,
                'input':True
            }
            if 'input' in request.POST:
                pierwsza_wartosc = request.POST['wartość_1']
                druga_wartosc = request.POST['wartość_2']
                input = request.POST['input']
                odpowiedz = ''
                if input and int(input) >= 0:
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} m = {int(input)*0.001} km'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} m = {int(input)*10} dm'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} m = {int(input)*100} cm'                      
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'milimetr':                #konwersja z metrow
                        odpowiedz = f'{input} m = {int(input)*1000} mm'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} m = {int(input)/0.30480} ft'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} m = {int(input)/0.9144} yd'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} m = {int(input)/1609.344} M'
                        
                    if pierwsza_wartosc == 'kilometr' and druga_wartosc == 'metr':
                        odpowiedz = f'{input} km = {int(input)*1000} m'
                    if pierwsza_wartosc == 'kilometr' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} km = {int(input)*10000} dm'
                    if pierwsza_wartosc == 'kilometr' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} km = {int(input)*100000} cm'
                    if pierwsza_wartosc == 'kilometr' and druga_wartosc == 'milimetr':
                        odpowiedz = f'{input} km = {int(input)*1000000} mm'                        #konwersja z kilometrów
                    if pierwsza_wartosc == 'kilometr' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} km = {int(input)/0.00030480} ft'
                    if pierwsza_wartosc == 'killmetr' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} km = {int(input)/0.0009144} yd'
                    if pierwsza_wartosc == 'kilometr' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} km = {int(input)/1.609344} M'
                        
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} cm = {int(input)*0.00001} km'
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} cm = {int(input)*0.1} dm'
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'metr':
                        odpowiedz = f'{input} cm = {int(input)*0.01} m'                             #konwersja z centymetrow
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'milimetr':
                        odpowiedz = f'{input} cm = {int(input)*1000} mm'
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} cm = {int(input)/30.480} ft'
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} cm = {int(input)/91.44} yd'
                    if pierwsza_wartosc == 'centymetr' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} cm = {int(input)/160934.4} M'
                        
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} m = {int(input)*0.001} km'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} m = {int(input)*10} dm'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} m = {int(input)*100} cm'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'milimetr':
                        odpowiedz = f'{input} m = {int(input)*1000} mm'                              #konwersja z decymetrów
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} m = {int(input)*0.30480} ft'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} m = {int(input)*0.9144} yd'
                    if pierwsza_wartosc == 'metr' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} m = {int(input)*1609.344} M'
                        
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} mm = {int(input)*0.000001} km'
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} mm = {int(input)*0.01} dm'
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} mm = {int(input)*0.1} cm'                            #konwersja z milimetrów
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'metr':
                        odpowiedz = f'{input} mm = {int(input)*0.001} m'
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} mm = {int(input)/304.80} ft'
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} mm = {int(input)/914.4} yd'
                    if pierwsza_wartosc == 'milimetr' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} mm = {int(input)/1609344} M'
                        
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} ft = {int(input)*0.00030480} km'
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} ft = {int(input)*3.0480} dm'
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} ft = {int(input)*30.480} cm'                            #konwersja z stóp
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'metr':
                        odpowiedz = f'{input} ft = {int(input)*0.30480} mm'
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'milimetr':
                        odpowiedz = f'{input} ft = {int(input)*304.80} mm'
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} ft = {int(input)/0.9144*0.30480} yd'
                    if pierwsza_wartosc == 'stopa' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} ft = {int(input)/1609.344*0.30480} M'
                        
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} yd = {int(input)*0.0009144} km'
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} yd = {int(input)*9.144} dm'
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} yd = {int(input)*91.44} cm'                      
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'milimetr':                #konwersja z jardów
                        odpowiedz = f'{input} yd = {int(input)*914.4} mm'
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} yd = {int(input)/0.30480*0.9144} ft'
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'metr':
                        odpowiedz = f'{input} yd = {int(input)*0.9144} m'
                    if pierwsza_wartosc == 'jard' and druga_wartosc == 'mila':
                        odpowiedz = f'{input} yd = {int(input)/1609.344*0.9144} M'
                    
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'kilometr':
                        odpowiedz = f'{input} M = {int(input)*1.609344} km'
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'decymetr':
                        odpowiedz = f'{input} M = {int(input)*16093.44} dm'
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'centymetr':
                        odpowiedz = f'{input} M = {int(input)*160934.4} cm'                      
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'milimetr':                #konwersja z mil
                        odpowiedz = f'{input} M = {int(input)*1609344} mm'
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'stopa':
                        odpowiedz = f'{input} M = {int(input)/0.30480*1609.344} ft'
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'jard':
                        odpowiedz = f'{input} M = {int(input)/0.9144*1609.344} yd'
                    if pierwsza_wartosc == 'mila' and druga_wartosc == 'metr':
                        odpowiedz = f'{input} M = {int(input)*1609.344} m'
                        
                    context = {
                        'form':form,
                        'm_form':dlugosc,
                        'input':True,
                        'answer':odpowiedz
                    }
        if request.POST['przeliczanie_jednostek_miary'] == 'masa':
            masa = LinijkaMassForm()
            context = {
                'form':form,
                'm_form':masa,
                'input':True
            }
            if 'input' in request.POST:
                pierwsza_wartosc = request.POST['wartość_1']
                druga_wartosc = request.POST['wartość_2']
                input = request.POST['input']
                odpowiedz = ''
                if input and int(input) >= 0:
                    if pierwsza_wartosc == 'kilogram' and druga_wartosc == 'gram':
                        odpowiedz = f'{input} kg = {int(input)*1000} g'
                    if pierwsza_wartosc == 'kilogram' and druga_wartosc == 'funt':
                        odpowiedz = f'{input} kg = {int(input)/0.45359237} lb'
                    if pierwsza_wartosc == 'kilogram' and druga_wartosc == 'uncja':
                        odpowiedz = f'{input} kg = {int(input)*0.02834952981} oz'                              #konwersja z kilogramów
                    if pierwsza_wartosc == 'kilogram' and druga_wartosc == 'tona':
                        odpowiedz = f'{input} kg = {int(input)*0.0001} t'
                    if pierwsza_wartosc == 'kilogram' and druga_wartosc == 'miligram':
                        odpowiedz = f'{input} kg = {int(input)*1000} mg'
                        
                    if pierwsza_wartosc == 'gram' and druga_wartosc == 'kilogram':
                        odpowiedz = f'{input} g = {int(input)*0.001} kg'
                    if pierwsza_wartosc == 'gram' and druga_wartosc == 'funt':
                        odpowiedz = f'{input} g = {int(input)/453,59237  } lb'
                    if pierwsza_wartosc == 'gram' and druga_wartosc == 'uncja':
                        odpowiedz = f'{input} g = {int(input)/28.34952981} oz'                                   #konwersja z gramów
                    if pierwsza_wartosc == 'gram' and druga_wartosc == 'tona':
                        odpowiedz = f'{input} g = {int(input)*0.000001} t'
                    if pierwsza_wartosc == 'gram' and druga_wartosc == 'miligram':
                        odpowiedz = f'{input} g = {int(input)*1000} mg'
                        
                    if pierwsza_wartosc == 'tona' and druga_wartosc == 'gram':
                        odpowiedz = f'{input} t = {int(input)*1000000} g'
                    if pierwsza_wartosc == 'tona' and druga_wartosc == 'funt':
                        odpowiedz = f'{input} t = {int(input)/0.00000045359237} lb'
                    if pierwsza_wartosc == 'tona' and druga_wartosc == 'uncja':                           #konwersja z ton
                        odpowiedz = f'{input} t = {int(input)/0.00002834952981} oz'
                    if pierwsza_wartosc == 'tona' and druga_wartosc == 'kilogram':
                        odpowiedz = f'{input} t = {int(input)*1000} kg'
                    if pierwsza_wartosc == 'tona' and druga_wartosc == 'miligram':
                        odpowiedz = f'{input} t = {int(input)*1000000000} mg'
                        
                    if pierwsza_wartosc == 'miligram' and druga_wartosc == 'gram':
                        odpowiedz = f'{input} mg = {int(input)*0.001} g'
                    if pierwsza_wartosc == 'miligram' and druga_wartosc == 'funt':
                        odpowiedz = f'{input} mg = {int(input)/453592.37} lb'
                    if pierwsza_wartosc == 'miligram' and druga_wartosc == 'uncja':                     #konwersja z miligramów
                        odpowiedz = f'{input} mg = {int(input)/28349.52981} oz'
                    if pierwsza_wartosc == 'miligram' and druga_wartosc == 'tona':
                        odpowiedz = f'{input} mg = {int(input)*0.000000001} t'
                    if pierwsza_wartosc == 'miligram' and druga_wartosc == 'kilogram':
                        odpowiedz = f'{input} mg = {int(input)*0.000001} kg'
                        
                    if pierwsza_wartosc == 'funt' and druga_wartosc == 'gram':
                        odpowiedz = f'{input} lb = {int(input)*453.59237} g'
                    if pierwsza_wartosc == 'funt' and druga_wartosc == 'kilogram':
                        odpowiedz = f'{input} lb = {int(input)*0.45359237} kg'
                    if pierwsza_wartosc == 'funt' and druga_wartosc == 'uncja':
                        odpowiedz = f'{input} lb = {int(input)*16} oz'                            #konwersja z funtów
                    if pierwsza_wartosc == 'funt' and druga_wartosc == 'tona':
                        odpowiedz = f'{input} lb = {int(input)*0.00045359237} t'
                    if pierwsza_wartosc == 'funt' and druga_wartosc == 'miligram':
                        odpowiedz = f'{input} lb = {int(input)*453592.37} mg'
                        
                    if pierwsza_wartosc == 'uncja' and druga_wartosc == 'gram':
                        odpowiedz = f'{input} oz = {int(input)*28.34952981} g'
                    if pierwsza_wartosc == 'uncja' and druga_wartosc == 'funt':
                        odpowiedz = f'{input} oz = {int(input)/16} lb'
                    if pierwsza_wartosc == 'uncja' and druga_wartosc == 'kilogram':
                        odpowiedz = f'{input} oz = {int(input)*0.02834952981} kg'                     #konwersja z uncji
                    if pierwsza_wartosc == 'uncja' and druga_wartosc == 'tona':
                        odpowiedz = f'{input} oz = {int(input)*0.00002834952981} t'
                    if pierwsza_wartosc == 'uncja' and druga_wartosc == 'miligram':
                        odpowiedz = f'{input} oz = {int(input)*28349.52981} mg'
                        
                        
                    context = {
                        'form':form,
                        'm_form':masa,
                        'input':True,
                        'answer':odpowiedz
                    }
                    
        if request.POST['przeliczanie_jednostek_miary'] == 'temperatura':
            temperatura = Linijka_miary_temperatury()
            context = {
                'form':form,
                'm_form':temperatura,
                'input':True
            }
            if 'input' in request.POST:
                pierwsza_wartosc = request.POST['wartość_1']
                druga_wartosc = request.POST['wartość_2']
                input = request.POST['input']
                odpowiedz = ''
                if input and int(input) >= 0:
                    if pierwsza_wartosc == 'celcjusz' and druga_wartosc == 'kelvin':
                        odpowiedz = f'{input} C = {int(input)+273.15} K'
                    if pierwsza_wartosc == 'celcjusz' and druga_wartosc == 'fahrenheit':
                        odpowiedz = f'{input} C = {int(input)*1.8+32} F'
                        
                    if pierwsza_wartosc == 'fahrenheit' and druga_wartosc == 'celcjusz':
                        odpowiedz = f'{input} F = {(int(input)-32)/1.8} C'
                    if pierwsza_wartosc == 'fahrenheit' and druga_wartosc == 'kelvin':
                        odpowiedz = f'{input} F = {(int(input)-32)/1.8+273.15} K'
                         
                    if pierwsza_wartosc == 'kelvin' and druga_wartosc == 'celcjusz':
                        odpowiedz = f'{input} K = {int(input)-273.15} C'
                    if pierwsza_wartosc == 'kelvin' and druga_wartosc == 'fahrenheit':
                        odpowiedz = f'{input} K = {(int(input)-273.15)*1.8+32} F'
                    
                    context = {
                        'form':form,
                        'm_form':temperatura,
                        'input':True,
                        'answer':odpowiedz
                    }

    else:
        form = LinijkaForm()
        context = {
            'form':form,
            'input':False
        }
    return render(request,'dashboard/linijka.html',context)


def zarejestruj(request):
    if request.method == 'POST':
        form = Rejestracja_Form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Konto zostało utworzone pomyślnie')
            return redirect('zaloguj')
    else:
        form = Rejestracja_Form()
    context = {
        'form':form
    }
    return render(request,'dashboard/zarejestruj.html',context)

@login_required
def użytkownik(request):
    listy = Lista.objects.filter(czy_skonczony=False,uzytkownik=request.user)
    if len(listy) == 0:
        czy_skonczona_lista = True
    else:
        czy_skonczona_lista = False
    context = {
        'homeworks' : listy,
        'homework_done':czy_skonczona_lista,
    }
    return render(request,'dashboard/użytkownik.html',context)

def kalkulator(request):
    wynik=""
    try:
        if request.method=="POST":
            liczba_1=eval(request.POST.get('liczba_1'))
            liczba_2=eval(request.POST.get('liczba_2'))
            operator=request.POST.get('operator')
            if operator=="+":
                wynik=liczba_1+liczba_2;
            elif operator=="-":
                wynik=liczba_1-liczba_2
            elif operator=="*":
                wynik=liczba_1*liczba_2
            elif operator=="/":
                wynik=liczba_1/liczba_2
    except:
        wynik="Błedny typ danych"
    print(wynik)
    return render(request,"dashboard/kalkulator.html",{'wynik':wynik})