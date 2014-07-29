import datetime
import json
import socket
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from forms import GenderActionForm, MoteListForm, SightingForm
from models import GenderAction, Mote, Sighting

SEND_TO_MOTE_ACTIONS = [GenderAction.TypeChoices.tv_video, 
        GenderAction.TypeChoices.tv_image]

def json_response(x, status=200):
    '''Quick json response helper'''
    return HttpResponse(json.dumps(x, sort_keys=True, indent=2),
                        status=status,
                        content_type='application/json; charset=UTF-8')


@require_POST
@csrf_exempt
def mote_discovered(request, send_to_mote=False, first_sighting=True):
    '''Service used by the SDK to notify that a mote was found and a
    that probably a gender based action should be taken'''
    form = GenderActionForm(request.POST)
    if form.is_valid():
        app = form.cleaned_data.get('app')
        mote = form.cleaned_data.get('mote')
        gender = form.cleaned_data.get('gender')
        do_nothing_response = json_response({'action':None, 'question':None,
            'resource':None})

        try:
            # Get the active action
            action = GenderAction.objects.get(app=app, mote=mote, gender=gender,
                    active=True)
        except GenderAction.DoesNotExist:
            # No active action found, do nothing
            return do_nothing_response

        response_data = {'action':action.action_type, 
                'question':action.question,
                'resource':action.value,
                'repeat': True if action.mote.repeat_interval else False,
                'repeat_interval':action.mote.repeat_interval}

        # Log the sighting, but only when we see it for the first time
        if first_sighting:
            message = {'action': action.action_type, 'gender': gender, 
                    'confirmed':False}
            message_data = json.dumps(message)
            sighting = Sighting.objects.create(mote=mote, app=app, 
                    message=message_data)
            # Make sure to return sighting 
            response_data['uuid'] = sighting.uuid  

        if not first_sighting and action.action_type in SEND_TO_MOTE_ACTIONS:
            # The app doesn't need to do anything if displaying media on TV
            # First send data to mote, then return response to phone
            data = {'uuid':mote.uuid, 'major':mote.major, 'minor':mote.minor,
                    'action':action.action_type, 'question':action.question,
                    'resource':action.value}
            s = socket.create_connection(
                    (settings.SOCKET_HOST, settings.SOCKET_PORT), 3) #3s timeout
            s.send(json.dumps(data)+'\n')
            s.close()

        return json_response(response_data, status=200)
    return json_response({'errors': dict(form.errors.items())}, status=400)


@require_POST
@csrf_exempt
def mote_app(request):
    '''Service used by the SDK to get Mote IDs to sniff for a particular app'''
    form = MoteListForm(request.POST)
    if form.is_valid():
        app = form.cleaned_data.get('app')
        lat = form.cleaned_data.get('lat')
        lon = form.cleaned_data.get('lon')
        distance = form.cleaned_data.get('distance')
        point = Point(lon, lat, srid=4326)
        motes = Mote.objects.filter(
                location__point__distance_lte=(point, D(mi=distance)),
                genderaction__app=app).distinct().distance(point, field_name='location__point').order_by('distance')[:20]
        mote_list = []
        for mote in motes:
            mote_list.append({'uuid':mote.uuid, 'major':mote.major,
                'minor':mote.minor})
        return json_response({'motes':mote_list})
    return json_response({'errors': dict(form.errors.items())}, status=400)


@require_POST
@csrf_exempt
def mote_confirm(request):
    form = SightingForm(request.POST)
    if not form.is_valid():
        return json_response({'errors': dict(form.errors.items())}, status=400)
    app = form.cleaned_data.get('app')
    mote = form.cleaned_data.get('mote')
    uuid = form.cleaned_data.get('uuid')
    user_response = form.cleaned_data.get('response')

    # Action confirmed, update the sighting message
    try:
        sighting = Sighting.objects.get(uuid=uuid)
    except Sighting.DoesNotExist:
        return json_response({'errors': 'Invalid sighting uuid'}, status=400)

    message = json.loads(sighting.message)
    message['confirmed'] = True
    message['confirmed_time'] = datetime.datetime.now()
    message['user_response'] = user_response
    sighting.message = json.dumps(message, cls=DjangoJSONEncoder)
    sighting.save()
    send_to_mote = False
    return mote_discovered(request, first_sighting=False)


@require_POST
@csrf_exempt
def mote_sighting(request,):
    '''Service used by the SDK to notify that a mote was found'''
    form = SightingForm(request.POST)
    if form.is_valid():
        app = form.cleaned_data.get('app')
        mote = form.cleaned_data.get('mote')
        # Log the sighting
        sighting = Sighting.objects.create(mote=mote, app=app)
        return json_response({})
    return json_response({'errors': dict(form.errors.items())}, status=400)
