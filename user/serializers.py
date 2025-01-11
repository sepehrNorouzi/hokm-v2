from rest_framework import serializers

from user.models import NormalPlayer, GuestPlayer


class NormalPlayerSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = NormalPlayer
        fields = ['email', 'password', 'profile_name', 'gender', 'birth_date', 'first_name', 'last_name', ]

    def create(self, validated_data):
        data = validated_data
        email = data['email']
        password = data['password']
        del data['email']
        del data['password']
        return NormalPlayer.create(email=email, password=password, **data)


class NormalPlayerVerifySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(write_only=True, required=True)
    profile_name = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    credentials = serializers.SerializerMethodField()

    class Meta:
        model = NormalPlayer
        fields = ['email', 'profile_name', 'gender', 'birth_date', 'first_name', 'last_name', 'credentials', 'otp', ]

    def get_credentials(self, obj: NormalPlayer):
        return obj.get_token()


class NormalPlayerSignInSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = NormalPlayer
        fields = ['email', 'profile_name', 'gender', 'birth_date', 'first_name', 'last_name', 'password', ]


class GuestPlayerSignUpSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(required=True)
    credentials = serializers.SerializerMethodField()

    class Meta:
        model = GuestPlayer
        fields = ['device_id', 'recovery_string', 'profile_name', 'gender', 'birth_date', 'first_name', 'last_name',
                  'credentials']

    def create(self, validated_data):
        data = validated_data
        device_id = data['device_id']
        password = data['password']
        del data['password']
        del data['device_id']
        return GuestPlayer.create(device_id=device_id, password=password, **data)

    def get_credentials(self, obj: GuestPlayer):
        return obj.get_token()
