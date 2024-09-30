#!/usr/bin/env wolframscript
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # カスタムユーザーモデルをインポート

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')  # 必要なフィールドを追加
