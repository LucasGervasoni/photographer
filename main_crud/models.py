from django.db import models

# Create your models here.

#Orders

class CreateOrders(models.Model):
  # name = models.ForeignKey(User, on_delete=models.PROTECT)
  date = models.DateField()
  time = models.TimeField()
  addressOne = models.CharField(max_length=150, verbose_name="Address 1")
  AddressTwo = models.CharField(max_length=150, verbose_name="Address 2")
  ZipCode = models.CharField(max_length=50, verbose_name="Zip Code")
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  services = models.CharField(max_length=300)

  def __str__(self):
    return "{} -> {} | {} at {}".format(self.addressOne, self.ZipCode, self.date, self.time)

  