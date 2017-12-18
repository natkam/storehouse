from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

PRODUCT_TYPES = (
    ('A', 'Apples'),
    ('B', 'Bananas'),
    ('C', 'Carrots'),
    ('D', 'Dates'),
    ('E', 'Eggplants'),
)

class Shelf(models.Model):
    """ Has 10 slots for product units, max. 3 types of product on one shelf. """
    number = models.PositiveIntegerField(primary_key=True)
    position = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(9)])
    prod1_type = models.CharField(max_length=15, choices=PRODUCT_TYPES, default='', blank=True)
    prod1_count = models.PositiveIntegerField(default=0)
    prod2_type = models.CharField(max_length=15, choices=PRODUCT_TYPES, default='', blank=True)
    prod2_count = models.PositiveIntegerField(default=0)
    prod3_type = models.CharField(max_length=15, choices=PRODUCT_TYPES, default='', blank=True)
    prod3_count = models.PositiveIntegerField(default=0)

    # def fill(self):
    #     self.product_count = {self.prod1_type: self.prod1_count, self.prod2_type: self.prod2_count, self.prod3_type: self.prod3_count}
    #     return self.product_count

    def empty(self):
        self.prod1_type = ''
        self.prod2_type = ''
        self.prod3_type = ''
        self.prod1_count = 0
        self.prod2_count = 0
        self.prod3_count = 0

    def clean(self):
        error_messages = []

        if self.prod1_count + self.prod2_count + self.prod3_count > 10:
            error_messages.append('You cannot put more than 10 product units in total on one shelf.')

        prod_types_on_shelf = [self.prod1_type, self.prod2_type, self.prod3_type]
        prod_counts_on_shelf = [self.prod1_count, self.prod2_count, self.prod3_count]
        for prod_count, prod_type in zip(prod_counts_on_shelf, prod_types_on_shelf):
            if prod_count and not prod_type:
                error_messages.append('You have to choose the type of the product you want to put on the shelf.')

        """ Check if there are duplicate product types, except for empty strings (when only one type chosen): """
        non_empty_prod_types = list(filter(bool, prod_types_on_shelf))
        if len(set(non_empty_prod_types)) != len(non_empty_prod_types):
            error_messages.append('Product types should differ.')

        if len(error_messages):
            raise ValidationError(' '.join(error_messages))

    def __str__(self):
        return str(self.position) + ': Shelf no. ' + str(self.number)

    class Meta:
        ordering = ['position']

class Transport(models.Model):
    """ Takes <=5 units of one particular type of product. """
    number = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(4)])
    product_type = models.CharField(max_length=15, choices=PRODUCT_TYPES, default='A')
    load_size = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])

    def fill(self):
        self.load_size = 5

class ProductUnit(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, blank=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, blank=True)
    product_type = models.CharField(max_length=15, choices=PRODUCT_TYPES)
