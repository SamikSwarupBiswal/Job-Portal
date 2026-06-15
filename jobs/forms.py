from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Job

class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    role=forms.ChoiceField(
        choices=(('seeker', 'Job Seeker'), ('employer', 'Employer')),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model=User
        fields=UserCreationForm.Meta.fields + ('email','role')

        #Styling every field using bootstrap css class
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""
        for field_name,field in self.fields.items():
            field.widget.attrs['class']='form-control'

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary', 'category']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        
