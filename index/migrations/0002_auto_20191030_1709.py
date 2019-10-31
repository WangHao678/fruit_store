# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-30 09:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goodstype',
            options={'verbose_name': '商品类别', 'verbose_name_plural': '商品类别'},
        ),
        migrations.AddField(
            model_name='goods',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goods',
            name='goodsType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.GoodsType'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='spec',
            field=models.CharField(max_length=11, verbose_name='规格'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='title',
            field=models.CharField(max_length=20, verbose_name='商品名称'),
        ),
        migrations.AlterField(
            model_name='goodstype',
            name='title',
            field=models.CharField(max_length=20, verbose_name='品类名称'),
        ),
    ]