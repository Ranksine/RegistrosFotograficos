from django import forms

from Consulta_Fotos_Corp.models import *

class CorporacionesForm(forms.ModelForm):
    class Meta:
        model = Corporacion
        fields=['descripcion', 'clave', 'status_real', 'f_ing_depen']
        
    descripcion = forms.CharField(required=False,
                                  label = 'Corporación',
                                  max_length=100,
                                  widget=forms.TextInput(attrs={
                                      'class': 'busqueda-form',
                                      'id': 'nombre_corp',
                                      'name': 'nombre_corp',
                                  }),
                                  disabled = True,
                                )
    clave = forms.IntegerField(required=False,
                                  label = 'Clave',
                                  widget=forms.NumberInput(attrs={
                                      'class': 'busqueda-form',
                                      'id': 'clave_corp',
                                      'name': 'clave_corp'
                                  })
                                )
    status_real = forms.BooleanField(required=True,
                                  label = 'Elementos activos',
                                  initial=True,
                                  widget=forms.CheckboxInput(attrs={
                                      'class': 'busqueda-form',
                                      'id': 'status_real',
                                      'name': 'status_real'
                                  }),
                                )
    f_ing_depen = forms.DateField(required=True,
                                   label = 'Selecciona fecha límite',
                                   widget=forms.DateInput(format="%d-%m-%Y", attrs={
                                       "type": "date",
                                       "class": "busqueda-form",
                                       "id": "fecha_limite",
                                       "name": "fecha_limite",
                                   }),
                                   input_formats= ["%d-%m-%Y"]
                                )
    
    