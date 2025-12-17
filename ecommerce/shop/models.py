
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify



class ActiveManager(models.Manager):
    def get_queryset(self):    
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    status_flag = models.CharField(max_length=32, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    active_from = models.DateTimeField(blank=True, null=True)
    active_to = models.DateTimeField(blank=True, null=True)

    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)

    cuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_%(class)s"
    )
    muser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="modified_%(class)s"
    )

    is_deleted = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)     
        extra_fields.setdefault("is_superuser", True) 
        extra_fields.setdefault("is_customer", False)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=32, unique=True, blank=True, null=True)

    is_admin = models.BooleanField(default=False)      
    is_staff = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)  
    is_customer = models.BooleanField(default=True)    
    is_active = models.BooleanField(default=True)

    
    otp = models.CharField(max_length=16, default="1234")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []   

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Store(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="stores")
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name



class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - {self.name}"



class Product(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sku = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    inventory_count = models.IntegerField(default=0)

    weight = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True)
    attributes = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class ProductImage(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)



class Order(BaseModel):
    STATUS = [
        ("CART", "Cart"),          
        ("PLACED", "Placed"),
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.JSONField(blank=True, null=True)
    billing_address = models.JSONField(blank=True, null=True)
    item_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=32, choices=STATUS, default="PENDING")
    def __str__(self):
        return f"Order {self.id} - {self.user}"


class OrderDetail(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sku = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    metadata = models.JSONField(blank=True, null=True)



class Invoice(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice_obj")
    invoice_number = models.CharField(max_length=128, unique=True)
    issued_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    taxes = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class Payment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(max_length=64)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=64, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)



class Address(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=128, blank=True, null=True)
    data = models.JSONField() 



class Coupon(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    min_order_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)

    usage_limit = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)



class AuditLog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False) 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=100)
    table_name = models.CharField(max_length=100)
    record_id = models.CharField(max_length=100)
    old_data = models.JSONField(blank=True, null=True)
    new_data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action} on {self.table_name} ({self.record_id})"
