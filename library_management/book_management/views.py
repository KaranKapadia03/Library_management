from typing import Any, Dict
from django.contrib.auth.models import User
from book_management.models import UserID
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import  DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django_tables2 import SingleTableView
from book_management.forms import UserIDform, UserForm, BookFormSet,BookRequestForm1,SportForm,MenForm
from book_management.models import Books,BookRequest,UserID,User,Sports,men
from book_management.tables import BookRequestTable2, BookTable,BookRequestTable,BookRequestTable1,SPORTSTABLE,MENTABLE
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
import xlsxwriter
from book_management.filter import filterninja
from django_filters.views import FilterView
from book_management.forms import BookRequestForm
from django.db.models import Q
from django.shortcuts import render
import pdfkit
from django.http import HttpResponse
from .models import Books
import os
from library_management.settings import TEMP_DIR,BASE_DIR
TEMP_DIR = os.path.join(BASE_DIR, 'templates')
from django.core.mail import EmailMessage


 
# def send_welcome_email(request):
#     subject = 'Welcome to My Site'
#     message = 'Thank you for creating an account!'
#     from_email = 'teacher0000000001@gmail.com'
#     recipient_list = [request.user.email]
#     send_mail(subject, message, from_email, recipient_list)



def generate_pdf(request):
    # Fetch data from the models
    report_data = Books.objects.all()
    report_data2 = BookRequest.objects.all()
    report_data3 = UserID.objects.all()

    # Pass data to the template
    context = {'report_data': report_data, 'report_data2': report_data2, 'report_data3': report_data3}

    # Render HTML template to a string
    html_template = 'book_management/pdf_template.html'
    html_content = render(request, html_template, context).content.decode('utf-8')

    # Specify the path to the wkhtmltopdf executable
    # wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    wkhtmltopdf_path = os.path.join(TEMP_DIR, 'book_management', 'wkhtmltopdf','bin','wkhtmltopdf.exe')

    # Set up the configuration as a dictionary
    configuration = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    # Add header and footer options
    options = {
        'header-html': os.path.join(TEMP_DIR, 'book_management', 'headerpdf.html'),  # Replace with the path to your header HTML file
        'footer-html': os.path.join(TEMP_DIR, 'book_management', 'footerpdf.html'),  # Replace with the path to your footer HTML file
    }

    # Use pdfkit to generate PDF from HTML content with the specified path and options
    pdf_content = pdfkit.from_string(html_content, False, configuration=configuration, options=options)

    # Prepare response for download
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output_report.pdf"'

    return response




def export_to_excel(request):
    # Fetch data from your model
    data = Books.objects.all()
    output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    output['Content-Disposition'] = 'attachment; filename=BOOK_DATA.xlsx'
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("BOOK LOVERS")
    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    # Write headers
    headers = ['Author', 'Name_of_Book', 'Available']  # Replace with your actual field names
    bold_format = workbook.add_format({'bold': True,'font_color': '#D3D3D3'})
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header, bold_format)
    # Write data from the model to the worksheet
    row_num = 1
    for row_data in data:
        worksheet.write(row_num, 0, row_data.Author)  # Replace with your actual field names
        worksheet.write(row_num, 1, row_data.Name_Of_Book)
        if row_data.Available:
            available_value = 'Yes'
        else:
            available_value="NO" 
        worksheet.write(row_num, 2, available_value)
        row_num += 1
    # Save the workbook.
    workbook.close()
    # Create a response to return the Excel file
    response = FileResponse(output)
    response['Content-Disposition'] = 'attachment; filename=Book_data.xlsx'
    return response

#def registeration(request):
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        user_id_form=UserIDform(data=request.POST)
        if user_form.is_valid() and user_id_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=user_id_form.save(commit=False)
            profile.user=user
            profile.save()
            return index(request)

        else:

            print(user_form.errors, user_id_form.errors)

    else:
        user_form = UserForm()
        user_id_form = UserIDform()

    return render(request, 'room/registeration.html', {'u': user_form, 'w': user_id_form})


