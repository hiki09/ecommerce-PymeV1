from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Cuenta, UserProfile
from pedidos.models import Pedido
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from carrito.views import _carrito_id
from carrito.models import Carrito, CarritoItem
import requests

# Create your views here.
def registrarse(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #Se captura email del usuario y se utiliza como username
            username = email.split("@")[0]
            user = Cuenta.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            #Me genera ID
            #Aca lo capturo
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()


            current_site = get_current_site(request)
            mail_subject = 'Por favor activa tu cuenta en DonLuis'
            body = render_to_string('cuentas/cuenta_verificacion_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            try:
                send_email.send()
            except Exception as e:
                print(f"Error al enviar correo: {e}")


            #messages.success(request, 'Se registro el usuario exitosamente')
            return redirect('/cuentas/login/?command=verification&email='+email)

    
    context = {
        'form': form,
    }
    return render(request, 'cuentas/registrarse.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:

            try:
                carrito = Carrito.objects.get(carrito_id=_carrito_id(request))
                is_cart_item_exist = CarritoItem.objects.filter(carrito=carrito).exists()
                if is_cart_item_exist:
                    carrito_item = CarritoItem.objects.filter(carrito=carrito)
                    #comparo 2 arreglos, el de la sesion con el que no "esta" en sesion
                    producto_variedad = []
                    for item in carrito_item:
                        variedad = item.variedades.all()
                        producto_variedad.append(list(variedad))

                    carrito_item = CarritoItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in carrito_item:
                        existing_variedad = item.variedades.all()
                        ex_var_list.append(list(existing_variedad))
                        id.append(item.id)

                    for pr in producto_variedad:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CarritoItem.objects.get(id=item_id)
                                item.qty +=1
                                item.user = user
                                item.save()
                            else:
                                carrito_item = CarritoItem.objects.filter(carrito=carrito)
                                for item in carrito_item:
                                    item.user = user
                                    item.save()

            except:
                pass
            

            #quiero capturar ?next=/carrito/checkout/ al iniciar sesion con items y derivar al checkout
            auth.login(request, user)
            messages.success(request, 'Has iniciado sesion exitosamente!')

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #next=/carrito/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params: 
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                pass
            return redirect('perfil')
        else:
            messages.error(request, 'Las credenciales son incorrectas')
            return redirect('login')


    return render(request, 'cuentas/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Has cerrado tu sesion')

    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Cuenta._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades, tu cuenta esta activada!')
        return redirect('login')
    else:
        messages.error(request, 'La activacion es invalida')
        return redirect('registrarse')


@login_required(login_url='login')
def perfil(request):
    pedidos = Pedido.objects.order_by('-created_at').filter(user_id=request.user.id, is_orderer=True)
    pedidos_count = pedidos.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'pedidos_count': pedidos_count,
        'userprofile': userprofile,
    }

    return render(request, 'cuentas/perfil.html', context)



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Cuenta.objects.filter(email=email).exists():
            user = Cuenta.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Resetear Contraseña'
            body = render_to_string('cuentas/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body , to=[to_email])
            send_email.send()

            messages.success(request, 'Un correo fue enviado para resetear tu contraseña.')
            return redirect('login')
        else:
            messages.error(request, 'La cuenta de usuario no existe')
            return redirect('forgotpassword')

    return render(request, 'cuentas/forgotpassword.html')



def resetpassword_validate(request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Cuenta._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
            user=None
        
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Por favor resetea tu contraseña')
            return redirect('resetpassword')
        else:
            messages.error(request, 'El link ha expirado')
            return redirect('login')
        

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Cuenta.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'La contraseña se reseteo correctamente')
            return redirect('login')
        else:
            messages.error(request, 'La contraseña de confirmacion no concuerda')
            return redirect('resetpassword')
    else:
        return render(request, 'cuentas/resetpassword.html')
    


def mis_pedidos(request):
    pedidos = Pedido.objects.filter(user=request.user, is_orderer=True).order_by('-created_at')
    context = {
        'pedidos': pedidos,
    }

    return render(request, 'cuentas/mis_pedidos.html', context)


@login_required(login_url='login')
def editar_perfil(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Su informacion fue guardada con exito!')
            return redirect('editar_perfil')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'cuentas/editar_perfil.html', context)    


@login_required(login_url='login')
def cambiar_contrasena(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Cuenta.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'La contraseña se actuliazo correctamente')
                return redirect('cambiar_contrasena')
            else:
                messages.error(request, 'Por favor ingrese una contraseña valida!')
                return redirect('cambiar_contrasena')
        else:
            messages.error(request, 'La contraseña no coincide con la confirmacion de contraseña!')
            return redirect('cambiar_contrasena')
    return render(request, 'cuentas/cambiar_contrasena.html')