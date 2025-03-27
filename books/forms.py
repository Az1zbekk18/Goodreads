from django import forms
from .models import BookReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['comment', 'stars_given']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your review...'}),
            'stars_given': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'})
        }
