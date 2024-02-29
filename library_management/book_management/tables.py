import django_tables2 as tables
from book_management.models import Books,BookRequest,men,Sports
from book_management import filter
from django.utils.html import format_html

class BookTable(tables.Table):
    DETAIL = tables.TemplateColumn('<a href="{% url "book_management:BookDetailView" pk=record.id %}"><i class="bi bi-info-circle"></i></a>')
    class Meta:
        model = Books
        template_name ="django_tables2/bootstrap.html"
        fields = ('Author','Name_Of_Book','Available','Geners','id')
        
class BookRequestTable(tables.Table):
    Permissions=tables.TemplateColumn('<a href="{% url "book_management:updateRequestView" pk=record.id %}"><button class="btn btn-warning btn-lg btn-block" type="button">UPDATE</button></a>')
    id=tables.Column(verbose_name='ID')
    class Meta:
        model = BookRequest
        template_name="django_tables2/bootstrap.html"
        fields=('book','generated_by','status',)
    

class BookRequestTable1(tables.Table):
   
    class Meta:
        model=BookRequest
        template_name="django_tables2/bootstrap.html"
        fields=('book','generated_by','status','id')
    
    def render_status(self,value,record):
        if value == "Requested":
            return format_html('<span class="badge bg-warning">{}</span>', value)
        elif value == "Accepted":
            return format_html('<span class="badge bg-success">{}</span>', value)
        elif value == "Denied":
            return format_html('<span class="badge bg-danger">{}</span>', value)
        else:
            return value
    

class BookRequestTable2(tables.Table):
    
    class Meta:
        model=BookRequest
        template_name='django_tables2/bootstrap.html'
        fields=('book','generated_for','status','id')
        
    def render_status(self,value,record):
        if value == "Requested":
            return format_html('<span class="badge bg-warning">{}</span>', value)
        elif value == "Accepted":
            return format_html('<span class="badge bg-success">{}</span>', value)
        elif value == "Denied":
            return format_html('<span class="badge bg-danger">{}</span>', value)
        else:
            return value
    



class SPORTSTABLE(tables.Table):
    player_type = tables.Column(accessor='men_set.first.player_type', verbose_name='Player Type')
    future_name = tables.Column(accessor='men_set.first.name', verbose_name='Future Name')
    future_sports = tables.Column(accessor='men_set.first.name.sports_name', verbose_name='Future Sports')
    
    class Meta:
        model=Sports
        template_name='django_tables2/bootstrap.html'
        fields=('sports_name','player_name')
    def render_player_type(self, value, record):
        if value == 'coach':
              return format_html('<span class="badge bg-primary">{}</span>', value)
        elif value == 'player':
            return format_html('<span class="badge bg-success">{}</span>',value)
        else:
            return value
class MENTABLE(tables.Table):
    class Meta:
        model=men
        template_name='django_tables2/bootstrap.html'
        fields=('name','player_type','name__sports_name','name__player_name')
        