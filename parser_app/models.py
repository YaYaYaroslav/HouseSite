from django.db import models


class Listing(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.title


class PropertyInfo(models.Model):
    url = models.URLField(unique=True)
    images = models.TextField(blank=True)
    name = models.CharField(max_length=255, blank=True)
    cost = models.CharField(max_length=255, blank=True)
    details = models.TextField(blank=True)
    wordwrap = models.TextField(blank=True)
    highlights = models.TextField(blank=True)
    address = models.TextField(blank=True)
    location = models.TextField(blank=True)
    about_place = models.TextField(blank=True)
    nearby_places = models.TextField(blank=True)
    seller_info = models.JSONField(default=dict, blank=True)
    whatsapp = models.CharField(max_length=255, blank=True)
    now_on_ad = models.CharField(max_length=255, blank=True)

    def save_images(self, images_list):
        self.images = ','.join(images_list)

    def save_highlights(self, highlights_list):
        self.highlights = ','.join(highlights_list)

    def save_nearby_places(self, places_list):
        self.nearby_places = ','.join(places_list)

    def get_images(self):
        return self.images.split(',') if self.images else []

    def get_highlights(self):
        return self.highlights.split(',') if self.highlights else []

    def get_nearby_places(self):
        return self.nearby_places.split(',') if self.nearby_places else []

    def __str__(self):
        return self.name