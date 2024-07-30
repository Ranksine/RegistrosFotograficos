from django.shortcuts import render
from django.shortcuts import redirect
import os
import pandas as pd
from PIL import Image
import io
from django.http import Http404, HttpResponseBadRequest, HttpResponse

from django.db import connection
from django.db.models import Q
from django.db.models import Count, Sum

from django.views import View
from django.views.generic.list import ListView
from django.template import RequestContext
from .forms import CorporacionesForm
from .models import Corporaciones
from .models import CorporacionesMov
from .models import Corporacion
from .models import Persona
from .models import FichaFoto

class IndexView(View):
    
    def get(self, request):
        print('Entrando a GET')
        formBusqueda = CorporacionesForm()
        print(f'Valor requesto: {request}')
        return render(request, 'Index.html',{'formBusqueda': formBusqueda})
    
    def post(self, request):
        print('Entra el POST')
        nombre_corp = request.POST.get('descripcion')
        clave_corp = request.POST.get('clave')
        status_real = request.POST.get('status_real')
        estado = 1 if status_real else 2
        print(f'Estado: {estado}')
        fecha = request.POST.get('f_ing_depen')
        
        return redirect('consulta_corp/' + str(clave_corp) + '/' + str(estado) + '/' + str(fecha))
    

class Consulta_Fotos(View):
    def get(self,request, clave_corp,  status_real, fecha):
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        print('Entrando a consultar jeje')
        
        total_consulta = self.contar_resultados_consulta(clave_corp, status_real, fecha)
        print(f'Total de registros encontrados: {str(total_consulta)}')
        
        self.proceso_principal(clave_corp, status_real, fecha,directorio_script)
        
        total_fotos = self.contar_carpeta(directorio_script)
        print(f'Total de fotos generadas: {str(total_fotos)}')
        
        return render(request, 'Consultar.html',{'directorio':directorio_script, 'clave_corp': clave_corp, 'status_real': status_real, 'fecha': fecha, 'total_consulta': total_consulta, 'total_fotos': total_fotos})
    
    def contar_resultados_consulta(self,cve_corp, son_activos, fecha_limite):
        corps = Corporaciones.objects.filter(corporacion=cve_corp).filter(status_real=son_activos).filter(f_ing_depen__lte = fecha_limite).values('id_corp').count()
        return corps
    
    def contar_carpeta(self, directorio):
        directorio_base  = os.path.dirname(directorio)
        print(f'Direcotorio base: {directorio_base}')
        ruta_carpeta = os.path.join(directorio_base, 'Fotografias')
        print(f'Carpeta Fotos: {ruta_carpeta}')
        if not os.path.exists(ruta_carpeta):
            return -1
        archivos = os.listdir(ruta_carpeta)
        print('Lista de archivos de Fotografias')
        print(archivos)
        
        return len(archivos)
    
    def buscar_carpeta(self,carpeta):
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def hex_a_bytes(self, hex_string): # Obsoleta al 29/07/2024
        # Convierte un string hexadecimal en una cadena de bytes.
        # Elimina los prefijos '0x' y espacios si están presentes
        hex_string = hex_string.replace('0x', '').replace(' ', '')
        return bytes.fromhex(hex_string)

    def generar_imagen(self, hex_string, nombre_archivo):
        #print(f'Valor de imagen: {hex_string[:10]}'.center(50,'-'))
        if hex_string == None: #HACER UNA IMAGEN EN NEGRO ## Cambiarlo por una imagen default vacía
            width, height = 100, 100
            imagen = Image.new('RGB', (width, height), color='black')
        else:
            datos_binarios = hex_string 
            datos_imagen = io.BytesIO(datos_binarios)
            imagen = Image.open(datos_imagen)
        ruta_archivo = os.path.join('Fotografias', nombre_archivo + '.jpg')
        imagen.save(ruta_archivo, format='JPEG')
        
    def proceso_principal(self,clave_corp, status_real, fecha, directorio):
        carpeta_fotos = os.path.join(directorio, 'Fotografias')
        self.buscar_carpeta(carpeta_fotos)
        print(f'Directorio: {directorio}')
        cve_corp = clave_corp
        # Recuperar el nombre de la corporacion
        corporacion = Corporacion.objects.filter(clave=clave_corp).values_list('descripcion', flat=True)
        
        diccionario_fotos = self.consultardb(cve_corp, status_real, fecha)
        
        for rfc, imagen in diccionario_fotos:
            # print(f'RFC: {rfc}, Imagen: {imagen[:10]}')
            self.generar_imagen(imagen, rfc)     
        
    #Hace falta una funcion ExisteCorporacion antes de la consulta completa
    def consultardb(self,cve_corp, son_activos,fecha_limite, nombre_corp = '' ):
        print(f'Parametros cons: Clave: {cve_corp}, Activo: {son_activos}, Fecha: {fecha_limite}')
        
        with connection.cursor() as cursor:
            querystr = 'EXEC REGISTRO_FOTOGRAFICO_CORPORACION @CVE_CORP = %s, @STATUS_ACTIVO = %s, @FECHA_INGRESO = %s'
            cursor.execute(querystr, [cve_corp, son_activos, fecha_limite])
            queryres = cursor.fetchall()
        
        diccionario_resultados = {fila[0]: fila[1] for fila in queryres}

        return queryres
            