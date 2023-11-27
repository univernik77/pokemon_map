from django.db import models



class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField('Lat', null=True)
    long = models.FloatField('Long', null=True)
    appeared_at = models.DateTimeField('Date', null=True)
    disappeared_at = models.DateTimeField('Time', null=True)
    level = models.IntegerField('Level', null=True)
    health = models.IntegerField('Health', null=True)
    strength = models.IntegerField('Strength', null=True)
    defence = models.IntegerField('Defence', null=True)
    stamina = models.IntegerField('Stamina', null=True)