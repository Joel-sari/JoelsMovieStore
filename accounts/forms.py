from django.contrib.auth.forms import UserCreationForm
#We create a new class named CustomUserCreationForm, which inherits from UserCreationForm, making it a subclass of Django’s built-in user creation form.
from django.forms.utils import ErrorList
#We import the ErrorList class, which is a default class used to store and display validation error messages associated with form fields.
from django.utils.safestring import mark_safe
#We import the mark_safe function, which is used to mark a string as safe for HTML rendering, indicating that it doesn’t contain any harmful content and should be rendered as-is without escaping.

#We define a new class named CustomErrorList, which extends Django’s ErrorList class.
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        
        #We override the __str__() method of the base ErrorList class. If the error list is empty (i.e., there are no errors), it returns an empty string, indicating that no HTML should be generated. Otherwise, it defines a custom HTML code that uses <div> elements and Bootstrap CSS classes to improve the way the errors are displayed. It also uses the mark_safe function to render the code as-is.
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    
    #We define the class constructor (the __init__ method). The constructor calls the constructor of the parent class (UserCreationForm) through the super method.
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        #Then, we iterate through the fields provided by UserCreationForm. These are 'username', 'password1', and 'password2'. For each field specified in the loop, we set the help_text attribute to None, which removes any help text associated with these fields. Finally, for each field specified in the loop, we add the CSS form-control class to the field’s widget. This is a Bootstrap class that improves the look and feel of the fields.
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )


# ProfileForm: A Django ModelForm for editing user profile information.
# This form is connected to the Profile model and allows users to update
# their first name, last name, favorite movie, security question, and security answer.
# By using ModelForm, we leverage Django's automatic form generation based on model fields,
# ensuring tight integration between the form and the database model.
# The widgets dictionary is used to apply the Bootstrap 'form-control' class to each field,
# providing consistent and attractive styling for all form inputs.
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    A form for editing Profile model information.
    Inherits from forms.ModelForm to automatically generate fields
    based on the Profile model, ensuring consistency and reducing boilerplate.
    This form includes fields for first name, last name, favorite movie,
    security question, and security answer.
    The widgets parameter applies Bootstrap's 'form-control' CSS class to each field
    for improved UI/UX.
    """
    class Meta:
        model = Profile  # Connects this form to the Profile model
        fields = ['first_name', 'last_name', 'favorite_movie', 'security_question', 'security_answer']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'favorite_movie': forms.TextInput(attrs={'class': 'form-control'}),
            'security_question': forms.Select(attrs={'class': 'form-control'}),
            'security_answer': forms.TextInput(attrs={'class': 'form-control'}),
        }