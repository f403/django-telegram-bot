# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

@python_2_unicode_compatible
class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(_('First name'), max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255, blank=True, null=True)
    username = models.CharField(_('User name'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return "%s" % self.first_name

@python_2_unicode_compatible
class Chat(models.Model):

    PRIVATE, GROUP, SUPERGROUP, CHANNEL = 'private', 'group', 'supergroup', 'channel'

    TYPE_CHOICES = (
        (PRIVATE, _('Private')),
        (GROUP, _('Group')),
        (SUPERGROUP, _('Supergroup')),
        (CHANNEL, _('Channel')),
    )

    id = models.BigIntegerField(primary_key=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')

    def __str__(self):
        return "%s" % (self.title or self.username)
    
    def is_authenticated(self):
        return hasattr(self, 'auth_token') and not self.auth_token.expired()

@python_2_unicode_compatible
class Audio(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True, verbose_name=_("file_id"))
    duration = models.IntegerField(default=0, verbose_name=_("Duration"))
    # Optionals
    performer = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Performer"))
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Title"))
    mime_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("MIME type"))
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("File size"))
    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audios'
    def __str__(self):
        return "%s - %s (%d %s)" % (self.performer or 'Unknown artist', self.title or 'Unknown title', self.duration, _('sec.'))

@python_2_unicode_compatible
class PhotoSize(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True, verbose_name=_("file_id"))
    width = models.IntegerField(default=0, verbose_name=_("Width"))
    height = models.IntegerField(default=0, verbose_name=_("Height"))
    # Optionals
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("File size"))
    class Meta:
        verbose_name = 'PhotoSize object'
        verbose_name_plural = 'PhotoSize objects'
    def __str__(self):
        return "%s (%d x %d)" % (self.file_id, self.width, self.height)


@python_2_unicode_compatible
class Document(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True, verbose_name=_("file_id"))
    # Optionals
    thumb = models.ForeignKey(PhotoSize, null=True, blank=True, verbose_name=_("Thumbnail"))
    file_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("File name"))
    mime_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("MIME type"))
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("File size"))
    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
    def __str__(self):
        return "%s (%d %s)" % (self.file_name or self.file_id, self.file_size, _('bytes'))

@python_2_unicode_compatible
class Sticker(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True, verbose_name=_("file_id"))
    width = models.IntegerField(default=0, verbose_name=_("Width"))
    height = models.IntegerField(default=0, verbose_name=_("Height"))
    # Optionals
    thumb = models.ForeignKey(PhotoSize, null=True, blank=True, verbose_name=_("Thumbnail"))
    emoji = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Emoji"))
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("File size"))
    class Meta:
        verbose_name = 'Sticker'
        verbose_name_plural = 'Stickers'
    def __str__(self):
        return "%s %s (%d x %d)" % (self.emoji or '', self.file_id, self.width, self.height)

@python_2_unicode_compatible
class Video(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True, verbose_name=_("file_id"))
    width = models.IntegerField(default=0, verbose_name=_("Width"))
    height = models.IntegerField(default=0, verbose_name=_("Height"))
    duration = models.IntegerField(default=0, verbose_name=_("Duration"))
    # Optionals
    thumb = models.ForeignKey(PhotoSize, null=True, blank=True, verbose_name=_("Thumbnail"))
    mime_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("MIME type"))
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("File size"))
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
    def __str__(self):
        return "%s (%d x %d, %d %s)" % (self.file_id, self.width, self.height, self.duration, _('sec.'))

@python_2_unicode_compatible
class Voice(models.Model):
    file_id = models.CharField(max_length=255, primary_key=True, verbose_name=_("file_id"))
    duration = models.IntegerField(default=0, verbose_name=_("Duration"))
    # Optionals
    mime_type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("MIME type"))
    file_size = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("File size"))
    class Meta:
        verbose_name = 'Voice'
        verbose_name_plural = 'Voices'
    def __str__(self):
        return "%s (%d %s)" % (self.file_id, self.duration, _('sec.'))

@python_2_unicode_compatible
class Contact(models.Model):
    phone_number = models.CharField(max_length=50, verbose_name=_("Phone number"))
    first_name = models.CharField(max_length=255, verbose_name=_("First name"))
    # Optionals
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, verbose_name=_("User"))
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name,) if self.last_name else "%s" % self.first_name

@python_2_unicode_compatible
class Location(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    def __str__(self):
        return "%f, %f" % (self.longitude, self.latitude,)

@python_2_unicode_compatible
class Venue(models.Model):
    location = models.ForeignKey(Location)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    # Optionals
    foursquare_id = models.CharField(max_length=255, verbose_name=_("Foursquare identifier"))
    class Meta:
        verbose_name = 'Venue'
        verbose_name_plural = 'Venues'
    def __str__(self):
        return "%s" % self.title

@python_2_unicode_compatible
class Message(models.Model):

    message_id = models.BigIntegerField(_('Id'), primary_key=True)
    from_user = models.ForeignKey(User, related_name='messages', verbose_name=_("User"))
    date = models.DateTimeField(_('Date'))
    chat = models.ForeignKey(Chat, related_name='messages', verbose_name=_("Chat"))
    forward_from = models.ForeignKey(User, null=True, blank=True, related_name='forwarded_from',
                                     verbose_name=_("Forward from"))
    text = models.TextField(null=True, blank=True, verbose_name=_("Text"))
    audio = models.ForeignKey(Audio, null=True, blank=True, verbose_name=_("Audio"))
    document = models.ForeignKey(Document, null=True, blank=True, verbose_name=_("Document"))
    photo = models.ManyToManyField(PhotoSize, blank=True, verbose_name=_("Photo"))
    sticker = models.ForeignKey(Sticker, null=True, blank=True, verbose_name=_("Sticker"))
    vidoe = models.ForeignKey(Video, null=True, blank=True, verbose_name=_("Video"))
    voice = models.ForeignKey(Voice, null=True, blank=True, verbose_name=_("Voice"))
    caption = models.TextField(null=True, blank=True, verbose_name=_("Caption"))
    contact = models.ForeignKey(Contact, null=True, blank=True, verbose_name=_("Contact"))
    location = models.ForeignKey(Location, null=True, blank=True, verbose_name=_("Location"))
    venue = models.ForeignKey(Venue, null=True, blank=True, verbose_name=_("Venue"))
    #  TODO: complete fields with all message fields

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-date', ]

    def __str__(self):
        return "(%s,%s)" % (self.from_user, self.text or '(no text)')


class Update(models.Model):
    
    update_id = models.BigIntegerField(_('Id'), primary_key=True)
    message = models.ForeignKey(Message, null=True, blank=True, verbose_name=_('Message'), 
                                related_name="updates")
    
    class Meta:
        verbose_name = 'Update'
        verbose_name_plural = 'Updates'
    
    def __str__(self):
        return "%s" % self.update_id    
