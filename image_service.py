from stablelib import generate
from config import wordlistv2
from random import choice
from typing import List
from typing import Tuple
from secrets import token_urlsafe

from config import FOLDER_NEW




def generate_random(wordlist: List[str], folder: str, resolution: Tuple[int, int] = (512, 512), steps: int = 5):
    
    word = choice(wordlist)
    img = generate(word, resolution[0], resolution[1], steps=steps)
    img.save(f'{folder}/{word}-{token_urlsafe(6)}.png')




if __name__ == "__main__":
    while True:
        generate_random([k for k in wordlistv2], FOLDER_NEW, (512, 512), 9)
        print("generated image")