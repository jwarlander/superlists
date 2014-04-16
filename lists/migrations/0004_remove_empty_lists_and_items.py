# encoding: utf8
from django.db import models, migrations

def remove_empty_items(apps, schema_editor):
    Item = apps.get_model("lists", "Item")
    Item.objects.filter(text='').delete()

def remove_empty_lists(apps, schema_editor):
    List = apps.get_model("lists", "List")
    # Take all lists, then exclude those with ANY item with non-empty text
    List.objects.all().exclude(item__text__regex=r'^.+$').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_item_list'),
    ]

    operations = [
        migrations.RunPython(remove_empty_items),
        migrations.RunPython(remove_empty_lists),
    ]
