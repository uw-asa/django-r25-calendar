import logging
import re
from datetime import date, timedelta

from authz_group import Group
from dateutil import parser
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from uw_r25.models import Reservation, Space
from uw_r25.reservations import get_reservations
from uw_r25.spaces import get_spaces

logger = logging.getLogger(__name__)


@login_required
def space_reservations(request, space_name=None, res_date=None):
    user = request.user.username
    if not Group().is_member_of_group(user, settings.R25CAL_VIEWER_GROUP):
        return HttpResponseRedirect("/")

    reservations = None
    space = None
    rooms = []

    date_this = parser.parse(res_date) if res_date else date.today()
    date_prev = date_this - timedelta(days=1)
    date_next = date_this + timedelta(days=1)

    try:
        space_list = get_spaces()
    except Exception as ex:
        context = {
            'supporttools_user': 'nobody',
            'messages': ['Error: Could not contact R25 Web Service: %s' % (
                str(ex)
            )],
        }

        return render(request, 'r25_calendar/space-reservations.html', context)

    if space_name:
        space_name = re.sub(r'\+', ' ', space_name)

        for sp in space_list:
            if sp.name == space_name:
                space = sp
                break
            if sp.name_fixed() == space_name:
                space = sp
                break
            if ''.join(sp.name.split()) == space_name:
                space = sp
                break

    if space:
        try:
            reservations = get_reservations(
                space_id=space.space_id,
                start_dt=date_this.strftime('%Y-%m-%d'),
                end_dt=date_this.strftime('%Y-%m-%d'))
        except Exception as ex:
            context = {
                'supporttools_user': 'nobody',
                'messages': ['Error: Could not contact R25 Web Service: %s' % (
                    str(ex)
                )],
            }

            return render(request, 'r25_calendar/space-reservations.html',
                          context)

    else:
        for sp in sorted(space_list, key=Space.name_fixed):
            name = sp.name_fixed()
            name = name.split(' ', 1)
            bldg = name.pop(0)
            rm = ' '.join(name)
            if space_name is None or bldg == space_name:
                room = {'building': bldg, 'name': rm, 'space': sp}
                rooms.append(room)

    context = {
        'supporttools_user': 'nobody',
        'rooms': rooms,
        'space_name': space_name,
        'buildings': sorted(set(room['building'] for room in rooms)),
        'space': space,
        'date_this': date_this,
        'date_prev': date_prev,
        'date_next': date_next,
        'reservations': reservations,
    }

    return render(request, 'r25_calendar/space-reservations.html', context)


def _space_name_fixed(self):
    name = self.name
    name = re.sub(r'^ADMC', 'ADMC ', name)
    name = re.sub(r'^BIOE', 'BIOE ', name)
    name = re.sub(r'^GNOM', 'GNOM ', name)
    name = re.sub(r'^HSRR', 'HSRR ', name)
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'^SNAIL$', 'DISC SNAIL', name)
    name = re.sub(r'^ZZZ-', '', name)
    name = re.sub(r'/', '-', name)
    name = name.strip()

    return name


def _reservation_start_datetime_parsed(self):
    return parser.parse(self.start_datetime)


def _reservation_end_datetime_parsed(self):
    return parser.parse(self.end_datetime)


Space.name_fixed = _space_name_fixed
Reservation.start_datetime_parsed = _reservation_start_datetime_parsed
Reservation.end_datetime_parsed = _reservation_end_datetime_parsed
