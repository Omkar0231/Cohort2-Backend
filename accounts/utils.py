import  random
from django.core.mail import send_mail
from .models import  EmailOTP


def send_otp_to_email(email, otp):
    otp= str(random.randint(100000, 999999))
    EmailOTP.objects.create(email=email, otp=otp)

    send_mail(
        'Your OTP for Mentor Dashboard Login',
        f'Use this OTP to login:{otp}',
        'your_email@example.com'
        [email],
        fail_silently=False,
    )
    return otp