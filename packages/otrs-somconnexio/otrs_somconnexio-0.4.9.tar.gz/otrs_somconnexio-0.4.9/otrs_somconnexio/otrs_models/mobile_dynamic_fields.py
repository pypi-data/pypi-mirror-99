from pyotrs.lib import DynamicField

from otrs_somconnexio.otrs_models.provision_dynamic_fields import ProvisionDynamicFields


class MobileDynamicFields(ProvisionDynamicFields):

    def _build_specific_dynamic_fields(self):
        return [
            self._line(),
            self._icc_sc(),
            self._icc_donor(),
            self._service_type(),
            self._previous_provider(),
            self._previous_owner_vat(),
            self._street(),
            self._zip(),
            self._city(),
            self._subdivision(),
        ]

    def _line(self):
        return DynamicField("liniaMobil", self.service_data.phone_number)

    def _icc_sc(self):
        return DynamicField("ICCSC", self.service_data.sc_icc)

    def _icc_donor(self):
        return DynamicField("ICCdonant", self.service_data.icc)

    def _service_type(self):
        if self.service_data.portability:
            return DynamicField("tipusServeiMobil", "portabilitat")
        else:
            return DynamicField("tipusServeiMobil", "altaNova")

    def _previous_provider(self):
        return DynamicField(
            name="operadorDonantMobil",
            value=self.service_data.previous_provider
        )

    def _previous_owner_vat(self):
        return DynamicField(
            name="dniTitularAnterior",
            value=self.service_data.previous_owner_vat
        )

    def _street(self):
        return DynamicField("nomVia", self.customer_data.street)

    def _city(self):
        return DynamicField("localitat", self.customer_data.city)

    def _zip(self):
        return DynamicField("codiPostal", self.customer_data.zip)

    def _subdivision(self):
        return DynamicField("provinciaMobil", self.customer_data.subdivision)

    def _product(self):
        return DynamicField(
            name="productMobil",
            value=self.service_data.product
        )
