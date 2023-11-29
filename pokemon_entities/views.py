import folium

from django.shortcuts import render
from django.utils.timezone import localtime

from .models import (Pokemon, PokemonEntity)

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(
            pokemon=pokemon,
            appeared_at__lt=localtime(),
            disappeared_at__gt=localtime()
        )
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.long,
                request.build_absolute_uri(pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.get(id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemons,
        appeared_at__lt=localtime(),
        disappeared_at__gt=localtime()
    )
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.long,
            request.build_absolute_uri(pokemons.image.url)
        )

    if pokemons.parent:
        previous_pokemon = pokemons.parent
        previous_evolution = {
            "title_ru": previous_pokemon,
            "pokemon_id": previous_pokemon.id,
            "img_url": previous_pokemon.image.url
        }
    else:
        previous_evolution = None
    if pokemons.next_evolutions.first():
        next_pokemon = pokemons.next_evolutions.first()
        next_evolution = {
            "title_ru": next_pokemon.title,
            "pokemon_id": next_pokemon.id,
            "img_url": next_pokemon.image.url
        }
    else:
        next_evolution = None

    pokemon = {
        "title_ru": pokemons,
        "title_en": pokemons.title_en,
        "title_jp": pokemons.title_jp,
        "description": pokemons.description,
        "img_url": pokemons.image.url,
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })




  

