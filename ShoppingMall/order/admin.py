from django.contrib import admin
from .models import Order
from django.utils.html import format_html
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    # list_display 안에는 변수 뿐만 아니라, 함수도 사용할 수 있다
    list_display = ('user', 'product', 'styled_status')

    def styled_status(self, obj):
        if obj.status == '환불':
            return format_html(f'<span style="color:red">{obj.status}</span>')
        elif obj.status == '결제완료':
            return format_html(f'<span style="color:green">{obj.status}</span>')
        return obj.status

    styled_status.short_description = '상태'


admin.site.register(Order, OrderAdmin)
