from django.db import models
from django.utils.translation import ugettext_lazy as _

AMOUNT_CHOICES = (
    (5, '$5'),
    (10, '$10'),
    (25, '$25'),
    (50, '1 Hour ($50)'),
    (100, '2 Hours ($100)'),
    (200, '4 Hours ($200)'),
    (400, '1 Day ($400)'),
    (800, '2 Days ($800)'),
    (1200, '3 Days ($1200)'),
    (1600, '4 Days ($1600)'),
    (2000, '5 Days ($2000)'),
    (4000, '2 Weeks ($4000)'),
    (6000, '3 Weeks ($6000)'),
    (8000, '4 Weeks ($8000)'),
)

DISPLAY_CHOICES = (
    ('doc', 'Documentation Pages'),
    ('site-footer', 'Site Footer'),
    ('search', 'Search Pages'),
)


class Supporter(models.Model):
    pub_date = models.DateTimeField(_('Publication date'), auto_now_add=True)
    modified_date = models.DateTimeField(_('Modified date'), auto_now=True)
    public = models.BooleanField(_('Public'), default=True)

    name = models.CharField(_('name'), max_length=200, blank=True)
    email = models.EmailField(_('Email'), max_length=200, blank=True)
    user = models.ForeignKey('auth.User', verbose_name=_('User'),
                             related_name='goldonce', blank=True, null=True)
    dollars = models.IntegerField(_('Amount'), max_length=30,
                                  choices=AMOUNT_CHOICES, default=50)
    logo_url = models.URLField(_('Logo URL'), max_length=255, blank=True,
                               null=True)
    site_url = models.URLField(_('Site URL'), max_length=255, blank=True,
                               null=True)

    last_4_digits = models.CharField(max_length=4)
    stripe_id = models.CharField(max_length=255)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SupporterPromo(models.Model):
    pub_date = models.DateTimeField(_('Publication date'), auto_now_add=True)
    modified_date = models.DateTimeField(_('Modified date'), auto_now=True)

    name = models.CharField(_('Name'), max_length=200)
    analytics_id = models.CharField(_('Analytics ID'), max_length=200)
    text = models.TextField(_('Text'), blank=True)
    link = models.URLField(_('Link URL'), max_length=255, blank=True, null=True)
    image = models.URLField(_('Image URL'), max_length=255, blank=True, null=True)
    display_type = models.CharField(_('Display Type'), max_length=200,
                                    choices=DISPLAY_CHOICES, default='doc')

    live = models.BooleanField(_('Live'), default=False)

    def __str__(self):
        return self.name

    def as_dict(self):
        "A dict respresentation of this for JSON encoding"
        return {
            'id': self.analytics_id,
            'text': self.text,
            'link': self.link,
            'image': self.image,
        }
