from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from celery import task
from io import BytesIO
from .models import Order
import weasyprint


@task
def order_created(order_id):

  order = Order.objects.get(id=order_id)
  subject = f'Order nr.{order.id}'
  message = f'Dear {order.first_name}, \n\n' \
            f'Your order was successfully created.\n' \
            f'Your order ID is {order.id}.'

  email = EmailMessage(
    subject, message, settings.DEFAULT_FROM_EMAIL, [order.email]
  )

  html = render_to_string('order/pdf.html', {'order': order})
  out = BytesIO()
  stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
  weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

  email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
  email.send()


@task
def status_change_notification(order_id):

  order = Order.objects.get(id=order_id)
  subject = f'Order nr.{order.id}'
  message = f'Dear {order.first_name}, \n\n' \
            f'Status of your order(nr.{order.id}) has been updated to {order.status}.' 
  mail_sent = send_mail(subject, message, 
    settings.DEFAULT_FROM_EMAIL, [order.email])
  
  return mail_sent
