from django.shortcuts import render
# this creates more of the connection beteen the url home and the actual rendering 
def index(request):

    # here we are creating a Python dictionary that will be used to pass information from view functions to templates
    template_data = {}

    #title is the key
    template_data['title'] = 'Movies Store'

    # extending the return to have more than two variables, where 'index will have access to template_data variable'
    return render(request, 'home/index.html', {
        'template_data': template_data
    })
    

def about(request):
    template_data= {}
    template_data['title'] = 'About'
    #Again it changes the title of the webpage
    return render(request, 'home/about.html',{
        'template_data': template_data
    })

# Create your views here.
