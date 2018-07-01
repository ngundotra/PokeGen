from Pokemon import Pokemon
import pickle
import numpy as np

def load_poke(fname):
    with open(fname, "rb") as pokepickle:
        all_poke = pickle.load(pokepickle)
    return all_poke

def getTypes(pokes):
    types = []

    for poke in pokes:
        if poke.type1 not in types:
            types.append(poke.type1)
        if poke.type2 and poke.type2 not in types:
            types.append(poke.type2)
    types.append("None")
    return types

def oneHotTypes(pokes):
    """Sets oneHot property of each pokemon to be one hot encoding of types
    e.g. poke.oneHot.shape = (2, {len(types)})"""
    types = getTypes(pokes)
    numTypes = {tipo: i for i, tipo in enumerate(types)}
    num = len(types)

    for poke in pokes:
        oneHot = np.zeros(shape=(2, num))
        oneHot[0, numTypes[poke.type1]] = 1
        if poke.type2:
            oneHot[1, numTypes[poke.type2]] = 1
        else:
            oneHot[1, numTypes["None"]] = 1
        poke.oneHot = oneHot

    return pokes, types, numTypes

def getPaddedPics(pokes):
    max_d = 380 # from a notebook
    imgs = []
    for poke in pokes:
        if poke.load_pic("pokepics"):
            imgs.append(Pokemon.pad_data(poke.img, max_d, max_d))
        else:
            print(poke, "has no image! Appending `None`")
            imgs.append(None)
    return imgs

def getSmallPics(imgs):
    """Shrinks padded imgs from 380->150"""
    import cv2
    outsize = 150

    small = []
    for img in imgs:
        small.append(cv2.resize(img, (outsize, outsize)))
    return np.array(small)

def normalizePics(imgs, val_split=0.2):
    """Returns (train, test), mean, std of pics"""
    train_num = int(len(imgs) * (1 - val_split))
    imgs = imgs - np.min(imgs)
    imgs = imgs / np.max(imgs)

    return


def loadTuples(pokes):
    pokes = oneHotTypes(pokes)


def oneHotName(pokes):
    """Returns a list of one hot names"""
    tokens = set()
    for poke in pokes:
        name = poke.name.lower()
        for char in name:
            tokens.add(char)
    print(len(tokens), "tokens found")

    all_tok = sorted(tokens)
    print(all_tok)

    idx2char = all_tok
    char2idx = {a: i for i, a in enumerate(all_tok)}

    num_tok = len(all_tok)
    names = []
    for poke in pokes:
        name = poke.name.lower()
        new_name = np.zeros((len(name), num_tok))
        for i, char in enumerate(name):
            new_name[i, char2idx[char]] = 1
        names.append(new_name)

    return names, all_tok, idx2char

if __name__ == '__main__':
    pokes = load_poke("pokemon.pickle")
    if len(pokes) != 807:
        raise ValueError("Number of pokemon loaded is not 807: {}".format(len(pokes)))

    oneHotTypes(pokes)