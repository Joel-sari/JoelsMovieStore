from django.contrib.auth.forms import UserCreationForm
# We create a new class named CustomUserCreationForm, which inherits from UserCreationForm, making it a subclass of Django’s built-in user creation form.
from django.forms.utils import ErrorList
# We import the ErrorList class, which is a default class used to store and display validation error messages associated with form fields.
from django.utils.safestring import mark_safe
# We import the mark_safe function, which is used to mark a string as safe for HTML rendering, indicating that it doesn’t contain any harmful content and should be rendered as-is without escaping.
from django import forms
from .models import Profile

#We define a new class named CustomErrorList, which extends Django’s ErrorList class.
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        
        #We override the __str__() method of the base ErrorList class. If the error list is empty (i.e., there are no errors), it returns an empty string, indicating that no HTML should be generated. Otherwise, it defines a custom HTML code that uses <div> elements and Bootstrap CSS classes to improve the way the errors are displayed. It also uses the mark_safe function to render the code as-is.
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    """
    Extended signup form that now also asks for a security question and answer.
    This ensures that users set up their recovery info during signup.
    """

    # New field: dropdown for choosing a security question
    security_question = forms.ChoiceField(
        choices=Profile.SECURITY_QUESTION_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # New field: text input for the security answer
    security_answer = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Remove help text and add Bootstrap styling for default fields
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    class Meta(UserCreationForm.Meta):
        model = UserCreationForm.Meta.model
        fields = ('username', 'password1', 'password2', 'security_question', 'security_answer')


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