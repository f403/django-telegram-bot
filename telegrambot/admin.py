from django.contrib import admin
from telegrambot.models import *

admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(User)
admin.site.register(Update)
admin.site.register(Bot)
admin.site.register(AuthToken)

admin.site.register(Audio)
admin.site.register(PhotoSize)
admin.site.register(Document)
admin.site.register(Sticker)
admin.site.register(Video)
admin.site.register(Voice)
admin.site.register(Contact)
admin.site.register(Location)
admin.site.register(Venue)
