from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

class PetForm(forms.Form):
    name = forms.CharField(label='Name of the pet ', max_length=50)
    type = forms.CharField(label='What type of pet ', widget=forms.TextInput(attrs={'placeholder': "dog, cat, horse"}), max_length=50)
    memorable = forms.CharField(label='Tell us more about your pet ', widget=forms.Textarea(attrs={"rows":6, "cols": 70}))
    image = forms.ImageField()
