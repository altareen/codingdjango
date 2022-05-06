from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Brand(models.Model):
    name = models.CharField(
            max_length=200, 
            help_text='Enter a brand(e.g. Honda)',
            validators=[MinLengthValidator(2, "Brand name must be longer than 1 character")]
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Auto(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Auto name must be longer than 1 character")]
    )
    mileage = models.PositiveIntegerField()
    comments = models.CharField(max_length=300)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=False)

    # Shows up in the admin list
    def __str__(self):
        return self.name
