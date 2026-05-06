import uuid
from django.contrib.auth import get_user_model
from django.db import models
import jdatetime
from common.models import BaseModel
from ticket.type import (PriorityType, TicketCategory, TicketStatus)
from ticket.services import (ticket_attachment_path, validate_attachment_file, generate_ticket_number)

User = get_user_model()

class Ticket(BaseModel):
    user = models.ForeignKey(User, related_name="ticket_user", verbose_name="user", on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=30, choices=TicketStatus.choices, default=TicketStatus.open)
    number = models.CharField('number', max_length=256, unique=True, default=generate_ticket_number, editable=False)
    description = models.CharField('description', max_length=500, null=True, blank=True, default='')
    title = models.CharField('title', max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    can_reply = models.BooleanField(default=True)
    can_upload_attachment = models.BooleanField(default=True)
    reviewer = models.ForeignKey(User, related_name="reviewed_tickets", on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField("category", choices=TicketCategory.choices, max_length=400, null=True, blank=True)
    priority = models.CharField("priority", choices=PriorityType.choices, max_length=400, null=True, blank=True)
    is_pinned = models.BooleanField(default=False)

    class Meta:
        verbose_name = "01-ticket"
        verbose_name_plural = "01-tickets"
        db_table = 'ticket'
        indexes = [models.Index(fields=('id',))]

    def __str__(self):
        return f"{self.title} ({self.number})"

    @staticmethod
    def generate_ticket_number():
        year = jdatetime.date.today().year
        return f"{year}-{uuid.uuid4().hex[:8]}"


class TicketDetail(BaseModel):
    ticket = models.ForeignKey(Ticket, related_name='ticket', verbose_name='detail_ticket', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, related_name="detail_user", verbose_name="user", on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField('message', max_length=1000, blank=True, null=True)
    attachment = models.FileField(upload_to=ticket_attachment_path, validators=[validate_attachment_file], blank=True, null=True)
    seen_by = models.ManyToManyField(User, related_name="seen_ticket_messages", blank=True)

    class Meta:
        verbose_name = "02-ticket_detail"
        verbose_name_plural = "02-ticket_details"
        db_table = 'ticket_detail'
        indexes = [models.Index(fields=('id',))]

    def __str__(self):
        return f"Message for Ticket {self.ticket.number}" if self.ticket else "TicketDetail"
