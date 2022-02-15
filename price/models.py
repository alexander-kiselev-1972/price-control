from django.db import models


# Create your models here.
# создать сязанные таблицы
# Табл1 Lek - в ней общая информация о лекарстве ( Название, форма, дозировка, barcode и производитель)


class MNN(models.Model):
    """Список Международных не патентованных названий """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Lek(models.Model):
    """Запись общего вида о препарате"""
    name = models.CharField(max_length=80)
    lek_form = models.CharField(max_length=300, default='tabl')
    barcode = models.CharField(max_length=13, default='1234567898765')
    name_factory = models.CharField(max_length=255, default='uu')
    mnn = models.ForeignKey(MNN, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class HistoryPrice(models.Model):
    """Здесь записываем когда у лекарства появилась зарегистрированная цена,
    а когда действие правила завершилось"""

    lek = models.ForeignKey(Lek, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    date_in = models.DateTimeField(null=True, blank=True)
    date_out = models.DateTimeField(null=True, blank=True)
    solution = models.CharField(max_length=30)

    def __str__(self):
        return str(self.price)


# Регионы
class Regions(models.Model):
    region_name = models.CharField(max_length=50)

    def __str__(self):
        return self.region_name


# Здесь хранятся правила расценки
class PricingRules(models.Model):
    region_id = models.ForeignKey(Regions, on_delete=models.CASCADE)
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    procent = models.IntegerField()
    date_in = models.DateField()
    is_active = models.BooleanField(default=True)

    def __int__(self):
        return self.min_price, self.max_price
