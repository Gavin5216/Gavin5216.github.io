from django.shortcuts import render
import logging
import requests


def home_screen_view(request):
    return render(request, "base.html",{})



def rust_screen_view(request):
    api_key = '648D4A1BA436CF2A80FF60EA3698D48F'
    steam_id = request.GET.get('steamId', '')
    context = rust_stats(api_key, steam_id)
    return render(request, "rust.html", context)



def csgo_screen_view(request):
    api_key = '648D4A1BA436CF2A80FF60EA3698D48F'
    steam_id = request.GET.get('steamId', '')
    context = csgo_stats(api_key, steam_id)
    return render(request, "csgo.html", context)



def csgo_stats(api_key, steam_id):
    app_id_csgo = '730'
    csgo_stats_url = f'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key={api_key}&steamid={steam_id}&appid={app_id_csgo}'
    print(csgo_stats_url)
    csgo_total_kills = ''
    csgo_total_deaths = ''
    csgo_total_wins = ''
    csgo_total_planted_bombs = ''
    playtime_hours = '0'

    try:
        response = requests.get(csgo_stats_url)
        if response.status_code == 200:
            data = response.json()
            for stat in data.get('playerstats', {}).get('stats', []):
                if stat['name'] == 'total_kills':
                    csgo_total_kills = stat['value']
                if stat['name'] == 'total_deaths':
                    csgo_total_deaths = stat['value']
                if stat['name'] == 'total_wins':
                    csgo_total_wins = stat['value']
                if stat['name'] == 'total_planted_bombs':
                    csgo_total_planted_bombs = stat['value']
            #print("CSGO Stats")
            #print(f"Total kills: {csgo_total_kills}")
            #print(f"Total deaths: {csgo_total_deaths}")
            #print(f"Total wins: {csgo_total_wins}")
            #print(f"Total bombs planted: {csgo_total_planted_bombs}")
        else:
            print(f"API Request Failed with Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occured: {str(e)}")
        
    playtime_url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&format=json'
    try:
        response = requests.get(playtime_url)
        if response.status_code == 200:
            data = response.json()
            for game in data.get('response', {}).get('games', []):
                if game.get('appid') == int(app_id_csgo):
                    playtime_minutes = game.get('playtime_forever')
                    playtime_hours = playtime_minutes / 60
                    #print(f"Hours: {int(playtime_hours)}")
                    break
    except Exception as e:
        print(f"An error occured: {str(e)}")

    kd = round(csgo_total_kills / csgo_total_deaths, 2)
    return {'hours': int(playtime_hours), 'kills': csgo_total_kills, 'deaths': csgo_total_deaths, 'wins': csgo_total_wins, 'bombs_planted': csgo_total_planted_bombs, 'kd': kd}



def rust_stats(api_key, steam_id):
    app_id_rust = '252490'
    rust_stats_url= f'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key={api_key}&steamid={steam_id}&appid={app_id_rust}'
    
    try:
        response = requests.get(rust_stats_url)
        if response.status_code == 200:
            data = response.json()
            for stat in data.get('playerstats', {}).get('stats', []):
                if stat['name'] == 'kill_player':
                    rust_kill_player = stat['value']
                if stat['name'] == 'deaths':
                    rust_deaths = stat['value']
                if stat['name'] == 'bullet_fired':
                    rust_bullet_fired = stat['value']
                if stat['name'] == 'headshot':
                    rust_headshot = stat['value']
                if stat['name'] == 'death_suicide':
                    rust_death_suicide = stat['value']
            #print("Rust Stats")
            #print(f"Kills: {rust_kill_player}")
            #print(f"Deaths: {rust_deaths}")
            #print(f"Bullets Fired: {rust_bullet_fired}")
            #print(f"Headshots: {rust_headshot}")
            #print(f"Suicides: {rust_death_suicide}")
        else:
            print(f"API Request Failed with Status Code: {response.status_code}")
    except Exception as e:
            print(f"An error occured: {str(e)}")

    playtime_url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={steam_id}&format=json'
    try:
        response = requests.get(playtime_url)
        if response.status_code == 200:
            data = response.json()
            for game in data.get('response', {}).get('games', []):
                if game.get('appid') == int(app_id_rust):
                    playtime_minutes = game.get('playtime_forever')
                    playtime_hours = playtime_minutes / 60
                    #print(f"Hours: {int(playtime_hours)}")
                    break
    except Exception as e:
        print(f"An error occured: {str(e)}")
    
    kd = round(rust_kill_player / rust_deaths, 2)
    return {'hours': int(playtime_hours), 'kills': rust_kill_player, 'deaths': rust_deaths, 'bullets_fired': rust_bullet_fired, 'headshots': rust_headshot, 'suicides': rust_death_suicide, 'kd': kd}