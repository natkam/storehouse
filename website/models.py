from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
# from django.utils.translation import gettext_lazy as _

LOAD_TYPES = (
    ('A', 'Apples'),
    ('B', 'Bananas'),
    ('C', 'Carrots'),
    ('D', 'Dates'),
    ('E', 'Eggplants'),
)

MAX_NUMBER_OF_SHELVES_IN_LINE = 10
MAX_TYPES_OF_LOAD_ON_SHELF = 3
MAX_LOADS_ON_SHELF = 10
MAX_LOADS_IN_TRANSPORT = 5
MAX_NUMBER_OF_TRANSPORTS = 5


class Shelf(models.Model):
    """ Has 10 slots for loads, max. 3 types of load on one shelf. """

    number = models.PositiveIntegerField(primary_key=True)
    position = models.PositiveIntegerField(
        unique=True,
        validators=[MaxValueValidator(MAX_NUMBER_OF_SHELVES_IN_LINE-1)],
        # a shelf can be put aside in the storehouse (useful while shifting shelves):
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        ordering = ['position']

    def __str__(self):
        return str(self.position) + ': Shelf no. ' + str(self.number)


class Transport(models.Model):
    """ Takes <=5 loads of one particular type of product. """

    number = models.PositiveIntegerField(
        primary_key=True,
        validators=[MaxValueValidator(MAX_NUMBER_OF_TRANSPORTS-1)],
    )
    load_type = models.CharField(
        max_length=15,
        choices=LOAD_TYPES,
    )

    class Meta:
        ordering = ['number']

    def __str__(self):
        return 'Transport no. ' + str(self.number) + ', ' + self.get_load_type_display()


class Load(models.Model):
    """ A load of specific type, can be on a shelf or in a transport (not both),
    or nowhere in particular. If assigned to either, perform validation: check
    whether the types match, and whether the shelf/transport it full already. """

    shelf = models.ForeignKey(
        Shelf,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    transport = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    load_type = models.CharField(
        max_length=15,
        choices=LOAD_TYPES,
        default='A',
    )

    def __str__(self):
        return 'id ' + str(self.id) + ', ' + self.get_load_type_display()

    def add_to_shelf_validator(self):
        shelf_error_messages = []
        shelf = self.shelf
        all_loads_on_shelf = shelf.load_set.all()
        if all_loads_on_shelf.count() >= MAX_LOADS_ON_SHELF:
            shelf_error_messages.append('This shelf is already full.')
        same_type_loads_on_shelf = all_loads_on_shelf.filter(
            load_type=self.load_type
        )
        unique_types = all_loads_on_shelf.values_list('load_type').distinct().count()
        if unique_types > 2 and not same_type_loads_on_shelf:
            shelf_error_messages.append('There can be max. 3 types of load on one shelf.')
        return shelf_error_messages

    def transfer_validator(self):
        transport_error_messages = []
        transport = self.transport
        if self.load_type != transport.load_type:
            transport_error_messages.append(
                'The type of this load does not match the type of the transport.'
            )
        if transport.load_set.count() >= MAX_LOADS_IN_TRANSPORT:
            transport_error_messages.append('This transport is already full.')
        return transport_error_messages

    def clean(self):
        error_messages = []
        if self.shelf and self.transport:
            raise ValidationError('A load can be either on a shelf or in a transport, not both!')
        if self.shelf:
            error_messages += self.add_to_shelf_validator()
        if self.transport:
            error_messages += self.transfer_validator()
        if error_messages:
            raise ValidationError(' '.join(error_messages))
