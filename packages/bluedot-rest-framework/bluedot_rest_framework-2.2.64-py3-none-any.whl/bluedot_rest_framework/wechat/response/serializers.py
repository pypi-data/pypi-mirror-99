from rest_framework.serializers import CharField
from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import WeChatResponseMaterial, WeChatResponseEvent, WeChatQrcode


class WeChatResponseMaterialSerializer(CustomSerializer):

    class Meta:
        model = WeChatResponseMaterial
        fields = '__all__'


class WeChatResponseEventSerializer(CustomSerializer):

    event_key = CharField(required=False)

    class Meta:
        model = WeChatResponseEvent
        fields = '__all__'


class WeChatQrcodeSerializer(CustomSerializer):

    class Meta:
        model = WeChatQrcode
        fields = '__all__'
