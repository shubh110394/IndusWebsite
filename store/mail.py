from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string

class Mailing:
    def mailing_function(mydict):
        print(mydict)
        html_template = 'emailinvoice.html'
        # mydict = {'user':'shubham'}
        html_message = render_to_string(html_template,context = mydict)
        subject = "Thanks for shopping"
        email_from = settings.EMAIL_HOST_USER
        # recipient = "shubham.shrivastava@indusnet.co.in"
        email = EmailMessage(
            subject,
            html_message,
            email_from,
            ['shubham.shrivastava@indusnet.co.in']
        )
        email.content_subtype = 'html'
        # email.send()
        print('went')
        return None