#deklena mast hai
class BookRequested(CreateView):
    model=BookRequest
    template_name='book_management/BookRequest.html'
    pk_url_kwarg = 'pk'
    form_class=BookRequestForm

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super(BookRequested, self).get_form_kwargs()
        kwargs['user_type'] = self.request.user.userid.user_type
        return kwargs
    def form_valid(self, form):
        book = get_object_or_404(Books, pk=self.kwargs['pk'])
        form.instance.book = book        
        form.instance.generated_by = self.request.user        
        student_email = self.request.user.email  # Student's email
        teacher_email = form.cleaned_data['generated_for'].email  # Teacher's email
        generated_for=form.cleaned_data['generated_for']

        message_1=f'''Dear {self.request.user},
        
        YOU HAVE REQUESTED FOR :-
        Book:{book}
        Author:{book.Author}
        REQUEST TRANSECTION:-
        Genered by:{self.request.user}
        Generated for:{generated_for}'''
        email = EmailMessage(
            f'Conformation Request Mail for {self.request.user}',
            message_1,
            'kapadiakaran.20.ce@iite.indusuni.ac.in',
            [student_email],
            cc=[teacher_email],
            reply_to=[student_email],
        )
        email.send(fail_silently=False)
        karan=BookRequest.objects.order_by('id')

        obj=form.save()
        print(f'here is the: {obj}')
        print(f'here is the obj id: {obj.id}')
        
        

        link = f'<a href="http://127.0.0.1:8000/r/trf/book_request/{obj.id}/">Click me</a>'       
        message_2=f'''Dear {generated_for},<br>
        
        <b>You have  gotten a request for:-</b> 
        <br>
        Book:{book}<br>
        Author:{book.Author}<br>
        From:{self.request.user}<br>
        Please approve/deny the request-----><br>
        {link}
        '''
        email = EmailMessage(
            f'Request from {self.request.user}',

            message_2,
            'kapadiakaran.20.ce@iite.indusuni.ac.in',
            [teacher_email],
            cc=[teacher_email],
            reply_to=[teacher_email],
        )
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        return super().form_valid(form)
    def get_success_url(self) -> str:
        return reverse_lazy('book_management:TeacherRequestAnswere')
    




class FormFIll(CreateView):
    model = Books
    fields = ['Author', 'Name_Of_Book', 'Available','Geners']
    template_name = 'book_management/forms.html'
    success_url = reverse_lazy('book_management:FormsShow')
    def get_success_url(self) -> str:
        return  reverse_lazy('book_management:FormsShow')
   

class AddMultipleBookView(CreateView):
    model = Books
    fields = []
    template_name = 'book_management/mulforms.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['book_formset'] = BookFormSet(self.request.POST, queryset=Books.objects.none(),prefix='book_formset')
        else:
            context['book_formset'] = BookFormSet(queryset=Books.objects.none(),prefix='book_formset')
        return context
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        BookFormSet = context['book_formset']
        if BookFormSet.is_valid():
            BookFormSet.save()
            return HttpResponseRedirect('/')
        else:
            context['book_formset'] = BookFormSet
            return render(self.request, "book_management/mulforms.html", context)

class BookTableView(FilterView,SingleTableView):
    model = Books
    table_class = BookTable
    template_name = 'book_management/formsshow.html'
    filterset_class=filterninja

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(BookTableView, self).get_queryset()
        print(self.request.user.userid.user_type)
        if self.request.user.userid.user_type == 'student':
            queryset = queryset.filter(Available=True)
        return queryset    

class BookDetailView(DetailView):
    model = Books
    template_name = 'book_management/detailview.html'
    pk_url_kwarg = 'pk'


class Updateview(UpdateView):
    model = Books
    fields = ['Author', 'Available', 'Name_Of_Book']
    template_name = "book_management/forms.html"
    pk_url_kwarg = 'pk'
       
    def get_success_url(self):
        # Redirect to the BookDetailView for the updated book
        return reverse_lazy('book_management:BookDetailView', kwargs={'pk': self.object.pk})
    
class Deleteview(DeleteView):
    model = Books
    success_url = reverse_lazy("book_management:FormsShow")
    pk_url_kwarg = 'pk'
    template_name = "book_management/forms.html"
 
class UpdateRequestView(UpdateView):
    model = BookRequest
    form_class = BookRequestForm1
    template_name='book_management/updaterequestview.html'
    pk_url_kwarg='pk'
    
    def form_valid(self, form):
        # Access the object being updated
        instance = form.save(commit=False)
        print(instance.status)
        if instance.status == 'accepted':
        
            print(instance.book.Available)
            instance.book.Available = False
            instance.book.save()


        # Save the changes to the BookRequest model
        instance.save()
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book_management:trf')



class profileview(TemplateView):
    template_name='book_management/userprofile.html'

class TeacherRequest(SingleTableView):
    model=BookRequest
    table_class=BookRequestTable
    template_name='book_management/teachertable.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset= super(TeacherRequest,self).get_queryset()
       
        queryset=BookRequest.objects.filter(status='requested',generated_for=self.request.user)
        print(queryset)
        return queryset    

