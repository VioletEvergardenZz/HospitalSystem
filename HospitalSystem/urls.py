from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from HospitalSystem.settings import DEBUG, MEDIA_ROOT

# 主路由
urlpatterns = [
                  path('admin/', admin.site.urls),  # 后台管理系统
                  path('', include('hospital.url')),  # 挂号预约系统
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 上传媒体文件
if DEBUG:
    from django.views.static import serve

    urlpatterns.append(path('media/(.*)', serve, kwargs={'document_root': MEDIA_ROOT}))
