from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    type = serializers.CharField(required=False, allow_blank=True)
    subject = serializers.CharField(required=True)
    template = serializers.CharField(required=True)
    user_id = serializers.UUIDField(required=True)
    film_id = serializers.UUIDField(required=False, allow_blank=True)

    def create(self, request_data, type):
        self.type = type,
        self.subject = request_data.data['subject'],
        self.template = request_data.data['template'],
        self.user_id = request_data.data['user_id']

        if 'film_id' in request_data.data.keys():
            self.film_id = request_data.data['film_id']

        return self.data
