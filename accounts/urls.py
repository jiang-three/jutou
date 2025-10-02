from django.urls import path, include
from django.http import HttpResponse
from django.core.management import call_command
from . import views

app_name = 'accounts'

def run_migration(request):
    """运行数据库迁移"""
    if request.GET.get('key') == 'NPIG3NAT-5Cf-Jo9dhmpI4Hhfw1KmybtJjwjo3snefnfdhs5f0MLuMmlM1ElGL1eogk':
        try:
            call_command('migrate')
            return HttpResponse('数据库迁移成功！')
        except Exception as e:
            return HttpResponse(f'迁移失败: {str(e)}')
    return HttpResponse('未授权')

def create_superuser(request):
    """创建超级用户"""
    if request.GET.get('key') == 'NPIG3NAT-5Cf-Jo9dhmpI4Hhfw1KmybtJjwjo3snefnfdhs5f0MLuMmlM1ElGL1eogk':
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'jiang44811957')  # 替换为实际密码
            return HttpResponse('超级用户创建成功！')
        return HttpResponse('超级用户已存在')
    return HttpResponse('未授权')

# 正确的 urlpatterns - 包含所有路径
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    # 添加管理命令URL
    path('admin-commands/migrate/', run_migration, name='run_migration'),
    path('admin-commands/create-superuser/', create_superuser, name='create_superuser'),
]
