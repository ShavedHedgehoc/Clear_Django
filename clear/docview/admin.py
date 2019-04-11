from django.contrib import admin

# Register your models here.

from .models import(
    Row_id,
    Batch_pr,
    Raw_material,
    Lot,
    W_user,
    Weighting,
    Production2,
)

admin.site.register(
    (
        Row_id,
        Batch_pr,
        Raw_material,
        Lot,
        W_user,
        Weighting,
        Production2,
    )
)
