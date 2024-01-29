from django.db import models
import uuid
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField

ACCOUNT_STATUS = (
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('in-active', 'In-active'),
)

MARITAL_STATUS = (
    ("single", "Single"),
    ("married", "Married"),
    ("other", "Other"),
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)

IDENTITY_TYPE = (
    ("national_id_cart", "National ID Card"),
    ("drives_license", "Driver's License"),
    ("international_passport", "International Passport"),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)


class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # 123 345 654 768
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix='217', alphabet='0123456789') # 217 767 676 767
    account_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix='DEX', alphabet='0123456789') # DEX 767 676 767
    pin_number = ShortUUIDField(unique=True, length=4, max_length=7, alphabet='0123456789') # 4364
    ref_code = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh0123456789') # hgj565h
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default='in-active')
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirm = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='recommended_by')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"


class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="kyc", default='default.jpg')
    marital_status = models.CharField(max_length=100, choices=MARITAL_STATUS)
    gender = models.CharField(max_length=100, choices=GENDER)
    identity_type = models.CharField(max_length=100, choices=IDENTITY_TYPE)
    identity_image = models.ImageField(upload_to="kyc", null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # Address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Contact Detail
    mobile = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"






