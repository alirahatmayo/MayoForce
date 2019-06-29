from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser as User
from .models import Education, FamilyInfo, Profile
from .models import CustomUser as User
from posts.models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from posts.models import Post




class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', )

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


class EditProfileForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('gender', 'm_status', 'address', 'city', 'village', 'State', 'country', 'birth_date', 'cnic',  'avatar')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # self.fields['avatar'].required = False


class EditEducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = ('school', 'qualification', 'fieldOfStudy', 'dateFrom', 'dateTo', 'current', 'graduated')
        labels = {
            'school': 'Institute',
            'qualification': 'Qualification',
            'fieldOfStudy': 'Field Of Study',
            'dateFrom': 'From',
            'dateTo': 'To',
        }


    dateFrom = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    dateTo = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

class EditFamilyForm(UserChangeForm):

    class Meta:
        model = FamilyInfo
        fields = ('familychoice', 'name', 'm_status', )


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ( 'text',)
        # widgets = {'author': forms.HiddenInput()}
        labels = {

            'text': '',
        }
        # widget = forms.TextInput(
        #     attrs={'class': 'form-control', 'name': 'text', 'placeholder': 'Share what is on your mind',
        #            'styles': 'width: 100% !important;'},
        # ),
            # 'title': forms.HiddenInput()

