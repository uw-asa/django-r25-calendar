from dateutil import parser
from django.conf import settings
from django_ical.views import ICalFeed
from uw_r25.reservations import get_reservations
from uw_r25.spaces import get_spaces


class ReservationFeed(ICalFeed):
    """
    ical feed from R25 reservation data
    """
    product_id = '-//UW-IT CTE//R25//EN'

    def get_object(self, request, *args, **kwargs):
        feedobj = {
            'search': request.GET.dict()
        }

        if 'building' in kwargs and 'room' in kwargs:
            spaces = get_spaces(starts_with=kwargs['building'],
                                ends_with=kwargs['room'])
            feedobj['search']['space_id'] = spaces[0].space_id
            feedobj['space_name'] = spaces[0].name

        return feedobj

    def title(self, feedobj):
        if 'space_name' not in feedobj:
            return "R25 Reservation Calendar"

        return "%s - R25 Reservation Calendar" % \
               ' '.join(feedobj['space_name'].split())

    def file_name(self, feedobj):
        if 'space_name' not in feedobj:
            return "reservations.ics"

        return "%s.ics" % '_'.join(feedobj['space_name'].split())

    def items(self, feedobj):
        return get_reservations(**feedobj['search'])

    def item_title(self, reservation):
        return reservation.event_name

    def item_description(self, reservation):
        return reservation.profile_name

    def item_link(self, reservation):
        return "%s/r25ws/servlet/wrd/run/reservation.xml?" \
               "rsrv_id=%s&otransform=browse.xsl" % \
               (settings.RESTCLIENTS_R25_HOST, reservation.reservation_id)

    def item_start_datetime(self, reservation):
        return parser.parse(reservation.start_datetime)

    def item_end_datetime(self, reservation):
        return parser.parse(reservation.end_datetime)

    def item_location(self, reservation):
        return reservation.space_reservation.name
