
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import account.urls
import app.urls
import account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(account.urls)),
    path('show/', include(app.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'account.views.err404'
# handler500 = 'account.views.500'
# handler403 = 'account.views.403'
# handler400 = 'account.views.400'
