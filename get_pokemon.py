# Pretty printing of the `print_thread` works best if this is run in a shell
import bs4 as bs
import requests
import threading
import pickle
from Pokemon import Pokemon
from time import time
import pdb

"""
The following methods are meant to extract useful information about Pokemon found from span elements.

These span elements are referred to as `cards` 
"""
def get_name(card):
    return card.findAll('a')[1].text

def get_num(card):
    return card.find('small').text

def get_type(card):
    types = []
    for spick in card.findAll('small')[1].findAll('a'):
        types.append(spick.text)
    return types

def get_page(card):
    return card.find('a')['href']

def get_all_pokemon():
    resp = requests.get("https://pokemondb.net/pokedex/national")
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    cards = soup.find_all('span', {'class': 'infocard'})
    if not cards:
        cards = soup.find_all('div', {'class': "infocard"})

    pokemon = []
    for card in cards:
        name = get_name(card)
        num = get_num(card)
        types = get_type(card)
        page = get_page(card)
        if len(types) > 1:
            type2 = types[1]
        else:
            type2 = None
        pokemon.append(Pokemon(name, num, types[0], type2, page))
    return pokemon

print_lock = threading.Lock()

def get_pics(pokemon):
    """Takes a list of Pokémon and associates the appropriate images with the pokemon objects"""
    base = "https://pokemondb.net"
    while len(pokemon) >= 1:
        poke = pokemon.pop()
        resp = requests.get(base+poke.page)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        image = [f for f in soup.findAll('img') if f['src'].endswith('jpg')][0]
        # Create URL to image of the Pokemon
        try:
            img_src = image['src']
            poke.img_src = img_src
        except TypeError:
            with print_lock:
                print(poke.name, "has no image")
                print(poke.page)
            continue

        # Write it to a PNG
        with open('pokepics/' + poke.name + '.png', 'wb') as f:
            pic = requests.get(poke.img_src)
            if pic.status_code == 200:
                f.write(pic.content)
            else:
                print("Status code: " + pic.status_code)

def update_progress(num_start, pokemon):
    while len(pokemon) > 0:
        num = len(pokemon)
        percent = 1.0 - float(num) / num_start
        percent *= 100
        percent = int(percent)
        if percent == 1.0:
            end = ']'
        else:
            end = '>' + ' '*(10 - (percent // 10) - 1) + ']'
        rep = '[' + '='*(percent // 10) + end
        rep += ' {}% completed'.format(percent)
        with print_lock:
            print(rep, end='\r')

if __name__ == '__main__':
    pokemon = get_all_pokemon()
    pdb.set_trace()
    pokemon = sorted(pokemon, key=lambda poke: poke.number)
    poke_copy = pokemon.copy()

    with open("pokemon.pickle", 'wb') as f:
        pickle.dump(poke_copy, f)

    num_poke = len(pokemon)

    print("Collected {} pokemon".format(len(pokemon)))
    print("First few:", pokemon[:5])
    print("Last few:", pokemon[-5:])

    print("Starting Thread execution process")
    start = time()
    NUM_THREADS = 10
    threads = []

    print_thread = threading.Thread(target=lambda: update_progress(num_poke, pokemon))
    print_thread.start()
    # Spawn multiple Threads to query webpages n shit
    for i in range(NUM_THREADS):
        t = threading.Thread(target=lambda: get_pics(pokemon))
        threads.append(t)
        t.start()


    # Wait for Threads to finish
    for t in threads:
        t.join()
    print_thread.join()

    end = time()
    print("Downloading {} Pokémon took {:1f} seconds.".format(num_poke, end - start))
