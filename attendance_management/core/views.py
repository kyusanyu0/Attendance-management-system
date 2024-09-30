from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import logout
from .forms import CustomUserCreationForm 
from django.contrib.auth.forms import UserCreationForm
from .models import AttendanceRecord,User

def employee_dashboard(request):
    if request.method == 'POST':
        # 出勤打刻
        if 'check_in' in request.POST:
            # 同日に出勤打刻がない場合のみ、出勤時間を記録
            today = timezone.now().date()
            attendance_record, created = AttendanceRecord.objects.get_or_create(
                user=request.user,
                check_in__date=today,
                defaults={'check_in': timezone.now()}
            )
            if not created:
                # 既に出勤打刻がある場合のメッセージやエラーハンドリングをここで行う
                pass

        # 退勤打刻
        if 'check_out' in request.POST:
            # 今日の出勤記録がある場合、その記録の退勤時間を更新
            try:
                attendance_record = AttendanceRecord.objects.get(
                    user=request.user,
                    check_in__date=timezone.now().date()
                )
                if attendance_record.check_out is None:
                    attendance_record.check_out = timezone.now()
                    attendance_record.save()
                else:
                    # 既に退勤打刻がされている場合のメッセージやエラーハンドリング
                    pass
            except AttendanceRecord.DoesNotExist:
                # 出勤記録がない場合のエラーハンドリング
                pass
        
        if 'reset_records' in request.POST:
            # リセット処理：すべての記録を削除
            AttendanceRecord.objects.filter(user=request.user).delete()

            # メッセージやリダイレクト処理
            return redirect('employee_dashboard')

    return render(request, 'employee_dashboard.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employer_dashboard' if user.user_type == 'employer' else 'employee_dashboard')
    return render(request, 'login.html')

def attendance_records(request):
    records = AttendanceRecord.objects.filter(user=request.user)
    return render(request, 'attendance_records.html', {'records': records})



def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = request.POST['user_type']  # ユーザータイプを取得
            user.save()
            return redirect('employer_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'add_user.html', {'form': form})

def employer_dashboard(request):
    return render(request, 'employer_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('start')


def start(request):
    return render(request, 'start.html')  # start.html テンプレートを表示


