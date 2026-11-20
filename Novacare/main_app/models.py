from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()

    # Department services
    service_one = models.CharField(max_length=150)
    service_two = models.CharField(max_length=150)
    service_three = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Doctor(models.Model):
    name = models.CharField(max_length=150)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='doctors'
    )
    role = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience = models.PositiveSmallIntegerField()
    availability = models.CharField(max_length=150, blank=True)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True
    )
    about = models.TextField()
    slug = models.SlugField(max_length=150, unique=True)
    image = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class DepartmentService(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=150)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.department.name} - {self.name}'

    class Meta:
        ordering = ['order', 'name']