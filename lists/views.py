from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List

def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        item = Item(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
            item.save()
            return redirect(list_)
        except:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': list_, 'error': error})

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(list_)
