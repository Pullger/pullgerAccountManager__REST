from rest_framework import serializers


class AccountListSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'uuid': str(instance.uuid),
            'authorization': str(instance.authorization),
            'login': str(instance.login),
            'active': str(instance.active),
            'use': str(instance.use),
        }