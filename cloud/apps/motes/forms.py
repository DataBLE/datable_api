from django import forms

from djchoices import DjangoChoices, ChoiceItem

from models import GenderAction, App, Mote, Sighting

class MoteListForm(forms.Form):
    app = forms.CharField(max_length=255) # App's BundleID/packageName
    lat = forms.FloatField()
    lon = forms.FloatField()
    distance = forms.FloatField(required=False)
    platform = forms.ChoiceField(choices=App.Platform.choices)

    def clean_distance(self):
        distance = self.cleaned_data.get('distance', 5)
        if not distance:
            distance = 5
        return distance

    def clean(self):
        app_id = self.cleaned_data.get('app')
        platform = self.cleaned_data.get('platform')
        # Does app exist
        try:
            self.cleaned_data['app'] = App.objects.get(identifier=app_id, 
                    platform=platform)
        except App.DoesNotExist:
            raise forms.ValidationError('Invalid application')
        return self.cleaned_data


class SightingForm(forms.Form):
    app = forms.CharField(max_length=255) # App's BundleID/packageName
    platform = forms.ChoiceField(choices=App.Platform.choices)
    mote = forms.CharField(max_length=255) # Mote's UUID
    major = forms.CharField(max_length=255) # Mote's major number
    minor = forms.CharField(max_length=255) # Mote's minor number
    uuid = forms.CharField(max_length=255, required=False) 
    response = forms.CharField(max_length=255, required=False) # Response from user
    
    def clean(self):
        cleaned_data = super(SightingForm, self).clean()
        app_id = cleaned_data.get('app')
        platform = cleaned_data.get('platform')
        mote_id = cleaned_data.get('mote')
        major = cleaned_data.get('major')
        minor = cleaned_data.get('minor')
        mote = None

        # Does app exist
        try:
            cleaned_data['app'] = App.objects.get(identifier=app_id, 
                    platform=platform)
        except App.DoesNotExist:
            raise forms.ValidationError('Invalid application')

        # Does mote exist
        try:
            # Make sure the mote is active
            mote = Mote.objects.get(uuid=mote_id, major=major, minor=minor, 
                    active=True)
            self.cleaned_data['mote'] = mote
        except Mote.DoesNotExist:
            raise forms.ValidationError('Invalid mote')
        return cleaned_data


class GenderActionForm(SightingForm):
    gender = forms.ChoiceField(choices=GenderAction.GenderChoices.choices)
    rssi = forms.FloatField(required=False, 
            help_text='Minimum value for action to execute')

    def clean_rssi(self):
        # If not given in the form, default to 0
        rssi = self.cleaned_data.get('rssi', 0)
        return rssi

