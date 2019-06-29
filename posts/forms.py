from django import forms

from posts.models import Post, Comment

class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['text']
        # widgets = {
        #     'text': forms.TextInput(attrs={
        #         'id': 'id_text',
        #         'class': 'form-control',
        #         'required': True,
        #         'placeholder': 'Say something...'
        #     }),
        # }


        # widgets = {'author': forms.HiddenInput()}
        # labels = {
        #
        #     'text': '',
        # }
        # widget = forms.TextInput(
        #     attrs={'class': 'form-control', 'name': 'text', 'placeholder': 'Share what is on your mind',
        #            'styles': 'width: 100% !important;'},
        # ),
            # 'title': forms.HiddenInput()




class CommentForm(forms.ModelForm):

    text = forms.CharField(
        label='',
        max_length=1000,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'commenttextarea', 'name': 'text', 'placeholder': 'comment', 'styles': 'width: 100% !important;', 'cols':'30', 'rows':'1' }
        )


    )

    class Meta:
        model = Comment
        fields = ('text', 'post')
        widgets = {'post': forms.HiddenInput()}