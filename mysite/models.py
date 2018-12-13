from django.contrib import auth
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import validate_email, EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.db.models.manager import EmptyManager

SILENCED_SYSTEM_CHECKS = ["auth.W004"]

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')

        username = self.model.normalize_username(username, required=True)
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
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
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

    def save(self, *args, **kwargs):
        self.article = article
        super(RoomImage, self).save(*args, **kwargs)

class Article(models.Model):
    """カスタム物件モデル."""

    id = models.AutoField(primary_key=True)
    article_name = models.CharField(_('article name'), max_length=150)
    comments = models.CharField(_('comments'), max_length=150)
    room_images = models.ForeignKey(RoomImage, on_delete=models.CASCADE, related_name="image_key")
    article_image = models.ImageField(_('article image'), max_length=150)
    address = models.CharField(_('address'), max_length=150)
    rent = models.CharField(_('rent'), max_length=150)
    park = models.CharField(_('park'), max_length=150)
    initial_cost = models.CharField(_('initial cost'), max_length=150)
    floor_plan = models.CharField(_('floor plan'), max_length=150)
    common_service_expense = models.CharField(_('common service expense'), max_length=150)
    term_of_contract = models.CharField(_('term of contract'), max_length=150)
    floor_number = models.CharField(_('floor number'), max_length=150)
    others = models.ForeignKey(Others, on_delete=models.CASCADE, related_name="comment_key")
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

    class Meta:

        db_table = 'sample_room'

class ArticleFloor(models.Model):
    """サンプル物件モデル(View用)"""

    id = models.AutoField(primary_key=True)
    floor = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="floor_key")

    class Meta:

        db_table = 'sample_floor'
