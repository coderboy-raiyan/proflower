from django import forms
from .models import ReviewModel
from .constants import RATINGS


class ReviewForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    ratings = forms.ChoiceField(choices=RATINGS)

    class Meta:
        model = ReviewModel
        fields = ['content', 'ratings', 'flower', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flower'].disabled = True
        self.fields['flower'].widget = forms.HiddenInput()
        self.fields['user'].disabled = True
        self.fields['user'].widget = forms.HiddenInput()

        for field in self.fields:
            self.fields[field].widget.attrs.update({

                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
