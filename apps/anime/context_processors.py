def header_links(request):
    anime_pages = ['anime_list', 'anime_detail', 'anime_format', 'anime_genre', 'anime_status', 'anime_studio',
                   'anime_year', 'anime_season', 'anime_season_and_year', 'add_anime']

    nav_links = []
    menu_links = []

    if request.resolver_match.url_name in anime_pages:
        nav_links.extend([
            {'title': 'Случайное аниме', 'url': 'anime:anime_random'},
        ])
        menu_links.extend([
            {'title': 'Добавить аниме', 'url': 'anime:add_anime'}
        ])

    return {'nav_links': nav_links, 'menu_links': menu_links}
