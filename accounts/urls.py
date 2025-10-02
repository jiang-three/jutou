from django.urls import path, include
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model
from . import views

app_name = 'accounts'

def run_migration(request):
    """运行数据库迁移"""
    admin_key = os.environ.get('ADMIN_COMMAND_KEY', 'NPIG3NAT-5Cf-Jo9dhmpI4Hhfw1KmybtJjwjo3snefnfdhs5f0MLuMmlM1ElGL1eogk')
    if request.GET.get('key') == admin_key:
        try:
            call_command('migrate')
            return HttpResponse('✅ 数据库迁移成功！')
        except Exception as e:
            return HttpResponse(f'❌ 迁移失败: {str(e)}')
    return HttpResponse('❌ 未授权')

def create_users(request):
    """创建多个用户"""
    admin_key = os.environ.get('ADMIN_COMMAND_KEY', 'NPIG3NAT-5Cf-Jo9dhmpI4Hhfw1KmybtJjwjo3snefnfdhs5f0MLuMmlM1ElGL1eogk')
    if request.GET.get('key') == admin_key:
        User = get_user_model()
        results = []
        
        # 要创建的用户列表
        users_to_create = [
            {'username': 'admin', 'password': 'Admin123!', 'email': 'admin@example.com', 'is_superuser': True},
            {'username': '小鹿', 'password': 'jiang448119', 'email': 'zhihu@example.com', 'is_superuser': False},
            {'username': '耗子','password': 'zhy12345678', 'email': 'test@example.com', 'is_superuser': False},
            {'username': '老吊', 'password': 'zxc66668888', 'email': 'zhihu@example.com', 'is_superuser': False},
            {'username': '贝肯'，'password': 'ljl00000000', 'email': 'test@example.com', 'is_superuser': False},
        ]
        
        for user_data in users_to_create:
            if not User.objects.filter(username=user_data['username']).exists():
                if user_data['is_superuser']:
                    user = User.objects.create_superuser(
                        user_data['username'],
                        user_data['email'],
                        user_data['password']
                    )
                else:
                    user = User.objects.create_user(
                        user_data['username'],
                        user_data['email'],
                        user_data['password']
                    )
                results.append(f"✅ 创建用户: {user_data['username']} / {user_data['password']}")
            else:
                results.append(f"ℹ️ 用户已存在: {user_data['username']}")
        
        return HttpResponse('<br>'.join(results))
    return HttpResponse('❌ 未授权')

def check_users(request):
    """检查现有用户"""
    admin_key = os.environ.get('ADMIN_COMMAND_KEY', 'NPIG3NAT-5Cf-Jo9dhmpI4Hhfw1KmybtJjwjo3snefnfdhs5f0MLuMmlM1ElGL1eogk')
    if request.GET.get('key') == admin_key:
        User = get_user_model()
        users = User.objects.all().order_by('date_joined')
        
        if not users:
            return HttpResponse('📭 数据库中没有用户')
        
        result = ["<h1>📋 用户列表</h1>"]
        for user in users:
            result.append(
                f"<p>👤 <strong>{user.username}</strong> | "
                f"邮箱: {user.email} | "
                f"超级用户: {'✅' if user.is_superuser else '❌'} | "
                f"注册时间: {user.date_joined}</p>"
            )
        
        return HttpResponse(''.join(result))
    return HttpResponse('❌ 未授权')

# URL 配置
urlpatterns = [
    # 原有的认证 URL
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    
    # 管理命令 URL
    path('admin-commands/migrate/', run_migration, name='run_migration'),
    path('admin-commands/create-users/', create_users, name='create_users'),
    path('admin-commands/check-users/', check_users, name='check_users'),
]
