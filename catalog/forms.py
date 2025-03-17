import datetime
from django import forms

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default is 3 weeks)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if date is not in the past
        if data < datetime.date.today():
            raise forms.ValidationError('Invalid date - renewal in past')

        # Check if date is in the allowed range (4 weeks max)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError('Invalid date - renewal more than 4 weeks ahead')

        return data
