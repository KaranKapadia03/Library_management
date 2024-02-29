import django_filters
from book_management.models import User,UserID,BookRequest
from book_management.models import Books
class filterninja(django_filters.FilterSet):
    
    User_geners={
        ('action','Action'),
        ('adventure','Adventure'),
        ('crime','Crime'),
        ('suspense','Suspense')
    }
    
    Author = django_filters.CharFilter(lookup_expr='icontains', label='Author')
    Name_Of_Book = django_filters.CharFilter(lookup_expr='icontains', label='Name of Book')
    Geners=django_filters.ChoiceFilter(choices=User_geners)
    Available = django_filters.BooleanFilter(label='Available') 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check the user type and conditionally exclude the 'Available' filter
        user_type = self.request.user.userid.user_type
        if user_type == 'student':
            del self.filters['Available']
    class Meta(): 
            model=Books
            fields=[] 


     
    
                
               
            
           

            