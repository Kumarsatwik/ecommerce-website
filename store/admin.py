from django.contrib import admin
from store.models import Product,Category,Customer,Order
# Register your models here.


class productAdmin(admin.ModelAdmin):
	list_display=['name','price','description','category','image']

class categoryAdmin(admin.ModelAdmin):
	class Meta:
		models='__all__'
class customerAdmin(admin.ModelAdmin):
	class Meta:
		models='__all__'

class orderAdmin(admin.ModelAdmin):
	class Meta:
		models='__all__'

admin.site.register(Order,orderAdmin)
admin.site.register(Customer,customerAdmin)
admin.site.register(Product,productAdmin)
admin.site.register(Category,categoryAdmin)