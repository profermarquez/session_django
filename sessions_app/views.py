# sessions_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
import pytz # Necesitarás instalar 'pytz' si no lo tienes: pip install pytz

# Para ilustrar el uso de sesiones fuera de las vistas
from importlib import import_module
from django.conf import settings

# Obtener la clase SessionStore del motor de sesión configurado
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


def index(request):
    """Página de inicio con enlaces a las diferentes funcionalidades de sesión."""
    return render(request, 'sessions_app/index.html')

def set_session_data(request):
    """Establece datos en la sesión."""
    if request.method == 'POST':
        item_key = request.POST.get('item_key')
        item_value = request.POST.get('item_value')
        if item_key and item_value:
            request.session[item_key] = item_value
            # Si modificas un diccionario dentro de la sesión, debes marcar la sesión como modificada
            # Por ejemplo:
            # if 'my_dict' not in request.session:
            #     request.session['my_dict'] = {}
            # request.session['my_dict']['new_key'] = 'new_value'
            # request.session.modified = True
            message = f" '{item_key}' establecido a '{item_value}' en la sesión."
        else:
            message = "Por favor, proporciona una clave y un valor."
    else:
        message = "Introduce una clave y un valor para establecer en la sesión."

    current_session_data = request.session.items()
    return render(request, 'sessions_app/set_session.html', {'message': message, 'current_session_data': current_session_data})


def get_session_data(request):
    """Recupera datos de la sesión."""
    # Ejemplo de cómo obtener un valor con un valor por defecto
    fav_color = request.session.get('fav_color', 'no establecido')
    user_name = request.session.get('user_name', 'Invitado')
    member_id = request.session.get('member_id', 'N/A')
    has_commented = request.session.get('has_commented', False)

    session_data = {
        'fav_color': fav_color,
        'user_name': user_name,
        'member_id': member_id,
        'has_commented': has_commented,
        'all_session_items': request.session.items(),
    }
    return render(request, 'sessions_app/session_info.html', {'session_data': session_data, 'title': 'Datos de Sesión'})


def delete_session_data(request):
    """Elimina una clave específica de la sesión."""
    if request.method == 'POST':
        key_to_delete = request.POST.get('key_to_delete')
        if key_to_delete in request.session:
            del request.session[key_to_delete]
            message = f"'{key_to_delete}' eliminado de la sesión."
        else:
            message = f"'{key_to_delete}' no encontrado en la sesión."
    else:
        message = "Introduce la clave que deseas eliminar de la sesión."

    current_session_data = request.session.items()
    return render(request, 'sessions_app/set_session.html', {'message': message, 'current_session_data': current_session_data})


def flush_session(request):
    """Elimina todos los datos de la sesión actual y la cookie de sesión."""
    request.session.flush()
    return HttpResponse("¡Sesión vaciada! Todos los datos de la sesión han sido eliminados y la cookie de sesión ha sido invalidada.")


def test_cookies(request):
    """Establece una cookie de prueba."""
    request.session.set_test_cookie()
    return render(request, 'sessions_app/test_cookies.html', {'message': 'Cookie de prueba establecida. Ahora ve a la página de verificación.'})


def check_test_cookie(request):
    """Verifica si la cookie de prueba funcionó y la elimina."""
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        message = "¡La cookie de prueba funcionó! La cookie de prueba ha sido eliminada."
    else:
        message = "La cookie de prueba NO funcionó. Por favor, asegúrate de que las cookies estén habilitadas en tu navegador."
    return render(request, 'sessions_app/test_cookies.html', {'message': message})

def delete_test_cookie_view(request):
    """Elimina el test cookie si existe."""
    if 'testcookie' in request.session:
        request.session.delete_test_cookie()
        message = "Cookie de prueba eliminada explícitamente."
    else:
        message = "La cookie de prueba no existía en la sesión para ser eliminada."
    return HttpResponse(message)


def set_expiry_seconds(request):
    """Establece la expiración de la sesión en 30 segundos de inactividad."""
    request.session.set_expiry(30)
    return HttpResponse("La sesión expirará en 30 segundos de inactividad.")

def set_expiry_browser(request):
    """Establece la expiración de la sesión al cerrar el navegador."""
    request.session.set_expiry(0)
    return HttpResponse("La sesión expirará cuando cierres el navegador.")

def set_expiry_none(request):
    """Restablece la expiración de la sesión a la política global (SESSION_COOKIE_AGE)."""
    request.session.set_expiry(None)
    return HttpResponse(f"La sesión revertirá a la política de expiración global (actualmente {settings.SESSION_COOKIE_AGE} segundos).")


def session_info(request):
    """Muestra información detallada de la sesión."""
    session_id = request.session.session_key
    expire_at_browser_close = request.session.get_expire_at_browser_close()
    expiry_age = request.session.get_expiry_age()
    expiry_date = request.session.get_expiry_date()
    modified_status = request.session.modified

    # Ejemplo de uso de session_data fuera de una vista (solo si es el backend de DB)
    session_data_from_db = None
    if settings.SESSION_ENGINE == 'django.contrib.sessions.backends.db' and session_id:
        try:
            from django.contrib.sessions.models import Session
            s = Session.objects.get(pk=session_id)
            session_data_from_db = s.get_decoded()
        except Session.DoesNotExist:
            session_data_from_db = "No se pudo cargar la sesión de la base de datos (quizás expiró o no existe aún)."
        except Exception as e:
            session_data_from_db = f"Error al cargar de DB: {e}"
    elif session_id and settings.SESSION_ENGINE != 'django.contrib.sessions.backends.db':
         # Para otros backends, podemos intentar cargar con SessionStore directamente
         # Esto es más para fines de demostración que para un uso común en producción
         try:
             s_store = SessionStore(session_key=session_id)
             session_data_from_db = s_store.load()
         except Exception as e:
             session_data_from_db = f"Error al cargar con SessionStore: {e}"


    # Ejemplo de cómo manipular sesiones fuera de una vista (solo para DB o File backends que lo permitan)
    # Esto es solo para fines ilustrativos y no debe hacerse a menudo en la práctica
    try:
        s_obj_out_of_view = SessionStore()
        s_obj_out_of_view['out_of_view_data'] = 'This was set outside a view!'
        s_obj_out_of_view.create() # Guarda la nueva sesión en el store
        out_of_view_session_key = s_obj_out_of_view.session_key
    except Exception as e:
        out_of_view_session_key = f"No se pudo crear sesión fuera de vista: {e}"


    context = {
        'session_id': session_id,
        'current_session_data': request.session.items(),
        'expire_at_browser_close': expire_at_browser_close,
        'expiry_age': expiry_age,
        'expiry_date': expiry_date,
        'modified_status': modified_status,
        'session_data_from_db': session_data_from_db,
        'out_of_view_session_key': out_of_view_session_key,
        'session_engine': settings.SESSION_ENGINE,
        'session_cookie_age': settings.SESSION_COOKIE_AGE,
    }
    return render(request, 'sessions_app/session_info.html', context)