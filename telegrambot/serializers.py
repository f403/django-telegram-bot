from rest_framework import serializers
from telegrambot.models import *
from datetime import datetime
import time
import logging

class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')
        
class ChatSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ('id', 'type', 'title', 'username', 'first_name', 'last_name')
        
class TimestampField(serializers.Field):

    def to_internal_value(self, data):
        return datetime.fromtimestamp(data)
    
    def to_representation(self, value):
        return int(time.mktime(value.timetuple()))


class PhotoSizeSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(required=False)
    class Meta:
        model = PhotoSize
        fields = '__all__'

class AudioSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(required=False)
    performer = serializers.CharField(max_length=255, required=False)
    title = serializers.CharField(max_length=255, required=False)
    mime_type = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Audio
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(required=False)
    thumb = PhotoSizeSerializer(many=False,required=False)
    file_name = serializers.CharField(max_length=255, required=False)
    mime_type = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Document
        fields = '__all__'

class StickerSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(required=False)
    thumb = PhotoSizeSerializer(many=False,required=False)
    emoji = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Sticker
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(required=False)
    thumb = PhotoSizeSerializer(many=False,required=False)
    mime_type = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Video
        fields = '__all__'

class VoiceSerializer(serializers.ModelSerializer):
    file_id = serializers.CharField(max_length=255)
    file_size = serializers.IntegerField(required=False)
    mime_type = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Voice
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(max_length=255, required=False)
    user_id = serializers.IntegerField(required=False)
    class Meta:
        model = Contact
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)
    foursquare_id = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Venue
        fields = '__all__'

        
class MessageSerializer(serializers.HyperlinkedModelSerializer):
    message_id = serializers.IntegerField()
    # reserved word field 'from' changed dynamically
    from_ = UserSerializer(many=False, source="from_user")
    chat = ChatSerializer(many=False)
    date = TimestampField()
    forward_from = UserSerializer(many=False,required=False)
    photo = PhotoSizeSerializer(many=True,required=False)
    audio = AudioSerializer(many=False,required=False)
    document = DocumentSerializer(many=False,required=False)
    sticker = StickerSerializer(many=False,required=False)
    video = VideoSerializer(many=False,required=False)
    voice = VoiceSerializer(many=False,required=False)
    contact = ContactSerializer(many=False,required=False)
    location = LocationSerializer(many=False,required=False)
    venue = VenueSerializer(many=False,required=False)
    
    def __init__(self, *args, **kwargs):
        super(MessageSerializer, self).__init__(*args, **kwargs)
        self.fields['from'] = self.fields['from_']
        del self.fields['from_']

    class Meta:
        model = Message
        fields = ('message_id', 'from_', 'date', 'chat', 'text', 'forward_from', 'audio', 'document', 'photo', 'sticker', 'video', 'voice', 'caption', 'contact', 'location', 'venue', )
        
