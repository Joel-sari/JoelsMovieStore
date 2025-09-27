from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#We import login_required, which is a decorator to ensure that only authenticated users can access specific view functions. A Django decorator is a function that wraps another function or method to modify its behavior. Decorators are commonly used for things such as authentication, permissions, and logging.
@login_required
#We create the logout function, which uses the login_required decorator. This means that only authenticated users can access this function.
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    from django.contrib import messages
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
         {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            # The old check for user.profile.security_phrase has been removed
            # because signup now always creates a security question and answer,
            # so this check is no longer necessary.
            auth_login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('home.index')



# We imported UserCreationForm, which is a built-in form class provided by Django. It is designed to facilitate the creation of user registration forms, specifically to create new user accounts.
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

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
            # Save the user object first
            user = form.save()

            # ✅ Create a profile immediately with security question + answer
            Profile.objects.create(
                user=user,
                security_question=form.cleaned_data['security_question'],
                security_answer=form.cleaned_data['security_answer']
            )

            # Redirect to login page after successful signup
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


# Settings view for user profile management
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def settings(request):
    updated = False
    # Ensure the user has a related profile object; if not, create one.
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        from .models import Profile
        profile = Profile.objects.create(user=request.user)

    # If the request is a POST, process the submitted form data.
    if request.method == 'POST':
        # Bind the form to POST data and the existing profile instance.
        form = ProfileForm(request.POST, instance=profile)
        # Validate the form.
        if form.is_valid():
            # Save the updated profile data.
            form.save()
            updated = True
    else:
        # If GET request, instantiate the form with the current profile instance.
        form = ProfileForm(instance=profile)

    # Render the settings template with the form.
    return render(request, 'accounts/settings.html', {'form': form, 'updated': updated})


# Security phrase verification view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



#
# Forgot Password Step 1: This view is the entry point for users who have forgotten their password.
# It displays a form prompting for a username. On POST, it checks if the username exists.
# If found, it redirects to the security verification step (step 2). If not, it displays an error.
def forgot_password(request):
    """
    Step 1 of the forgot password flow.
    Renders a form asking for the user's username. On POST, checks if the user exists,
    then redirects to the verify_security view if found.
    """
    template_data = {}
    if request.method == "GET":
        # GET: Show the form to enter username
        return render(request, "accounts/forgot_password.html", template_data)
    elif request.method == "POST":
        # POST: Process the submitted username
        username = request.POST.get("username")
        user = None
        if username:
            try:
                # Try to find the user by username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
        if user:
            # If user exists, redirect to verify_security, passing username as GET param
            return redirect(f"{reverse('accounts.verify_security')}?username={user.username}")
        else:
            # If not found, show error on the same form
            template_data["error"] = "No user found with that username."
            return render(request, "accounts/forgot_password.html", template_data)


#
# Forgot Password Step 2: This view handles security question verification.
# It receives a username (from GET or POST), fetches the user and their profile,
# and prompts for the security answer. On POST, it checks the answer and either
# redirects on success or shows an error.
def verify_security(request):
    username = request.GET.get("username") or request.POST.get("username")
    user = None
    profile = None
    if username:
        try:
            user = User.objects.get(username=username)
            profile = user.profile
        except User.DoesNotExist:
            return redirect("accounts.forgot_password")
        except Exception:
            return redirect("accounts.forgot_password")
    else:
        return redirect("accounts.forgot_password")

    if request.method == "POST":
        answer = request.POST.get("security_answer")
        if answer and answer.strip().lower() == (profile.security_answer or "").strip().lower():
            # ✅ Log the user in before redirect
            auth_login(request, user)
            # ✅ Add a success message
            messages.success(request, "✅ You have been logged in successfully!")
            return redirect('home.index')
        else:
            return render(
                request,
                "accounts/verify-security.html",
                {
                    "profile": profile,
                    "username": username,
                    "error": "❌ Incorrect answer. Please try again."
                }
            )

    return render(request, "accounts/verify-security.html", {"profile": profile, "username": username})