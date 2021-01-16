from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login , logout 
from datetime import datetime
from django.contrib.auth.models import User
from .forms import UserForm
from home.models import Contact
from django.contrib import messages
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.core.files import File
import os
from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from .models import Contact
from .serializers import RestaurantSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser




class RestaurantApiView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    def get(self, request):
        restaurants= Contact.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


data = None
url = None


# Create your views here.
def index(request):
    context = {"home": "active"}
    return render(request, 'index.html', context)



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Form has been Submitted')
    return render(request, 'contact.html')


def signup(request):
    if request.method == "POST":
        form1 = UserForm(request.POST)
        if form1.is_valid():
            username = form1.cleaned_data['username']
            first_name = form1.cleaned_data['first_name']
            last_name = form1.cleaned_data['last_name']
            email = form1.cleaned_data['email']
            password = form1.cleaned_data['password']
            
            User.objects.create_user(username=username,email=email, first_name=first_name, last_name=last_name, password=password,)
            return HttpResponseRedirect('/login')
    else:
        form1 = UserForm()
    return render(request, 'signup.html',{'frm':form1})
    


def handlelogin(request):
    if request.method == "POST":
        username = request.POST['username']
        loginpassword = request.POST['loginpass']
        
        user = authenticate(username=username, password=loginpassword)

        if user is not None:
            login(request, user)
            return redirect('/')
        else: 
            messages.error(request, "Credentials do not match, Try again")
    return render(request, 'login.html')

    

def handlelogout(request):
    logout(request)
    return redirect('login')




def pdf_to_txt(request):
    if request.method == "POST":
        p = request.FILES['pdf']
        # file_path = 'C:\\Users\\AA\\Desktop\\sample.pdf'
        pdf = PdfFileReader(p)
        with open(os.path.join('static/yourtxt.txt'), 'w') as f:
            f = File(f)
            for page_num in range(pdf.numPages):
                # print('Page: {0}'.format(page_num))
                pageObj = pdf.getPage(page_num)
        
                try: 
                    txt = pageObj.extractText()
                    # print(''.center(100, '-'))
                except:
                    pass
                else:
                    f.write('\n')
                    f.write(''.center(100, '-'))
                    f.write('\n')
                    f.write('Page {0}\n'.format(page_num+1))
                    f.write(txt)
            f.closed
        return render(request, 'pdf_to_txt.html',{'f':f})
    else:
        return render(request, 'pdf_to_txt.html')


        


# with open('/path/to/hello.world', 'w') as f:
# ...     myfile = File(f)
# ...     myfile.write('Hello World')
# ...
# >>> myfile.closed