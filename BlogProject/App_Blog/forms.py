from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add class directly to the field widget (flexible approach)
        self.fields['comment'].widget.attrs.update({'class': 'form-control','rows': 2,'class':'mt-3'})

        # Optional error handling for robust validation (improves user experience)
        if self.errors:
            self.fields['comment'].widget.attrs.update({'class': 'form-control is-invalid'})
