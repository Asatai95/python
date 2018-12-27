import os
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)

from django.contrib.auth import get_user_model
from mysite.models import Article, RoomImage, Fab, ArticleCreate, ArticleLive, CompanyCreate
from django.db import models
from django.shortcuts import redirect

User = get_user_model()
# Article = Article.objects.all()


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class LoginCustomerForm(AuthenticationForm):
    """業者専用ログインフォーム"""

    class Meta:
        model = User
        # fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        self.fields['username'].widget.attrs.pop("autofocus", None)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        check_email = User.objects.all().filter(email=email)
        if check_email:
            raise forms.ValidationError('このメールアドレスはすでに使用されています')

        return email

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def clean_email(self):
        email = self.cleaned_data['email']
        check_email = User.objects.all().filter(email=email)
        if not check_email:
            raise forms.ValidationError('このメールアドレスは登録されておりません')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""

    class Meta:
        model = User
        fields = ("username", "email", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CreateCompany(forms.ModelForm):
    """業者登録"""

    def clean_email(self):

        email = self.cleaned_data['email']
        print(email)
        try:
            return email
        except:
            raise forms.ValidationError("正しいEmailアドレスを入力してください。")

    class Meta:
        model = CompanyCreate
        fields = ("user_id", "company_name", "address", "license", "email", "web", "tel_number", "company_image",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class Createform(forms.ModelForm):
    """物件登録"""

    CHOICE_Room = (
              ('', '選択肢から選んでください'),
              ('1L', '1L'),
              ('1DK', '1DK'),
              ('1LDK', '1LDK'),
              ('1D', '1D'),
            )

    CHOICE_Floor = (
              ('', '選択肢から選んでください'),
              ('1F', '1F'),
              ('2F', '2F'),
              ('3F', '3F'),
              ('4F', '4F'),
            )

    CHOICE_Park = (
              ('', '選択肢から選んでください'),
              ('駐車場あり', 'あり'),
              ('駐車場なし', 'なし'),
            )

    CHOICE_Vacant = (
              ('', '選択肢から選んでください'),
              ('0', '空室です'),
              ('1', '空室ではないです'),
            )

    rent = forms.CharField(
           label='家賃',
           max_length=150,
           widget=forms.TextInput(attrs={'placeholder':'例: 3万円, 3.5万円'}))

    park = forms.ChoiceField(
           label='駐車場',
           widget=forms.Select,
           choices=CHOICE_Park)

    floor_plan = forms.ChoiceField(
           label="間取り",
           widget=forms.Select,
           choices=CHOICE_Room)

    floor_number = forms.ChoiceField(
           label="階数",
           widget=forms.Select,
           choices=CHOICE_Floor)

    initial_cost = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder':'例: 4万円, 5.5万円'}),
           label='初期費用',
           max_length=150)

    common_service_expense = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder':'例: 1千円, 1千円'}),
           label='共益費', max_length=150)

    term_of_contract = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder':'例: 2年'}),
           label='契約期間', max_length=150)

    column = forms.CharField(
           label='備考',
           widget=forms.Textarea(attrs={'placeholder':'例: ペットOK！'}),
           max_length=150)

    files = forms.FileField(
           label='その他の画像',
           widget=forms.ClearableFileInput(attrs={'multiple':True}),
    )

    live_flag = forms.ChoiceField(
           label="空室情報",
           widget=forms.Select,
           choices=CHOICE_Vacant
     )

    class Meta:
        model = ArticleCreate
        fields = ( "article_image", "article_name", "comments", "address", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):

        tmp_image_id = []
        upload_files = self.files.getlist('files')
        self.instance.files = upload_files[0]
        self.instance.others = []
        other_files = upload_files[1:]
        file_id = Article.objects.order_by('id').reverse()[0]
        for file_image in other_files:
            file_obj = RoomImage.objects.create(article_id=file_id.id, image=file_image)
            tmp_image_id.append(file_obj.id)
            if commit:
                file_obj.save()
            self.instance.others.append(file_obj)
        return super().save(commit)

UploadModelFormSet = forms.modelformset_factory(
    ArticleCreate, form=Createform,
    extra=10
)

class ArticleUpdateForm(forms.ModelForm):
    """物件更新"""

    class Meta:
        model = Article
        fields = ("article_image","article_name", "comments", "address", "rent",
                  "park", "floor_plan", "floor_number", "initial_cost", "common_service_expense",
                  "term_of_contract", "column", "room_images_id", "live_flag", "customer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():

            field.widget.attrs['class'] = 'form-control'
