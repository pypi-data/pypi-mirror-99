from otrs_somconnexio.otrs_models.adsl_ticket import ADSLTicket
from otrs_somconnexio.otrs_models.fiber_ticket import FiberTicket
from otrs_somconnexio.otrs_models.mobile_ticket import MobileTicket
from otrs_somconnexio.exceptions import ServiceTypeNotAllowedError


class TicketFactory(object):
    """ This factory is to generate the concrete ticket with his internal logic based on
        the service of the EticomContract.
    """
    def __init__(self, service_data, customer_data):
        self.service_data = service_data
        self.customer_data = customer_data

    def build(self):
        """ Create a OTRS Process Ticket with the information of the ServiceData and return it. """
        if self.service_data.type == 'adsl':
            TicketClass = ADSLTicket
        elif self.service_data.type == 'fiber':
            TicketClass = FiberTicket
        elif self.service_data.type == 'mobile':
            TicketClass = MobileTicket
        else:
            raise ServiceTypeNotAllowedError(self.service_data.order_id, self.service_data.type)

        return TicketClass(
            service_data=self.service_data,
            customer_data=self.customer_data
        )
