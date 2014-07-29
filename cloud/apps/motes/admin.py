from django.conf import settings
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from models import Mote, App, GenderAction, Location, Sighting
from widgets import PointWidget


class GenderActionInline(admin.TabularInline):
    model = GenderAction


class MoteAdmin(admin.ModelAdmin):
    inlines = [GenderActionInline,]
    list_display = ('name', 'uuid', 'major', 'minor')
    search_fields = ('name', 'uuid', 'major', 'minor')
    exclude = ('rssi',)


class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'platform')
    search_fields = ('name', 'identifier', 'platform')
    list_filter = ('platform',)


class MoteInline(admin.TabularInline):
    model = Mote
    extra = 0
    readonly_fields = ('edit_actions',)

    def edit_actions(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.module_name),  
            args=[instance.pk] )
        return mark_safe(u'<a href="{u}">Edit</a>'.format(u=url))


class LocationAdmin(admin.ModelAdmin):
    inlines = [MoteInline,]
    formfield_overrides = {
            models.PointField: {'widget': PointWidget}
            }

    def get_form(self, request, obj=None, **kwargs):
        form = super(LocationAdmin, self).get_form(request, obj, **kwargs)
        return form


class SightingAdmin(admin.ModelAdmin):
    readonly_fields = ('app', 'mote', 'date', 'address', 'location', 'log_info')
    list_display = ('mote', 'app', 'address', 'date', 'log_info')
    search_fields = ('mote', 'app', 'address')
    list_filter = ('date', 'app__platform')

    class Media:
        # We're not really a geoform, so include these so 'location' 
        # readonly widget works propertly
        js = ('js/OpenLayers.js', 'floppyforms/js/MapWidget.js')
    
    def address(self, instance):
        return mark_safe('%s, %s, %s %s' % (instance.mote.location.address, 
                instance.mote.location.city, instance.mote.location.state, 
                instance.mote.location.postal_code,))

    def location(self, instance):
        widget = PointWidget()
        return mark_safe(widget.render('point', instance.mote.location.point,
                attrs={'id':'id_point'}).replace('\n', ''))

    def log_info(self, instance):
        return mark_safe(instance.message)
    

admin.site.register(Location, LocationAdmin)
admin.site.register(Mote, MoteAdmin)
admin.site.register(App, AppAdmin)
admin.site.register(Sighting, SightingAdmin)
