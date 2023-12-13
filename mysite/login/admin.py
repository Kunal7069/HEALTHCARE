from django.contrib import admin
from login.models import LadleInfo, LadleUpdate , LadleUpdateRoomWise , EntriesAdded

class LadleInfoAdmin(admin.ModelAdmin):
    list_display=('name','stop_point_no','stop_point_work','min_temp','max_temp','turn_around_time')
admin.site.register(LadleInfo,LadleInfoAdmin)

class LadleUpdateAdmin(admin.ModelAdmin):
    list_display=('name','start_time','stop_points','stop_time')
admin.site.register(LadleUpdate,LadleUpdateAdmin)

class LadleUpdateRoomWiseAdmin(admin.ModelAdmin):
    list_display=('name','date','entry_time','room','exit_time','stop_points')
admin.site.register(LadleUpdateRoomWise,LadleUpdateRoomWiseAdmin)

class EntriesAddedAdmin(admin.ModelAdmin):
    list_display=('name','date','count')
admin.site.register(EntriesAdded,EntriesAddedAdmin)
# Register your models here.

    
    
    