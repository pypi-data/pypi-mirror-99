import uuid

from crum import get_current_user
from django.conf import settings
from django.db.models import Model, UUIDField, DateTimeField, ForeignKey, CASCADE, CharField, BooleanField
from django.utils.translation import ugettext_lazy as _

class Audit(Model):
    
    '''Audit Model
    AuditModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created_at (DateTime): Stores the datetime the object was created.
        + modified_at (DateTime): Stores the last datetime the object was modified.
        + created_by (ForeignKey): Stores the user who created the object.
        + modified_by (ForeignKey): Stores the user who modified the object.
    '''
    id: UUIDField = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(
        auto_now_add=True,
        verbose_name=_('creation date'),
        help_text=_('date when the object was created'),
        db_index=True
    )
    modified_at = DateTimeField(
        auto_now=True,
        verbose_name=_('update date'),
        help_text=_('date when the object was modified'),
    )
    created_by = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE,
        related_name='%(class)s_created_by',
        null=True, blank=True,
        verbose_name=_('creation user'),
        help_text=_('user who created the object'),
    )
    modified_by = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE,
        related_name='%(class)s_modified_by',
        null=True, blank=True,
        verbose_name=_('update user'),
        help_text=_('user who performed the update'),
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            if self.created_at is None and not user.is_anonymous:
                self.created_by = user
                self.modified_by = user
            elif not user.is_anonymous:
                self.modified_by = user
        super(Audit, self).save(*args, **kwargs)

class City(Audit):
    STATES = (
        ('', '---------'),
        ('Amazonas', 'Amazonas'),
        ('Antioquia', 'Antioquia'),
        ('Arauca', 'Arauca'),
        ('Atlántico', 'Atlántico'),
        ('Bolívar', 'Bolívar'),
        ('Boyacá', 'Boyacá'),
        ('Caldas', 'Caldas'),
        ('Caquetá', 'Caquetá'),
        ('Casanare', 'Casanare'),
        ('Cauca', 'Cauca'),
        ('Cesar', 'Cesar'),
        ('Chocó', 'Chocó'),
        ('Córdoba', 'Córdoba'),
        ('Cundinamarca', 'Cundinamarca'),
        ('Guainía', 'Guainía'),
        ('Guaviare', 'Guaviare'),
        ('Huila', 'Huila'),
        ('La Guajira', 'La Guajira'),
        ('Magdalena', 'Magdalena'),
        ('Meta', 'Meta'),
        ('Nariño', 'Nariño'),
        ('Norte de Santander', 'Norte de Santander'),
        ('Putumayo', 'Putumayo'),
        ('Quindío', 'Quindío'),
        ('Risaralda', 'Risaralda'),
        ('San Andrés y Providencia', 'San Andrés y Providencia'),
        ('Santander', 'Santander'),
        ('Sucre', 'Sucre'),
        ('Tolima', 'Tolima'),
        ('Valle del Cauca', 'Valle del Cauca'),
        ('Vaupés', 'Vaupés'),
        ('Vichada', 'Vichada'),
        ('Bogotá d C.', 'Bogotá d C.'),
    )
    name: str = CharField(verbose_name=_('name'), max_length=100)
    state: str = CharField(verbose_name=_('departament'), max_length=100, choices=STATES)
    active: bool = BooleanField(verbose_name=_('active'),default=True)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __str__(self):
        return f'{self.name} - {self.state}'


class PaymentRecord(Audit):
    x_cust_id_cliente = CharField(max_length=250, blank=True, null=True)
    x_description = CharField(max_length=250, blank=True, null=True)
    x_amount_ok = CharField(max_length=250, blank=True, null=True)
    x_id_invoice = CharField(max_length=250, blank=True, null=True)
    x_amount_base = CharField(max_length=250, blank=True, null=True)
    x_tax = CharField(max_length=250, blank=True, null=True)
    x_currency_code = CharField(max_length=250, blank=True, null=True)
    x_franchise = CharField(max_length=250, blank=True, null=True)
    x_transaction_date = CharField(max_length=250, blank=True,
                                          null=True)
    x_approval_code = CharField(max_length=250, blank=True, null=True)
    x_transaction_id = CharField(max_length=250, blank=True, null=True)
    x_ref_payco = CharField(max_length=250, blank=True, null=True)
    x_cod_response = CharField(max_length=250, blank=True, null=True)
    x_cod_transaction_state = CharField(max_length=250, blank=True,
                                               null=True)
    x_transaction_state = CharField(max_length=250, blank=True,
                                           null=True)
    x_signature = CharField(max_length=250, blank=True, null=True)
    x_response = CharField(max_length=250, blank=True, null=True)
    x_response_reason_text = CharField(max_length=250, blank=True,
                                              null=True)
    x_extra1 = CharField(max_length=250, blank=True, null=True)
    x_extra2 = CharField(max_length=250, blank=True, null=True)
    x_extra3 = CharField(max_length=250, blank=True, null=True)
    x_amount = CharField(max_length=250, blank=True, null=True)
    x_amount_country = CharField(max_length=250, blank=True, null=True)
    x_bank_name = CharField(max_length=250, blank=True, null=True)
    x_cardnumber = CharField(max_length=250, blank=True, null=True)
    x_quotas = CharField(max_length=250, blank=True, null=True)
    x_fecha_transaccion = CharField(max_length=250, blank=True,
                                           null=True)
    x_errorcode = CharField(max_length=250, blank=True, null=True)
    x_customer_doctype = CharField(max_length=250, blank=True,
                                          null=True)
    x_customer_lastname = CharField(max_length=250, blank=True,
                                           null=True)
    x_customer_name = CharField(max_length=250, blank=True, null=True)
    x_customer_email = CharField(max_length=250, blank=True, null=True)
    x_customer_phone = CharField(max_length=250, blank=True, null=True)
    x_customer_country = CharField(max_length=250, blank=True,
                                          null=True)
    x_customer_city = CharField(max_length=250, blank=True, null=True)
    x_customer_address = CharField(max_length=250, blank=True,
                                          null=True)
    x_customer_ip = CharField(max_length=250, blank=True, null=True)
    x_test_request = CharField(max_length=250, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s'%self.id