from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.strona_glowna,name='strona_glowna'),
    path('notatki/',views.notatki,name='notatki'),
    path('usun_notatke/<int:pk>/',views.usun_notatke,name='usun_notatke'),
    path('notatkidetail/<int:pk>/',views.Notatki_szczegoly.as_view(),name='notatkadetail'),
    path('lista/',views.lista,name='lista'),
    path('zaktualizuj_liste/<int:pk>/',views.zaktualizuj_liste,name='zaktualizuj_liste'),
    path('usun_liste/<int:pk>/',views.usun_liste,name='usun_liste'),
    path('linijka/',views.linijka,name='linijka'),
    path('kalkulator/',views.kalkulator,name='kalkulator')

]