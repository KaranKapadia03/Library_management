from django.core.management import BaseCommand
from models import BookRequest,Books,User,UserID
from forms import User,UserForm,UserIDform,TeacherRequestForm

class Command(BaseCommand):

    def handle(self, *args, **options):
        pass
