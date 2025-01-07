from django.core.exceptions import ValidationError
from django.db import models

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, # ссылка на модель явным импортом модели.
                                  on_delete=models.CASCADE,
                                  related_name='from_city_set',
                                  verbose_name='Из какого города'
                                  )
    to_city = models.ForeignKey('cities.City', # ссылка на модель точечной нотацией на приложение, где находится модель.
                                on_delete=models.CASCADE,
                                related_name='to_city_set',
                                verbose_name='В какой город'
                                )

    def __str__(self):
        return f'Поезд № {self.name} из города {self.from_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['travel_time']

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Изменить город прибытия или отправления')
        qs = Train.objects.filter(
            from_city=self.from_city,
            to_city=self.to_city,
            travel_time=self.travel_time
        ).exclude(pk=self.pk)
        # Train == self.__class__
        if qs.exists():
            raise ValidationError('Необходимо изменить время в пути')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)