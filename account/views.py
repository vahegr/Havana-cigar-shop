# import requests
# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
# from django.http import JsonResponse
# from django.urls import reverse_lazy
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from .tokens import account_activation_token
# from django.core.mail import EmailMessage
# from django.views import View
# from django.views.generic import DetailView, CreateView
# from .forms import LogInForm, EditProfileForm, UserCreationForm
# from .models import User, UserFollowing
#
#
# class UserRegister(CreateView):
#     form_class = UserCreationForm
#     template_name = "account/register.html"
#     success_url = reverse_lazy('home:home')
#
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('home:home')
#         return super(UserRegister, self).get(*args, **kwargs)
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(self.request)
#         mail_subject = 'فعال سازی اکانت'
#         message = render_to_string('account/account_activate.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
#         to_email = form.cleaned_data.get('email')
#         email = EmailMessage(
#             mail_subject, message, to=[to_email]
#         )
#         email.send()
#         return render(self.request, "account/email_sent.html")
#
#
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return HttpResponse('اکانت شما با موفقیت فعال شد.')
#     else:
#         return HttpResponse('لینک فعال سازی منقضی شده است!')
#
#
# class UserLogIn(View):
#     def get(self, request):
#         if request.user.is_authenticated is True:
#             return redirect('home:home')
#         form = LogInForm()
#         return render(request, 'account/login.html', context={'form': form})
#
#     def post(self, request):
#         if request.user.is_authenticated is True:
#             return redirect('home:home')
#         form = LogInForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['email'], password=cd['password'])
#             if user is not None:
#                 login(request, user)
#                 return redirect('home:home')
#             else:
#                 form.add_error('email', 'اطلاعات وارد شده اشتباه است')
#         else:
#             form.add_error('email', 'اطلاعات وارد شده اشتباه است')
#
#         return render(request, 'account/login.html', context={'form': form})
#
#
# class UserLogOut(View):
#     def get(self, request):
#         logout(request)
#         return redirect('home:home')
