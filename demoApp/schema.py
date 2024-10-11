import graphene
from graphene_django.types import DjangoObjectType
from .models import CustomUser,TailorDetail
from django.contrib.auth.hashers import make_password
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from graphql import GraphQLError
# from graphene_file_upload.scalars import Upload
# from django.core.files.uploadedfile import InMemoryUploadedFile




# Configure logging
logger = logging.getLogger(__name__)

# Define the CustomUserType for the GraphQL schema
class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser 
        fields = ("id", "first_name", "last_name", "email")  # Specify fields to expose, # Exclude password for security

# Define TailorDetailType for the TailorDetail model
class TailorDetailType(DjangoObjectType):
    class Meta:
        model = TailorDetail  # Only one model per ObjectType
        fields = ("id", "full_name", "username", "email", "national_id_number", 
                  "phone_number", "sex", "passport_size", "area_of_residence", 
                  "area_of_work", "date_of_registration")  # Specify fields to expose
 

# Define the mutation class for creating a CustomUser
class CreateCustomUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    custom_user = graphene.Field(CustomUserType)

    def mutate(self, info, first_name, last_name, email, password):
        logger.debug(f"Creating user: {first_name} {last_name} with email: {email}")

        # Hash the password before saving
        hashed_password = make_password(password)
        logger.debug("Password hashed successfully.")

        custom_user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )
        custom_user.save()
        logger.info(f"User created successfully: {custom_user.email}")

        return CreateCustomUser(custom_user=custom_user)

# Define the mutation class for obtaining JWT tokens
class obtainJwtToken(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    refresh = graphene.String()
    token = graphene.String()
    user = graphene.Field(CustomUserType)  # Return CustomUserType

    def mutate(self, info, email, password):
        logger.debug(f"Attempting to obtain token for email: {email}")
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise Exception('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        return obtainJwtToken(
            token=str(refresh.access_token),
            refresh=str(refresh),
            user=user  # Return user instance directly
        )
        
# Define a mutation to register TailorDetail
class RegisterTailor(graphene.Mutation):
    tailor = graphene.Field(TailorDetailType)

    class Arguments:
        full_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        national_id_number = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        sex = graphene.String(required=True)
        passport_size = graphene.String(required=True)  # For simplicity, assuming the frontend will send a file path
        area_of_residence = graphene.String(required=True)
        area_of_work = graphene.String(required=True)
        password = graphene.String(required=True)
        
    def mutate(self, info,full_name, username, email, national_id_number, phone_number, sex, passport_size=None, area_of_residence=None, area_of_work=None, password=None):
        if TailorDetail.objects.filter(username=username).exists():
            raise GraphQLError('Username already exists.')
           
        if TailorDetail.objects.filter(email=email).exists():
            raise GraphQLError('Email already exists.')
            
        tailor = TailorDetail(
            full_name=full_name,
            username=username,
            email=email,
            national_id_number=national_id_number,
            phone_number=phone_number,
            sex=sex,
            passport_size=passport_size,
            area_of_residence=area_of_residence,
            area_of_work=area_of_work,
        )
        
        tailor.set_password(password)
        
        # if isinstance(passport_size, InMemoryUploadedFile):  # Ensure it's a file object
        #     tailor.passport_size.save(passport_size.name, passport_size)
            
        tailor.save()
         
        return RegisterTailor(tailor=tailor)

# Define the main Mutation class
class Mutation(graphene.ObjectType):
    pass
    create_custom_user = CreateCustomUser.Field()
    obtain_jwt_token = obtainJwtToken.Field()
    register_tailor = RegisterTailor.Field()

# Define the Query class (optional)
class Query(graphene.ObjectType):
    all_custom_users = graphene.List(CustomUserType)
    all_tailors = graphene.List(TailorDetailType)

    def resolve_all_custom_users(self, info):
        logger.debug("Fetching all custom users.")
        users = CustomUser.objects.all()
        logger.info(f"Fetched {users.count()} users.")
        return users
    
        
    def resolve_all_tailors(self, info):
            logger.debug("Fetching all registered tailors.")
            return TailorDetail.objects.all()

class Mutation(graphene.ObjectType):
    create_custom_user = CreateCustomUser.Field()
    register_tailor = RegisterTailor.Field()   

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
