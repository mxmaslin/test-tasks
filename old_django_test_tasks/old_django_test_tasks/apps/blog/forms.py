from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'title-field',
                    'placeholder': 'Введите название статьи'
                }
            ),
            'content': CKEditorWidget(attrs={'class': 'content-field'}),
            'image': forms.ClearableFileInput(attrs={'class': 'image-field'}),
        }
