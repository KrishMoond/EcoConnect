from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    interests_input = forms.CharField(
        required=False,
        help_text='Enter interests separated by commas',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., renewable energy, recycling, gardening'})
    )
    
    class Meta:
        model = Profile
        fields = ['location', 'skills']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['interests_input'].initial = ', '.join(self.instance.interests) if self.instance.interests else ''
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        interests_str = self.cleaned_data.get('interests_input', '')
        if interests_str:
            profile.interests = [interest.strip() for interest in interests_str.split(',') if interest.strip()]
        else:
            profile.interests = []
        if commit:
            profile.save()
        return profile
