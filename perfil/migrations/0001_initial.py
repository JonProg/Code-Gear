# Generated by Django 4.2.3 on 2023-07-29 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idade', models.PositiveIntegerField()),
                ('data_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=11)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfis',
            },
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=5)),
                ('complemento', models.CharField(max_length=30)),
                ('bairro', models.CharField(max_length=30)),
                ('cep', models.CharField(max_length=8)),
                ('cidade', models.CharField(max_length=30)),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('PA', 'Pará'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('TO', 'Tocatins'), ('MA', 'Maranhâo'), ('PB', 'Paraíba'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RN', 'Rio Grande do Norte'), ('SE', 'Sergipe'), ('GO', 'Goiás'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('ES', 'Espírito Santo'), ('MG', 'Minas Gerais'), ('RJ', 'Rio de Janeiro'), ('SP', 'São Paulo'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'), ('AM', 'Amazonas'), ('AP', 'Amapá'), ('AL', 'Alagoas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('PR', 'Paraná')], max_length=2)),
                ('perfil_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfil.perfilusuario')),
            ],
        ),
    ]
