from django.contrib import auth
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import validate_email, EmailValidator, FileExtensionValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.db.models.manager import EmptyManager
from django.core.validators import RegexValidator

import re

SILENCED_SYSTEM_CHECKS = ["auth.W004"]

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')

        username_validator = ASCIIUsernameValidator()
        username = self.model.normalize_username(username, required=True, validators=[username_validator])
        email = self.normalize_email(email, required=True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    id = models.AutoField(primary_key=True)
    username = models.CharField(_('username'), max_length=150)
    password = models.CharField(_('password'), max_length=150)
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_company = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    image = models.ImageField(_('image'), max_length=150)
    fab_selection_id = models.CharField(_('fab_selection_id'), max_length=45)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'mysite_user'

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Others(models.Model):
    """概要欄"""

    article_id = models.CharField(_('article id'), max_length=45)
    comment = models.CharField(_('comment'), max_length=150)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        verbose_name = _('others')
        verbose_name_plural = _('others')
        db_table = 'others'

    def __str__(self):
        return self.comment

class RoomImage(models.Model):
    """部屋の画像"""

    article_id = models.CharField(_('floor number'), max_length=45)
    image = models.ImageField(_('image'), max_length=150)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        verbose_name = _('images')
        verbose_name_plural = _('images')
        db_table = 'images'


class ArticleLive(models.Model):
    """カスタム物件モデル"""

    id = models.AutoField(_('id'), primary_key=True)
    article_id = models.CharField(_('article id'), max_length=45)
    vacancy_info = models.CharField(_('vacancy live'), max_length=45)
    vacancy_live = models.CharField(_('vacancy live'), max_length=45)
    start_date = models.CharField(_('start date'), max_length=45)
    update_date = models.CharField(_('update date'), max_length=45)
    cancel_date = models.CharField(_('cancel date'), max_length=45)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'))

    class Meta:
        verbose_name = _('article live')
        verbose_name_plural = _('article live')
        db_table = 'article_live'

class Article(models.Model):
    """カスタム物件モデル(View専用)"""

    id = models.AutoField(primary_key=True)
    customer = models.IntegerField(_('customer'))
    article_name = models.CharField(_('article name'), max_length=150)
    comments = models.CharField(_('comments'), max_length=150)
    room_images_id = models.CharField(_('room images id'), max_length=150)
    article_image = models.ImageField(_('article image'), upload_to='media')
    address_number = models.CharField(u'郵便番号', max_length=45)
    address = models.CharField(_('address'), max_length=150)
    rent = models.CharField(_('rent'), max_length=150)
    park = models.CharField(_('park'), max_length=150)
    initial_cost = models.CharField(_('initial cost'), max_length=150)
    floor_plan = models.CharField(_('floor plan'), max_length=150)
    common_service_expense = models.CharField(_('common service expense'), max_length=150)
    term_of_contract = models.CharField(_('term of contract'), max_length=150)
    floor_number = models.CharField(_('floor number'), max_length=150)
    column = models.CharField(_('column'), max_length=150)
    live_flag = models.ForeignKey(ArticleLive, on_delete=models.CASCADE, related_name="article_live")
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    published_at = models.DateTimeField(_('published at'), default=timezone.now)


    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        db_table = 'article'

    def __str__(self):
        return self.article_name

class Fab(models.Model):
    """お気に入り機能"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_key")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_key")
    flag = models.IntegerField()
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'))

    class Meta:
        verbose_name = _('fab')
        verbose_name_plural = _('fab')
        db_table = 'fab'

class ArticleRoom(models.Model):
    """サンプル物件モデル(View用)"""

    id = models.AutoField(primary_key=True)
    room = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="room_key")
    room_live_id = models.CharField(_('room live id'), max_length=150)

    class Meta:

        db_table = 'sample_room'

class ArticleFloor(models.Model):
    """サンプル物件モデル(View用)"""

    id = models.AutoField(primary_key=True)
    floor = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="floor_key")

    class Meta:

        db_table = 'sample_floor'

class ArticleCreate(models.Model):
    """物件登録モデル"""
    id = models.AutoField(primary_key=True)
    customer = models.IntegerField(_('customer'))
    article_name = models.CharField(u'名称', max_length=150)
    comments = models.CharField(u'キャッチコピー', max_length=150)
    room_images_id = models.CharField(u'メイン画像', max_length=150)
    article_image = models.FileField(u'メイン画像')
    address_number = models.CharField(u'郵便番号', max_length=45)
    address = models.CharField(u'住所', max_length=150)
    rent = models.CharField(u'家賃', max_length=150)
    park = models.CharField(u'駐車場', max_length=150)
    initial_cost = models.CharField(u'初期費用', max_length=150)
    floor_plan = models.CharField(u'間取り', max_length=150)
    common_service_expense = models.CharField(u'共益費用', max_length=150)
    term_of_contract = models.CharField(u'契約期間', max_length=150)
    floor_number = models.CharField(u'階数', max_length=150)
    column = models.TextField(u"備考", max_length=150)
    live_flag = models.OneToOneField(ArticleLive, verbose_name="vacancy_live", on_delete=models.CASCADE, related_name="live")
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'))
    published_at = models.DateTimeField(_('published at'), default=timezone.now)

    class Meta:
        verbose_name = _('article_name')
        verbose_name_plural = _('article_name')
        db_table = 'article'

class Company(models.Model):
    """業者モデル"""
    id = models.AutoField(primary_key=True)
    is_company = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    user_id = models.IntegerField(_('user_id'))
    company_name = models.CharField(u'会社名', max_length=150)
    address_number = models.CharField(u'郵便番号', max_length=45)
    address = models.CharField(u'住所', max_length=150)
    update_count = models.CharField(u'免許更新回数', max_length=45)
    license = models.CharField(u'免許番号', max_length=45)
    email = models.EmailField(u'Email', max_length=45)
    web = models.CharField(u'Webサイト', max_length=45)
    tel_number = models.CharField(u'電話番号', max_length=150)
    company_image = models.FileField(u'イメージ画像')
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'))

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = verbose_name
        db_table = 'company'

    def __str__(self):
        return self.company_name

class CompanyCreate(models.Model):
    """業者登録モデル"""
    id = models.AutoField(primary_key=True)
    is_company = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    user_id = models.IntegerField(_('user_id'))
    company_name = models.CharField(u'会社名', max_length=150)
    address_number = models.CharField(u'郵便番号', max_length=45)
    address = models.CharField(u'住所', max_length=150)
    update_count = models.CharField(u'免許更新回数', max_length=45)
    license = models.CharField(u'免許番号', max_length=45)
    email = models.EmailField(u'Email', max_length=45)
    web = models.URLField(u'Webサイト', max_length=45)
    tel_number = models.CharField(u'電話番号', max_length=150)
    company_image = models.FileField(u'イメージ画像', validators=[FileExtensionValidator(['pdf', 'png', 'jpeg', ])])
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'))

    class Meta:
        verbose_name = _('company create')
        verbose_name_plural = _('company creates')
        db_table = 'company'