class StudentRequestAnsweres(SingleTableView):
    model=BookRequest
    table_class=BookRequestTable1
    template_name='book_management/StudentRequestAnsweres.html'
    q=BookRequest.objects.order_by("book")
    for a in q:
        #  print('Book:',a.book)
        #  print('STATUS:',a.status)
        #  print('AVAILABLE:',a.book.Available)  
         if a.status == 'accepted':
            a.book.Available=False
            a.book.save()
            # print("AVAILABLE UPDATED",a.book.Available)
         elif a.status == "denied":
             a.book.Available=True
            #  print("Available Updated",a.book.Available)    
             a.book.save()   
    def get_queryset(self) -> QuerySet[Any]:
        queryset= super().get_queryset()
        queryset=BookRequest.objects.filter(Q(status='accepted')| Q(status='denied'),generated_for=self.request.user)
        return queryset

class TeacherRequestAnswere(SingleTableView):
    model=BookRequest
    table_class=BookRequestTable2
    template_name='book_management/TeacherRequestAnswere.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset= super().get_queryset()    
        queryset=BookRequest.objects.filter(generated_by=self.request.user)

        return queryset

from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
import pandas as pd
from .models import Books

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded Excel file
            excel_file = request.FILES['excel_file']
            data = pd.read_excel(excel_file)

            # Save the data to the Books model
            for index, row in data.iterrows():
                Books.objects.create(
                    Author=row['Author'],
                    Name_Of_Book=row['Name_Of_Book'],
                    Available=row['Available'],
                    Geners=row['Geners']
                )

            return redirect('book_management:FormsShow')  # Redirect to a success page or another view
    else:
        form = ExcelUploadForm()

    return render(request, 'book_management/upload_excel.html', {'form': form})

class UserRegisterCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'book_management/registeration.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_id_form'] = UserIDform(self.request.POST)
        else:
            context['user_id_form'] = UserIDform()
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = self.get_context_data()
        user_id_form = context['user_id_form']
        if form.is_valid() and user_id_form.is_valid():
            obj = form.save()
            print(f'ye save wala nai hais :{obj.email},{obj.password},{obj.username}')
            obj.set_password(obj.password)
            obj.save()
            obj2 = user_id_form.save(commit=False)
            obj2.user = obj
            obj2.save()
            print(obj2.user)
            print(obj2.user_type)
      
        
            return HttpResponseRedirect(reverse_lazy('book_management:login'))

        else:
            return render(self.request, self.template_name, self.get_context_data(form=form, user_id_form=user_id_form))

class FOREMY1(CreateView):
    model=Sports
    form_class=SportForm
    template_name='book_management/FORMEY1.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context= super().get_context_data(**kwargs)
        if self.request.POST:
            
            context['Men_Form']=MenForm(self.request.POST)
        else:
            
            context['Men_Form']=MenForm()
        return context

    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context=self.get_context_data()
        Men_Form=context['Men_Form']
        if form.is_valid() and Men_Form.is_valid():
            formobj=form.save()
            formobj.save()
            print(formobj)
            print(formobj.sports_name)
            print(formobj.player_name)
            menformobj=Men_Form.save(commit=False)
            menformobj.name=formobj
            menformobj=Men_Form.save()
            menformobj.save()
            print(f'NAME:{menformobj.name},player_type:{menformobj.player_type},sports_name{menformobj.name.sports_name}')

            return HttpResponseRedirect( reverse_lazy("book_management:FORMEY2")) 
        else:
             return render(self.request, self.template_name, self.get_context_data(form=form,Men_Form=Men_Form ))

        
class CombinedTablesView(SingleTableView):
    template_name = 'book_management/FORMEY2.html'
    table_pagination = {'per_page': 10}  # Customize pagination if needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sports_table = SPORTSTABLE(Sports.objects.all())
        men_table = MENTABLE(men.objects.all())
        
        context['sports_table'] = sports_table
        context['men_table'] = men_table
        
        return context

class SportsTableshow(CombinedTablesView):
    model = Sports
    table_class = SPORTSTABLE

class Mentableshow(CombinedTablesView):
    model = men
    table_class = MENTABLE

class sportstabledetailview(DetailView):
    model = Books
    template_name = 'book_management/sportstabledetailview.html'
    pk_url_kwarg = 'pk'


        

def user_login(request):
    print(request.POST)
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('book_management:FormsShow'))
            else:
                return HttpResponse("account not active")
        else:
            print("someone tried and failed")
            return HttpResponse("INVALID LOGIN BRO")
    else:
        return render(request,'book_management/login.html',{})
@login_required

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('book_management:login'))    