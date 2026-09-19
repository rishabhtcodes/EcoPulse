from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    state = models.CharField(max_length=100)
    population = models.BigIntegerField(help_text='Total city population')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(blank=True, default='')
    is_metro = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.state}'

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def latest_air_quality(self):
        return self.air_quality_records.order_by('-recorded_date').first()

    @property
    def latest_weather(self):
        return self.weather_records.order_by('-recorded_date').first()

    @property
    def latest_analysis(self):
        return self.analyses.order_by('-created_at').first()
