from django.shortcuts import render
from django.http import Http404
from .models import Portfolio

def portfolio(request, portfolio_id):
    try:
        p = Portfolio.objects.get(pk=portfolio_id)
    except Portfolio.DoesNotExist:
        raise Http404("Portfolio does not exist")


    # list of all assets, ordered by exposure
    # etf1 - 0.4
    # -- asset1 - 0.12
    # -- asset2 - 0.07
    # etf2 - 0.6
    # -- asset1 - 0.05
    # -- asset4 - 0.01

    assets = {}
    for e in p.etfinportfolio_set.all():
        for a in e.etf.assetinetf_set.all():
            if a.asset not in assets:
                weight = a.weight * e.weight / 100
                value = (weight/100) * p.value
                assets[a.asset] = (
                    value,
                    weight,
                    [(e.etf, a.weight)]
                )
            else:
                existing = assets[a.asset]
                weight = a.weight * (e.weight / 100)
                new_total_weight = existing[1] + weight
                value = (weight/100) * p.value
                etf_list = existing[2]
                etf_list.append((e.etf, a.weight))
                assets[a.asset] = (
                    value,
                    new_total_weight,
                    etf_list
                )

    sorted_assets = dict(sorted(assets.items(), key=lambda item: item[1][0], reverse=True))

    return render(request, 'etf/portfolio.html', {'portfolio': p, 'assets': sorted_assets})
