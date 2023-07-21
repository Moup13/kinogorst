from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str


from tokens import account_activation_token
from .forms import RegisterForm, LoginForm, CustomerForm
from accounts.models import User

from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode, urlsafe_base64_encode


def register_page(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        new_user = User.objects.create_user(email, password, username)
        activateEmail(request, new_user, form.cleaned_data.get('email'))
        if new_user is not None:
            messages.success(request, "Created User.")
            return redirect('accounts:login')

        messages.warning(request, "Create Error !")

    context = {
        "form": form
    }

    return render(request, "registration/signup.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            messages.warning(request, 'Credentials error.')

    return render(request, "registration/login.html", context)


def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        if user == True or user == False:
            user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("registration/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'registration/profile.html', context)
