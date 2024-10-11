# Generated by Django 4.2.16 on 2024-10-08 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("demoApp", "0003_tailordetail_tailorproduct"),
    ]

    operations = [
        migrations.AddField(
            model_name="tailordetail",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="tailordetail_set", to="auth.group"
            ),
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="superuser status",
            ),
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="password",
            field=models.CharField(default=0, max_length=128, verbose_name="password"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddField(
            model_name="tailordetail",
            name="user_permissionss",
            field=models.ManyToManyField(
                blank=True, related_name="tailordetail_set", to="auth.permission"
            ),
        ),
        migrations.AddField(
            model_name="tailorproduct",
            name="tailor",
            field=models.ForeignKey(
                default=1234,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="demoApp.tailordetail",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customuser",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="customuser_set", to="auth.group"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True, related_name="customuser_set", to="auth.permission"
            ),
        ),
    ]
