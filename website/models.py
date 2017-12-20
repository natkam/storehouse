from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _

LOAD_TYPES = (
    ('A', 'Apples'),
    ('B', 'Bananas'),
    ('C', 'Carrots'),
    ('D', 'Dates'),
    ('E', 'Eggplants'),
)

class Shelf(models.Model):
    """ Has 10 slots for loads, max. 3 types of load on one shelf. """
    number = models.PositiveIntegerField(primary_key=True)
    position = models.PositiveIntegerField(
        unique=True,
        validators=[MaxValueValidator(9)],
    )
    # TODO later: add some validation to ensure that no more than 10 shelves are created?
    # Now, effectively this is ensured by the restrictions on the position field.

    # def clean(self):
    #     error_messages = []
    #     product_units_on_shelf = self.productunit_set.all()
    #     # self.productunit_set.count()
    #
    #     if self.prod1_count + self.prod2_count + self.prod3_count > 10:
    #         error_messages.append('You cannot put more than 10 product units in total on one shelf.')
    #
    #     # possibly redundant since a shelf has an all_products dict? NOT YET
    #     product_types_on_shelf = [self.prod1_type, self.prod2_type, self.prod3_type]
    #     product_counts_on_shelf = [self.prod1_count, self.prod2_count, self.prod3_count]
    #     for product_count, product_type in zip(product_counts_on_shelf, product_types_on_shelf):
    #         if product_count and not product_type:
    #             error_messages.append('You have to choose the type of the product you want to put on the shelf.')
    #
    #     """ Check if there are duplicate product types, except for empty strings when <=one type chosen: """
    #     non_empty_product_types = list(filter(bool, product_types_on_shelf))
    #     if len(set(non_empty_product_types)) != len(non_empty_product_types):
    #         error_messages.append('Product types should differ.')
    #
    #     if len(error_messages):
    #         raise ValidationError(' '.join(error_messages))

    def __str__(self):
        return str(self.position) + ': Shelf no. ' + str(self.number)

    class Meta:
        ordering = ['position']


class Transport(models.Model):
    """ Takes <=5 loads of one particular type of product. """
    number = models.PositiveIntegerField(
        primary_key=True,
        validators=[MaxValueValidator(4)],
    )
    load_type = models.CharField(
        max_length=15,
        choices=LOAD_TYPES,
        default='A',
    )
    max_load_count = 5

    def __str__(self):
        return 'Transport no. ' + str(self.number) + ', ' + self.get_load_type_display()

    class Meta:
        ordering = ['number']


class Load(models.Model):
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

    def add_to_shelf_validator(self):
        shelf_error_messages = []
        shelf = self.shelf
        all_loads_on_shelf = shelf.load_set.all()
        if all_loads_on_shelf.count() > 9:
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
        if transport.load_set.count() >= transport.max_load_count:
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
        if len(error_messages):
            raise ValidationError(' '.join(error_messages))

    def __str__(self):
        return 'id ' + str(self.id) + ', ' + self.get_load_type_display()
