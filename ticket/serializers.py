import datetime
from rest_framework import serializers
from ticket.models import Ticket, TicketDetail
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'full_name', 
            'base_role'
            )


class UserCreateTicketSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)
    attachment = serializers.FileField(
        required=False, 
        write_only=True
        )
    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'type',
            'priority',
            'message',
            'attachment',
            'user_ids'
        ]

    def create(self, validated_data):
        request = self.context['request']
        current_user = request.user
        message = validated_data.pop('message')
        attachment = validated_data.pop('attachment', None)
        staff_list = validated_data.pop('user_ids', [])
        users = {
            s.core_user
            for s in staff_list
            if s.core_user
        }
        users.add(current_user)
        ticket = Ticket.objects.create(
            status='open',
            **validated_data
        )
        ticket.user.set(users)
        TicketDetail.objects.create(
            ticket=ticket,
            message=message,
            attachment=attachment
        )
        return ticket


class UserTicketListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source='get_status_display', 
        read_only=True
        )
    type_display = serializers.CharField(
        source='get_type_display',
        read_only=True
        )
    relative_time = serializers.SerializerMethodField(read_only=True)
    user = UserMiniSerializer(
        many=True, 
        read_only=True
        )
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'number',
            'title',
            'status',
            'status_display',
            'type',
            'type_display',
            'relative_time',
            'user',
            'priority',
            'created_by',
            'created_at',
        ]

    def get_relative_time(self, obj):
        created_at = getattr(obj, '_created_at', obj.created_at)
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, "%Y.%m.%d %H:%M")
        now = timezone.now()
        diff = now - created_at
        minutes = diff.total_seconds() / 60
        if minutes < 1:
            return "چند لحظه قبل"
        elif minutes < 60:
            return f"{int(minutes)} دقیقه قبل"
        elif minutes < 1440:
            return f"{int(minutes // 60)} ساعت قبل"
        else:
            return f"{int(minutes // 1440)} روز قبل"
        

class TicketDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = TicketDetail
        fields = [
            'id',
            'user',
            'message',
            'attachment',
            'created_at',
            'created_by'
        ]

    def get_user(self, obj):
        if obj.ticket.user.exists():
            creator = obj.ticket.user.first()  
            return {
                'id': creator.id,
                'full_name': getattr(creator, 'full_name', f"{creator.first_name} {creator.last_name}"),
                'role': getattr(creator, 'role', '')
            }
        return None


class UserReplyTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDetail
        fields = ['message', 'attachment']

    def create(self, validated_data):
        request = self.context['request']
        ticket = self.context['ticket']
        if not ticket.can_reply:
            raise serializers.ValidationError('امکان پاسخ به این تیکت وجود ندارد')
        return TicketDetail.objects.create(
            ticket=ticket,
            **validated_data
        )
