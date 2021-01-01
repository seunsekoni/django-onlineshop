from io import BytesIO
from celery import shared_task
import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from orders.models import Order
from django.template.loader import render_to_string

@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    message = 'Please, find attached the invoice for your recent purchase.'
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - EE Invoice no. {order_id}'
    email = EmailMessage(subject, 'Please, find attached the invoice for your recent purchase.', 'noreply@onlineshop.com', [order.email])

    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    print(out)
    print(out.getvalue())
    # weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')])
    stylesheets=[weasyprint.CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)

    email.attach(f'order_{order.id}.pdf',
                    out.getvalue(),
                    'application/pdf')
    # send e-mail
    email.send()
