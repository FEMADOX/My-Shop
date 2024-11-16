from django.urls import path

from payment import views, weebhooks

app_name = "payment"

urlpatterns = [
    path("process/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("weebhook/", weebhooks.stripe_weebhook, name="stripe-weebhook"),
]
