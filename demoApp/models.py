from multiprocessing.managers import BaseManager
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,
                    first_name=None, 
                    last_name=None, 
                    email=None, 
                    password=None,
                    full_name=None, 
                    username=None, 
                    national_id_number=None,
                    phone_number=None,
                    sex=None,
                    passport_size=None,
                    area_of_residence=None,
                    area_of_work=None,
                    date_of_registration=None,
                    ):
        if not first_name or not last_name or not email:
            raise ValueError('First name, last name, and email are required fields.')
        
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            full_name=full_name,
            username=username,
            national_id_number=national_id_number,
            phone_number=phone_number,
            sex=sex,
            passport_size=passport_size,
            area_of_residence=area_of_residence,
            area_of_work=area_of_work,
            date_of_registration=date_of_registration,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name=None, last_name=None, email=None, password=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


#CustomerUser Details
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()  # Use your custom UserManager here
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
    
    class Meta:
        ordering = ['first_name']
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
#Product details    
class ProductDetail(models.Model,):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    suk = models.CharField(max_length=100)
    suk = models.CharField(max_length=100)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True, related_name='products')
        
    
    def clean(self):
        if self.cost < 0:
             raise ValidationError('Cost cannot be negative.')

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

# Tailor Details
class TailorDetail(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager() 
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'username', 'national_id_number', 'phone_number']
    
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    national_id_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    passport_size = models.CharField( max_length=255)  # Passport size photo
    area_of_residence = models.CharField(max_length=255)
    area_of_work = models.CharField(max_length=255)
    date_of_registration = models.DateField(auto_now_add=True)
    
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='tailordetail_set',
        blank=True,
    )
    user_permissionss = models.ManyToManyField(
        'auth.Permission',
        related_name='tailordetail_set',
        blank=True,
    )

    def __str__(self):
        return self.full_name

# Tailor Products
class TailorProduct(models.Model):
    CATEGORY_CHOICES = [
        ('SUIT', 'Suit'),
        ('TSHIRT', 'T-Shirt'),
        ('TROUSER', 'Trouser'),
        ('GAUNI', 'Gauni'),
       
    ]

    tailor = models.ForeignKey(TailorDetail, related_name='products', on_delete=models.CASCADE)  # Link to Tailor
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    product_name = models.CharField(max_length=255)
    product_image = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    measurement_guides = models.TextField()  # Measurement instructions for this product
    
    def clean(self):
        if self.cost < 0:
             raise ValidationError('Cost cannot be negative.')
         
    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method before saving
        super().save(*args, **kwargs)     

    def __str__(self):
        return f"{self.product_name} - {self.category}"    