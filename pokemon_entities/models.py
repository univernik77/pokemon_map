from django.db import models


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение',
                              upload_to='media',
                              blank=True)
    title_en = models.CharField('Название на английском',
                                max_length=200,
                                blank=True)
    title_jp = models.CharField('Название на японском',
                                max_length=200,
                                blank=True)
    description = models.TextField('Описание',
                                   max_length=1000,
                                   blank=True)
    previous_evolutions = models.ForeignKey("self",
                                            verbose_name='Из кого эволюционирует',
                                            related_name='next_evolutions',
                                            on_delete=models.SET_NULL,
                                            null=True,
                                            blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                related_name='entities',
                                verbose_name='Покемон',
                                on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    long = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления',
                                       null=True)
    disappeared_at = models.DateTimeField('Время исчезновения',
                                          null=True)
    level = models.IntegerField('Уровень',
                                null=True,
                                blank=True)
    health = models.IntegerField('Здоровье',
                                 null=True,
                                 blank=True)
    strength = models.IntegerField('Сила',
                                   null=True,
                                   blank=True)
    defence = models.IntegerField('Защита',
                                  null=True,
                                  blank=True)
    stamina = models.IntegerField('Выносливость',
                                  null=True,
                                  blank=True)

    def __str__(self):
        return self.pokemon.title