# Generated by Django 3.2.4 on 2021-06-09 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'actors',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'countries',
                'db_table': 'countries',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'directors',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('runtime', models.CharField(blank=True, max_length=20)),
                ('year', models.IntegerField(blank=True)),
                ('rating', models.FloatField(blank=True)),
                ('review', models.TextField()),
                ('see', models.BooleanField(default=False)),
                ('actors', models.ManyToManyField(blank=True, to='movieCrud.Actor')),
                ('countries', models.ManyToManyField(blank=True, to='movieCrud.Country')),
                ('directors', models.ManyToManyField(blank=True, to='movieCrud.Director')),
            ],
            options={
                'db_table': 'movies',
                'ordering': ['-rating'],
            },
        ),
        migrations.AddField(
            model_name='director',
            name='movies',
            field=models.ManyToManyField(db_table='movie_directors', to='movieCrud.Movie'),
        ),
        migrations.AddField(
            model_name='country',
            name='movies',
            field=models.ManyToManyField(db_table='movie_countries', to='movieCrud.Movie'),
        ),
        migrations.AddField(
            model_name='actor',
            name='movies',
            field=models.ManyToManyField(db_table='movie_actors', to='movieCrud.Movie'),
        ),
    ]
