from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    ads = models.ManyToManyField('Ad', related_name='users', blank=True)
    exhanges = models.ManyToManyField('ExchangeProposal', related_name='users', blank=True)
 

class Ad(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    AD_CATEGORIES = [
        ('home_goods', 'Товары для дома'),
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'),
        ('sport', 'Спорт и отдых'),
        ('other', 'Другое'),
    ]

    AD_CONDITIONS = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=AD_CATEGORIES)  
    condition = models.CharField(max_length=10, choices=AD_CONDITIONS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принята'),
        ('rejected', 'Отклонена'),
        ('canceled', 'Отменена'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_proposals')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_proposals')
    
    sender_ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_offers')
    receiver_ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_offers')
    comment = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.sender_ad.user != self.sender:
            raise ValidationError("Вы не владелец объявления-отправителя")
        if self.receiver_ad.user != self.receiver:
            raise ValidationError("Получатель не владелец объявления-получателя")
        if self.sender_ad == self.receiver_ad:
            raise ValidationError("Нельзя обменивать товар сам на себя")