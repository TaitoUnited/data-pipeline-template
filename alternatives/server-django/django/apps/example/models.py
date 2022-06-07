from django.db import models


class Sales(models.Model):
    key = models.TextField(primary_key=True)
    # date_key = models.ForeignKey(Dates)
    # product_key = models.ForeignKey(Products)
    order_number = models.TextField()
    quantity = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True
        db_table = "sales"


class SalesCreate(models.Model):
    # date_key = models.ForeignKey(Dates)
    # product_key = models.ForeignKey(Products)
    order_number = models.TextField()
    quantity = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = "sales"
