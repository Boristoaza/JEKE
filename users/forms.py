from django import forms
from django.utils import timezone
from .models import Image


class CreateEvent(forms.Form):
    name_event = forms.CharField(
        label="Create event",
        max_length=225
    )

    category = forms.CharField(
        label="Category",
        max_length=225
    )

    first_name = forms.CharField(
        label="First name",
        max_length=100
    )

    second_name = forms.CharField(
        label="Second name",
        max_length=100
    )

    description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        max_length=225
    )

    selected_date = forms.DateTimeField(
        label="Date"
    )

    def clean_selected_date(self):
        selected_date = self.cleaned_data.get("selected_date")
        now = timezone.now()

        if selected_date < now:
            raise forms.ValidationError(
                "La fecha no puede ser menor a la fecha actual"
            )

        return selected_date


# =================

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name_image', 'image']