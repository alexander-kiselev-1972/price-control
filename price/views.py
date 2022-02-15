from django.shortcuts import render
from .forms import LekSearch
from .models import Lek, HistoryPrice


def margin(price):
    price = float(price)
    if price <= 100.00:
        marg_opt = price*1.17 - price
        marg_apt = price*1.32 - price

        price = (price + marg_opt + marg_apt)*1.10
    elif price <=500.00:
        marg_opt = price * 1.1 - price
        marg_apt = price * 1.28 - price

        price = (price + marg_opt + marg_apt) * 1.10
    else:
        marg_opt = price * 1.07 - price
        marg_apt = price * 1.15 - price

        price = (price + marg_opt + marg_apt) * 1.10

    return round(price, 2)


def lek_search(request):
    if request.method == 'POST':
        form = LekSearch(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                try:
                    lek = Lek.objects.get(barcode=cd['barcode'])
                    lek_id = lek.id
                except Exception as o:
                    print("Ошибка get обращения к lek  ", o)

                prices = HistoryPrice.objects.filter(lek=lek_id).order_by('-date_in').first()
                price = prices.price
                print(price)
                price = round(margin(price), 2)

            except Exception as e:
                print(" Ошибка ", e)

                return render(request, 'price/error.html')

            return render(request, 'price/lek_price.html', {'lek': lek, 'prices': prices, 'price': price})

    else:
        form = LekSearch()
    return render(request, 'price/lek_search.html', {'form': form})


def lek_price(request, lek_id):
    pass
