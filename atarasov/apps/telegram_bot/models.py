from django.db import models
from django.utils import timezone


# ---------------------------------------------
# Телеграмм пользователь                      -
# ---------------------------------------------
# class TelegramUser(models.Model):
#     class Meta:
#         db_table = 'bot1_telegram_user'
#     id = models.IntegerField(primary_key=True, verbose_name='telegram user id', default=0)
#     date_of_create = models.DateTimeField(verbose_name='date of create', default=timezone.now)
#     favorite_color = models.CharField(verbose_name='word', max_length=35, blank=True, default='')
#     age = models.IntegerField(verbose_name='telegram user id', default=0)
#     # sex = models.NullBooleanField(default=None)
#     is_admin = models.BooleanField(default=False)
#     # ban = models.BooleanField(default=False)


# ---------------------------------------------
# Подписки                                    -
# ---------------------------------------------
# class Subscribes(models.Model):
#     class Meta:
#         db_table = 'bot1_telegram_subscribes'
#     name = models.CharField(verbose_name='')


# ---------------------------------------------
# Связь пользователей с подписками            -
# ---------------------------------------------
# class UserSubscribes(models.Model):
#     class Meta:
#         db_table = 'bot1_telegram_user_subscribes'
#     user = models.ForeignKey(TelegramUser)
#     subscribe = models.ForeignKey(Subscribes)
#     date_of_create = models.DateTimeField(verbose_name='date of create', default=timezone.now)
#     date_of_end = models.DateTimeField(verbose_name='date of end', default=None)


# class UserWords(models.Model):
#     word = models.CharField(verbose_name='word', max_length=35, blank=False, default='')
#     frequency = models.IntegerField(verbose_name='frequency of words', default=0)
#     user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)






