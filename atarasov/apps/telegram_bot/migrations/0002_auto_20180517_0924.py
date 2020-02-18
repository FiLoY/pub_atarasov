# Generated by Django 2.0.3 on 2018-05-17 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prep', models.CharField(default='nil', max_length=20, verbose_name='предлог')),
                ('sr1', models.CharField(default='', max_length=60, verbose_name='sort1')),
                ('sr2', models.CharField(default='', max_length=60, verbose_name='sort2')),
                ('grc', models.CharField(default='1', max_length=60, verbose_name='Grammaticalcase')),
                ('rel', models.CharField(default='', max_length=60, verbose_name='wordnumber')),
                ('ex', models.CharField(default='nil', max_length=100, verbose_name='example')),
            ],
            options={
                'db_table': 'bot1_telegram_frp',
            },
        ),
        migrations.CreateModel(
            name='Rqs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prep', models.CharField(default='nil', max_length=20, verbose_name='предлог')),
                ('qw', models.CharField(default='', max_length=60, verbose_name='вопросительное слово')),
                ('relq', models.CharField(default='', max_length=60, verbose_name='')),
            ],
            options={
                'db_table': 'bot1_telegram_rqs',
            },
        ),
        migrations.CreateModel(
            name='Vfr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semsit', models.CharField(default='', max_length=20, verbose_name='вид ситуации')),
                ('form', models.CharField(default='', max_length=60, verbose_name='признак формы глагола')),
                ('refl', models.CharField(default='', max_length=60, verbose_name='признак возратности глагола')),
                ('vc', models.CharField(default='', max_length=60, verbose_name='признаки залога')),
                ('sprep', models.CharField(default='nil', max_length=60, verbose_name='предлог в том числе и состовной')),
                ('grcase', models.CharField(default='1', max_length=60, verbose_name='код подежа')),
                ('str', models.CharField(default='', max_length=100, verbose_name='семантическое ограничение')),
                ('trole', models.CharField(default='', max_length=100, verbose_name='тематическая роль')),
                ('expl', models.CharField(default='nil', max_length=100, verbose_name='example')),
            ],
            options={
                'db_table': 'bot1_telegram_vfr',
            },
        ),
        migrations.RenameModel(
            old_name='Words',
            new_name='Lsdic',
        ),
        migrations.AlterModelTable(
            name='lsdic',
            table='bot1_telegram_lsdic',
        ),
    ]