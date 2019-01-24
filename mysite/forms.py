import os
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)

from django.contrib.auth import get_user_model
from mysite.models import Article, RoomImage, Fab, ArticleCreate, ArticleLive, CompanyCreate, Company, License
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

import re

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

    CHOICE_License_year = (
              ('', '免許の更新回数'),
              ('01', '1'),
              ('02', '2'),
              ('03', '3'),
              ('04', '4'),
              ('04', '5'),
              ('04', '6'),
            )

    address_number = forms.RegexField(
        label = "郵便番号",
        regex=r'^[0-9]+$',
        max_length=7,
        widget=forms.TextInput(attrs={'onKeyUp' : "AjaxZip3.zip2addr(this,'','address','address_city')",
                                      'placeholder': '1002003 ハイフン(-)なし'}),
    )

    address = forms.CharField(
           label="都道府県",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'沖縄県'}),
     )

    address_city = forms.CharField(
            label="市町村区",
            max_length=45,
            widget=forms.TextInput(attrs={'placeholder':'那覇市首里'}),
    )

    address_others = forms.CharField(
            label="番地以降",
            max_length=45,
            widget=forms.TextInput(attrs={'placeholder':'1-23 赤丸ビルディング'}),
    )

    update_count = forms.ChoiceField(
           label="免許更新回数",
           widget=forms.Select,
           choices=CHOICE_License_year
     )

    license = forms.CharField(
           widget=forms.TextInput(attrs={'placeholder':'第12345号'}),
           label='免許番号',
           max_length=45
    )

    def clean_email(self):

        email = self.cleaned_data["email"]
        print(email)
        try:
            if not email:
                raise forms.ValidationError(_("正しいEmailを入力してください"))
            return email
        except:
            raise forms.ValidationError(_("すでに登録されているEmailアドレスです"))


    def clean_tel_number(self):

        tel_number = self.cleaned_data["tel_number"]
        pattern = r"[\(]{0,1}[0-9]{2,4}[\)\-\(]{0,1}[0-9]{2,4}[\)\-]{0,1}[0-9]{3,4}"
        if tel_number:
            if not re.match( pattern, tel_number):
                raise forms.ValidationError(_("正しい電話番号を入力してください"))
        return tel_number

    def clean_web(self):

        url = self.cleaned_data["web"]
        pattern = r'^[a-zA-Z0-9!-/:@.]+$'

        if url:
            if not re.match( pattern, url):
                raise forms.ValidationError(_("正しいURLを入力してください"))

            if not 'http' in url:
                if not 'https' in url:
                    raise forms.ValidationError(_("正しいURLを入力してください"))
        return url

    def clean_image(self):

        image = self.cleaned_data["company_image"]
        if image:
            image_path = image.name
            print(image_path)
            if not image_path in [".jpg", ".png", ".jpeg"]:
                raise forms.ValidationError(_("指定された画像ファイルのみ登録可能です"))
        return image

    def clean_license(self):

        update_date = self.cleaned_data["update_count"]
        license_field = self.cleaned_data["license"]
        license = "("+update_date+")" + license_field
        license_table = License.objects.filter(license=license)
        if not license_table:
            raise forms.ValidationError(_("免許情報が異なります"))

        company = CompanyCreate.objects.all()
        if company.filter(license=license):
            raise forms.ValidationError(_("すでに登録されている免許情報です"))
        try:
            return license
        except :
            raise forms.ValidationError(_("すでに登録されている免許情報です"))

    def clean_license_year(self):

        update_count = self.cleaned_data["update_count"]
        print(update_count)
        return update_count

    def clean_address(self):

        address = self.cleaned_data["address_number"]
        pattern = r'^[a-zA-Z0-9]+$'
        if address:
            if '-' in address:
                raise forms.ValidationError(_("ハイフン(-)を省いてください"))
            if not re.match( pattern, address):
                raise forms.ValidationError(_("正しい郵便番号を入力してください"))
        return address

    class Meta:
        model = CompanyCreate
        fields = ("company_image", "company_name" , "email", "web", "tel_number", )

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
    
    company_id =  forms.IntegerField(label='企業ID')

    address_number = forms.RegexField(
        label = "郵便番号",
        regex=r'^[0-9]+$',
        max_length=7,
        widget=forms.TextInput(attrs={'onKeyUp' : "AjaxZip3.zip2addr(this,'','address','address_city')",
                                      'placeholder': '1002003'}),
    )

    address = forms.CharField(
           label="都道府県",
           max_length=45,
           widget=forms.TextInput(attrs={'placeholder':'沖縄県'}),
     )

    address_city = forms.CharField(
            label="市町村区",
            max_length=45,
            widget=forms.TextInput(attrs={'placeholder':'那覇市首里'}),
    )

    address_others = forms.CharField(
            label="番地以降</br>(アパート名,</br> 部屋番号, </br> etc)",
            max_length=45,
            widget=forms.TextInput(attrs={'placeholder':'1-23 赤丸ビルディング203'}),
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

    def clean_address(self):

        address = self.cleaned_data["address_number"]
        pattern = r'^[a-zA-Z0-9]+$'
        if address:
            if '-' in address:
                raise forms.ValidationError(_("ハイフン(-)を省いてください"))
            if not re.match( pattern, address):
                raise forms.ValidationError(_("正しい郵便番号を入力してください"))
        return address

    class Meta:
        model = ArticleCreate
        fields = ( "article_image", "article_name", "comments", )

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

class CompanyUpdateForm(forms.ModelForm):
    """会社情報更新"""

    class Meta:
        model = Company
        fields = ("company_name", "address_number", "address", "license", "email", "web", "tel_number", "company_image", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():

            field.widget.attrs['class'] = 'form-control'

class ArticleUpdateForm(forms.ModelForm):
    """物件更新"""

    class Meta:
        model = Article
        fields = ("article_image","article_name", "comments", "address", "rent",
                  "park", "floor_plan", "floor_number", "initial_cost", "common_service_expense",
                  "term_of_contract", "column", "room_images_id", "live_flag", "customer",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():

            field.widget.attrs['class'] = 'form-control'

class ChatRoom(forms.ModelForm):
    """チャットルーム"""
    company_id = forms.IntegerField(label='企業ID')
    user_id = forms.IntegerField(label='ユーザーID')
    article_id = forms.IntegerField(label='物件ID')
    chat = forms.CharField(
           label = 'コメント',
           max_length=200,
    )
    to_person = forms.CharField(
           label = '送信相手',
           max_length=45,
    )
    from_person = forms.CharField(
           label = '送信主',
           max_length=45,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():

            field.widget.attrs['class'] = 'form-control'

