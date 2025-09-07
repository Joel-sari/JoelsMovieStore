from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#We import login_required, which is a decorator to ensure that only authenticated users can access specific view functions. A Django decorator is a function that wraps another function or method to modify its behavior. Decorators are commonly used for things such as authentication, permissions, and logging.
@login_required
#We create the logout function, which uses the login_required decorator. This means that only authenticated users can access this function.
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
         {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'],password = request.POST['password'])
        if user is None:
            template_data['error'] ='The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')



# We imported UserCreationForm, which is a built-in form class provided by Django. It is designed to facilitate the creation of user registration forms, specifically to create new user accounts.
from django.contrib.auth.forms import UserCreationForm
def signup(request):
    template_data = {}
    #We created our template_data variable and assigned it a title.
    template_data['title'] = 'Sign Up'

    #Then, we checked whether the current HTTP request method is GET. If it is a GET request, it means that it’s a user navigating to the signup form via the localhost:8000/accounts/signup URL, in which case we simply send an instance of UserCreationForm to the template. Finally, we rendered the accounts/signup.html template.
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
# Create your views here.

# We add an elif section. This section checks whether the HTTP request method is POST, indicating that the form has been submitted.
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,error_class=CustomErrorList)


        #The if form.is_valid() checks whether the submitted form data is valid, according to the validation rules defined in the UserCreationForm class. These validations include that the two password fields match, the password is not common, and the username is unique, among others.
        if form.is_valid():
        #If the form data is valid, form.save() saves the user data to the database. This means creating a new user account with the provided username and password. Also, we redirect the user to the home page based on the URL pattern name.
            form.save()
            return redirect('accounts.login')
        else:
        #If the form data is not valid, the else section is executed, and we pass the form (including the errors) to the template and render the accounts/signup.html template again.
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})


@login_required

#We use the login_required decorator to ensure that the user must be logged in to access the orders function.
def orders(request):
    #We define the orders function, which takes a request object as a parameter.
    template_data = {}
    template_data['title'] = 'Orders'
    #We define the template_data variable and assign it a title.
    #We retrieve all orders belonging to the currently logged-in user (request.user). The order_set attribute is used to access the related orders associated with the user through their relationship. Remember that there is a ForeignKey relationship between the User model and the Order model.
    
    #Finally, we pass the orders to the template and render it.
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})