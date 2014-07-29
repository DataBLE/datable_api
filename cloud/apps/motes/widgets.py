import floppyforms as forms

class BaseESRIWidget(forms.gis.BaseGeometryWidget):
    map_srid = 3857
    template_name = 'motes/gis/esri.html'

    class Media:
        js = (
                'js/OpenLayers.js',
                'floppyforms/js/MapWidget.js',
             )

class PointWidget(forms.gis.PointWidget, BaseESRIWidget):
        pass


