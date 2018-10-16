from django import forms


class SearchSeriesForm(forms.Form):
    """Form to search for series."""

    search_term = forms.CharField(label='Search shows…', max_length=200)
