from django.template import Template, Context
from django.shortcuts import render, redirect
import proyectoPrograSegura.settings as conf
from django.http import HttpResponse
from modelo import models
import datetime
from datetime import timezone
import crypt
import os
import base64
import re


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def  es_ip_conocida(ip: str):
    """
    Determina si la ip ya está en la BD
    keyword Arguments:
        ip: str
        returns: Boolean
    """
    registros = models.Peticion.objects.filter(ip=ip)
    return len(registros) != 0

def guardar_peticion(ip: str, intentos: int):
    """
    Rutina para almacenar información de petición, considerando las reglas de bloqueo de peticiones.

    Keyword Arguments:
    ip: str
    intentos: int, es el valor a guardar de intentos
    returns: None
    """
    fecha_actual = datetime.datetime.now(timezone.utc)
    if not es_ip_conocida(ip):
        entrada = models.Peticion(ip=ip, intentos=1,
                                  timestamp=fecha_actual)
        entrada.save()
        return
    registro = models.Peticion.objects.get(ip=ip)
    registro.intentos = intentos
    registro.timestamp = fecha_actual
    registro.save()

def esta_tiempo_en_ventana(timestamp):
    """
    Compara una fecha con la fecha actual
    keyword Arguments:
        timestamp: datetime de referencia
        returns: Bool
    """
    momento_actual = datetime.datetime.now(timezone.utc)
    resta = momento_actual - timestamp
    if resta.seconds < conf.VENTANA_SEGUNDOS_INTENTOS_PETICION:
        return True
    return False

def puede_hacer_peticion(ip):
    """
    Verdadero si la IP no ha alcanzado el límite de intentos.

    Keyword Arguments:
    ip --
    returns: Bool
    """
    if not es_ip_conocida(ip):
        guardar_peticion(ip, 1)
        return True
    registro = models.Peticion.objects.get(ip=ip)
    if not esta_tiempo_en_ventana(registro.timestamp):
        guardar_peticion(ip, 1)
        return True
    else:
        if (registro.intentos + 1) > conf.INTENTOS_MAXIMOS_PETICION:
            guardar_peticion(ip, registro.intentos + 1)
            return False
        else:
            guardar_peticion(ip, registro.intentos + 1)
            return True




def enviar_formulario(request):
    """
    Login con número de intentos

    keyword Arguments:
        request --
        returns: HTTP_Response
    """
    if request.method == 'GET':
        t = 'envio.html'
        return render(request, t)
    elif request.method == 'POST':
        #Actualizar peticiones IP
        if puede_hacer_peticion(get_client_ip(request)):
            return HttpResponse('OK')
        else:
            return HttpResponse('Intentos agotados')

def validar_contraseña(password):
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&-_]{10,}$"
    if re.search(regex, password) is not None:
        return True
    return False

def registro_usuarios(request):
    t = "registro.html"
    bytes_aleatorios = os.urandom(16)
    salt = base64.b64encode(bytes_aleatorios).decode('utf-8')
    if request.method == "GET":
        return render(request, t)
    elif request.method == "POST":
        usuario=request.POST.get('usuario', '')
        password=request.POST.get('password', '')
        if usuario == "":
            return HttpResponse("Todos los campos son requeridos")
        if password == "":
            return HttpResponse("Todos los campos son requeridos")
        if validar_contraseña(password) == False:
            return HttpResponse("Debe ingresar minimo 10 caracteres, una mayúscula, una minúscula, un digito y un caracter especial")
        hasheado = crypt.crypt(password, '$6$' + salt)
        registro_user=models.registro_usuarios(usuario=usuario, password=hasheado)
        registro_user.save()
        return render(request, t)
    