class UpdateSerializer(serializers.HyperlinkedModelSerializer):
    update_id = serializers.IntegerField()
    message = MessageSerializer(many=False)
    
    class Meta:
        model = Update
        fields = ('update_id', 'message')
        
    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data['message']['from_user'])
        
        chat, created = Chat.objects.get_or_create(**validated_data['message']['chat'])

        forward_from, _ = User.objects.get_or_create(**validated_data['message']['forward_from']) if 'forward_from' in validated_data['message'].keys() else (None,False)

        logger = logging.getLogger(__name__)
        logger.debug(validated_data['message'].keys())
        logger.debug(validated_data['message'])
        # Associate chat to token if comes /start with token
        try:
                splitted_message = validated_data['message']['text'].split(' ')
        except KeyError:
                validated_data['message']['text'] = ''
                splitted_message = []
        if len(splitted_message) > 1 and splitted_message[0] == '/start':
            try:
                token = AuthToken.objects.get(key=splitted_message[1])
                token.chat_api = chat
                token.save()
            except AuthToken.DoesNotExist:
                #  Do not associate with any token
                pass                
        
        message, message_created = Message.objects.get_or_create(message_id=validated_data['message']['message_id'],
                                                   from_user=user,
                                                   date=validated_data['message']['date'],
                                                   chat=chat,
                                                   text=validated_data['message']['text'],
                                                   forward_from=forward_from,
                                                   caption = validated_data['message'].get('caption',''),)
        if message_created:
            if 'audio' in validated_data['message'].keys():
                a,_ = Audio.objects.get_or_create(file_id = validated_data['message']['audio']['file_id'],
                                                duration = validated_data['message']['audio']['duration'],
                                                performer = validated_data['message']['audio'].get('performer',''),
                                                title = validated_data['message']['audio'].get('title',''),
                                                mime_type = validated_data['message']['audio'].get('mime_type',''),
                                                file_size = validated_data['message']['audio'].get('file_size',0),)
                message.audio = a
            if 'document' in validated_data['message'].keys():
                d_thumb=None
                if 'thumb' in validated_data['message']['document'].keys():
                    d_thumb,_ = PhotoSize.objects.get_or_create(file_id=validated_data['message']['document']['thumb']['file_id'],
                                                                width=validated_data['message']['document']['thumb']['width'],
                                                                height=validated_data['message']['document']['thumb']['height'],
                                                                file_size=validated_data['message']['document']['thumb'].get('file_size', 0))
                d,_ = Document.objects.get_or_create(file_id = validated_data['message']['document']['file_id'],
                                                    thumb=d_thumb,
                                                    file_name = validated_data['message']['document'].get('file_name',''),
                                                    mime_type = validated_data['message']['document'].get('mime_type',''),
                                                    file_size = validated_data['message']['document'].get('file_size',0),)
                message.document = d
            if 'sticker' in validated_data['message'].keys():
                s_thumb=None
                if 'thumb' in validated_data['message']['sticker'].keys():
                    s_thumb,_ = PhotoSize.objects.get_or_create(file_id=validated_data['message']['sticker']['thumb']['file_id'],
                                                                width=validated_data['message']['sticker']['thumb']['width'],
                                                                height=validated_data['message']['sticker']['thumb']['height'],
                                                                file_size=validated_data['message']['sticker']['thumb'].get('file_size', 0))
                s,_ = Sticker.objects.get_or_create(file_id = validated_data['message']['sticker']['file_id'],
                                                    width = validated_data['message']['sticker']['width'],
                                                    height = validated_data['message']['sticker']['height'],
                                                    thumb=s_thumb,
                                                    file_size = validated_data['message']['sticker'].get('file_size',0),)
                message.sticker=s
            if 'video' in validated_data['message'].keys():
                v_thumb=None
                if 'thumb' in validated_data['message']['video'].keys():
                    v_thumb,_ = PhotoSize.objects.get_or_create(file_id=validated_data['message']['video']['thumb']['file_id'],
                                                                width=validated_data['message']['video']['thumb']['width'],
                                                                height=validated_data['message']['video']['thumb']['height'],
                                                                file_size=validated_data['message']['video']['thumb'].get('file_size', 0))
                v,_ = Video.objects.get_or_create(file_id = validated_data['message']['video']['file_id'],
                                                    width = validated_data['message']['video']['width'],
                                                    height = validated_data['message']['video']['height'],
                                                    duration = validated_data['message']['video']['duration'],
                                                    thumb=v_thumb,
                                                    mime_type = validated_data['message']['video'].get('mime_type',''),
                                                    file_size = validated_data['message']['video'].get('file_size',0),)
                message.video=v
            if 'voice' in validated_data['message'].keys():
                vc,_ = Voice.objects.get_or_create(file_id = validated_data['message']['voice']['file_id'],
                                                duration = validated_data['message']['voice']['duration'],
                                                mime_type = validated_data['message']['voice'].get('mime_type',''),
                                                file_size = validated_data['message']['voice'].get('file_size',0),)
                message.voice = vc
            if 'contact' in validated_data['message'].keys():
                c,_ = Contact.objects.get_or_create(phone_number = validated_data['message']['contact']['phone_number'],
                                                    first_name = validated_data['message']['contact']['first_name'],
                                                    last_name = validated_data['message']['contact'].get('last_name',''),
                                                    user_id = validated_data['message']['contact'].get('user_id',0),)
                message.contact = c
            if 'location' in validated_data['message'].keys():
                loc,_ = Location.objects.get_or_create(longitude = validated_data['message']['location']['longitude'],
                                                    latitude = validated_data['message']['location']['latitude'],)
                message.location = loc
            if 'venue' in validated_data['message'].keys():
                vloc,_ = Location.objects.get_or_create(longitude = validated_data['message']['venue']['location']['longitude'],
                                                    latitude = validated_data['message']['venue']['location']['latitude'],)
                ve,_ = Venue.objects.get_or_create(location = vloc,
                                                    title = validated_data['message']['venue']['title'],
                                                    address = validated_data['message']['venue']['address'],
                                                    foursquare_id = validated_data['message']['venue'].get('foursquare_id',0),)
                message.venue = ve

            if 'photo' in validated_data['message'].keys():
                for ph in validated_data['message']['photo']:
                    photosize, _ = PhotoSize.objects.get_or_create(file_id=ph['file_id'],
                                                                    width=ph['width'],
                                                                    height=ph['height'],
                                                                    file_size=ph.get('file_size', 0))
                    message.photo.add(photosize)
                    logger.debug(ph)

            message.save()

        update, _ = Update.objects.get_or_create(update_id=validated_data['update_id'],
                                                 message=message)

        return update