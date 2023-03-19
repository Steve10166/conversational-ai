# ========================================================================
# Copyright 2022 Emory University
#
# Licensed under the Apache License, Version 2.0 (the `License`);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an `AS IS` BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
__author__ = 'Steve Li'


from emora_stdm import DialogueFlow, Macro, Ngrams
from typing import Dict, Any, List
import time
import json
import requests
import re
import pickle
import os.path

class MacroGetName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r"(mr|mrs|ms|dr)?([a-z']+)(\s[a-z']+)?$")
        m = r.search(ngrams.text())
        if m is None: return False

        title, firstname, lastname = None, None, None

        if m.group(3):
            firstname = m.group(2)
            lastname = m.group(3)
        elif m.group(2):
            firstname = m.group(1)
            lastname = m.group(2)
        else:
            firstname = m.group(1)

        vars['FIRSTNAME'] = firstname
        vars['LASTNAME'] = lastname
        global name
        name = firstname + lastname
        return True

class MacroTime(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[str]):
        current_time = time.strftime("%H:%M")
        a = int(time.strftime("%H"))
        if 0 <= a <= 6:
            result = "up so early!"
        elif 7 <= a <= 12:
            result = "good morning!"
        elif 13 <= a <= 18:
            result = "good afternoon!"
        elif 19 <= a <= 23:
            result = "good evening!"

        return result

class MacroWeather(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        url = 'https://api.weather.gov/gridpoints/FFC/52,88/forecast'
        r = requests.get(url)
        d = json.loads(r.text)
        periods = d['properties']['periods']
        today = periods[0]
        return today['shortForecast']

class MacroVisits(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        global name
        vn = name
        if vn not in vars:
            vars[vn] = 1
            return 'first'
        else:
            count = vars[vn] + 1
            vars[vn] = count
            match count:
                case 2: return 'second'
                case 3: return 'third'
                case default: return '{}th'.format(count)

class MacroRecommended(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        global name
        mn = name + 'movie'
        vgenre = name + 'genre'
        if mn not in vars or vgenre not in vars:
            return False
        else:
            return True

class MacroNRecommended(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        global name
        mn = name + 'movie'
        if mn not in vars:
            return True
        else:
            return False

class MacroGetMovie(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        genres = ['captain america', 'superman', 'godzilla vs kong', 'hunger games', 'encanto', 'interstellar', 'unfriended', 'titanic']
        genresM = ['Unity by Thefatrat', 'California soil by London Grammar', 'Summertime sadness by Lana Del Rey', 'Wrecking ball by Miley Cyrus', 'Willpower by loutlander', 'interstellar by Hans Zimmer ', 'Solitude by M83']
        global name
        vgenre = name + 'genre'
        mn = name + 'movie'
        if vgenre in vars:
            count = vars[vgenre]
        else:
            count = 0
        res = name + 'music'
        if res not in vars:
            vars[res] = 1
        if vars[res] == 1:
            return genres[count]
        else:
            return genresM[count]

class MacroInsMovie(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        global name
        vgenre = name + 'genre'
        mn = name + 'movie'
        vars[mn] = vars[vgenre]
         #1 for movie, 0 for music
        return True

class MacroGenre(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        genres = ['captain america', 'superman', 'godzilla vs kong', 'hunger games', 'encanto', 'interstellar', 'unfriended', 'titanic']
        global name
        vgenre = name + 'genre'
        if vgenre not in vars:
            vars[vgenre] = 0
            count = vars[vgenre]
            return genres[count]
        else:
            count = vars[vgenre] + 1
            if count >= 8:
                count = 0
            vars[vgenre] = count
        return genres[count]

class MacroEXPGenre(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        genres = ['captain america', 'superman', 'godzilla vs kong', 'hunger games', 'encanto', 'interstellar', 'unfriended', 'titanic']
        explain = ['an american soldier got frozen in ice for about a decade. He is discovered to have superhuman '
                   'abilities due to the injection of a serum','a man who has superhuman abilities, including '
                                                               'incredible strength, speed, and the ability to fly. '
                                                               'He also has x-ray vision, heat vision, and the power '
                                                               'to freeze objects with his breath. As a young man, '
                                                               'he decides to use his powers to help others and '
                                                               'becomes the superhero known as Superman.','two iconic '
                                                                                                          'creatures '
                                                                                                          'from the '
                                                                                                          'world of '
                                                                                                          'cinema - '
                                                                                                          'Gorilla '
                                                                                                          'and Kong. '
                                                                                                          'Gorillas '
                                                                                                          'are the '
                                                                                                          'largest '
                                                                                                          'primates '
                                                                                                          'on earth '
                                                                                                          'and are '
                                                                                                          'known for '
                                                                                                          'their '
                                                                                                          'incredible '
                                                                                                          'strength '
                                                                                                          'and '
                                                                                                          'intelligence. Kong, on the other hand, is a giant ape who has been the subject of numerous movies and adaptations over the years. In the original King Kong film, Kong is captured and brought to New York City, where he wreaks havoc before ultimately falling to his death. In recent years, the two creatures have been pitted against each other in the popular film franchise, with the latest installment, "Godzilla vs. Kong," featuring an epic battle between the two monsters. Despite their differences, both Gorilla and Kong have captured the hearts and imaginations of audiences around the world, and their legacies continue to endure.', 'a dystopian world where children are forced to fight to the death in a televised event called the Hunger Games. The series is set in the country of Panem, which is ruled by the wealthy and powerful Capitol. The Games are a way for the Capitol to remind the districts of their power and control, as each district must send two "tributes" to compete in the deadly competition. The series follows the story of Katniss Everdeen, a young girl from District 12 who volunteers to take her younger sister\'s place in the Games. Along with her fellow tribute, Peeta Mellark, Katniss must fight to survive in a brutal arena filled with deadly traps and other tributes who are just as determined to win. As the series progresses, Katniss becomes a symbol of rebellion against the Capitol and their cruel regime, inspiring others to rise up and fight for their freedom.', 'a magical Colombian family called the Madrigals, who all possess unique abilities except for the youngest member, Mirabel. The family lives in a magical house called the Encanto, which bestows gifts on each family member, from superhuman strength to the ability to control the weather. However, when the magic of the Encanto begins to fade, the Madrigals must come together to save their home and their family before it\'s too late. Along the way, Mirabel discovers the true power of her own gifts and the importance of family, even in the face of adversity. Encanto is a heartwarming tale that celebrates the power of family, the beauty of Colombian culture, and the magic of the human spirit.', 'a near-future world where Earth is on the brink of environmental collapse, and a group of astronauts are sent on a mission to find a new habitable planet. Led by Cooper, a former pilot turned farmer, the crew must navigate through a wormhole in space to explore three potential new worlds. Along the way, they encounter mind-bending phenomena and challenges that test their endurance and their understanding of time and space. As the mission progresses, Cooper must make a difficult decision that could determine the fate of humanity and his own family. Interstellar is a thought-provoking sci-fi epic that explores themes of love, sacrifice, and the nature of human existence.', 'a found footage horror film that takes place entirely on a computer screen. The movie follows a group of high school friends who are haunted by a vengeful ghost that appears online during a group video chat. The ghost is seeking revenge for a cyberbullying incident that led to a classmate\'s suicide. As the group tries to figure out how to stop the ghost, they become trapped in a terrifying game of truth or dare that leads to deadly consequences. Unfriended is a unique and unsettling horror film that explores the dark side of social media and the dangers of online anonymity.', 'the story of Jack, a penniless artist, and Rose, a wealthy socialite, who fall in love aboard the Titanic, a luxurious and supposedly unsinkable ocean liner. However, their love is put to the test when the ship collides with an iceberg and begins to sink. As chaos and panic ensue, Jack and Rose must fight for survival and make difficult choices that could ultimately determine their fate. The movie is a poignant and epic portrayal of the tragic events that unfolded on the Titanic\'s maiden voyage, highlighting themes of love, class, and the human spirit in the face of disaster.']
        explainM = ['a vibrant electronic music that will almost surely cheer you up', 'a reflection on the band\'s experiences living in California and the emotions that come with leaving a place behind. The lyrics describe the beauty of the California landscape, from the sunsets to the ocean waves, and the sense of freedom that comes with living in such an iconic place. However, the song also acknowledges the darker side of California, with lines that speak to the loneliness and isolation that can come with chasing dreams in such a vast and competitive place. "California Soil" is a hauntingly beautiful song that captures the bittersweet feelings of nostalgia, longing, and hope that come with leaving a place behind.','a song by American singer Lana Del Rey, released in 2012. The song is a melancholic ballad that explores the themes of love and loss during the summer season. The lyrics describe the feelings of sadness and emptiness that can arise when a summer romance comes to an end, with lines like "I got my red dress on tonight, dancing in the dark in the pale moonlight, done my hair up real big beauty queen style, high heels off, I\'m feeling alive." Despite the upbeat melody, the song\'s lyrics paint a picture of a relationship that is fading away, with the singer longing for a lost love. "Summertime Sadness" is a powerful and emotional song that captures the fleeting nature of summer romances and the heartache that can come with them.','a emotional ballad that explores the pain of a failed relationship and the process of moving on', 'a lofi music that will relax you', 'a song from interstellar movie OST, it has a strong futuristic feeling to it.', 'a song by M83, a melancholic song that gives an otherworldly feeling to its listeners']
        global name
        vgenre = name + 'genre'
        res = vars[vgenre]

        y = name + 'music'
        if vars[y] == 1:
            return explain[res]
        else:
            return explainM[res]

class MacroMGenre(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        genres = ['Unity by Thefatrat', 'California soil by London Grammar', 'Summertime sadness by Lana Del Rey', 'Wrecking ball by Miley Cyrus', 'Willpower by loutlander', 'interstellar by Hans Zimmer ', 'Solitude by M83']
        global name
        vgenre = name + 'genre'
        if vgenre not in vars:
            vars[vgenre] = 0
            count = vars[vgenre]
            return genres[count]
        else:
            count = vars[vgenre] + 1
            if count >= 7:
                count = 0
            vars[vgenre] = count
        return genres[count]

class MacroMusic(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        global name
        res = name + 'music'
        vars[res] = 0
        return True

class MacroMovie(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        global name
        res = name + 'music'
        vars[res] = 1
        return True

def visits() -> DialogueFlow:
    transitions = {
        'state': 'start',
            '#GET_TIME`It is`#WEATHER`outside. What is your full name?`' : {
                '#GET_NAME': 'greeting'
            },
            '#GET_TIME`It is`#WEATHER`outside. May I have your full name please?`': {
                '#GET_NAME': 'greeting'
            },
            '#GET_TIME`It is`#WEATHER`outside. Please enter your full name to login`': {
                '#GET_NAME': 'greeting'
            },
            '#GET_TIME`It is`#WEATHER`outside. May I have your first and last name please?`': {
                '#GET_NAME': 'greeting'
            },
            '#GET_TIME`It is`#WEATHER`outside. Can I have your first and last name please?`': {
                '#GET_NAME': 'greeting'
            }
        }
    greeting_transitions = {
        'state': 'greeting',
            '#IF(#RECOMMENDED)`Welcome back`$FIRSTNAME`, it is your`#VISITS`time here. How was` #GETMOVIE `that I recommended you last time`': {
                '{[great], [awesome], [love], [adore], [favorite]}': {
                    '`glad to hear that. What else do you want me to recommend this time?`': {
                        '[{movies, films, cinemas, movie, film, cinema}]': 'movie',
                        '[{song, music, tune, songs, musics, tunes}]': 'music',
                        'error': {
                            '`sorry, I didn\'t understand that `': 'end'
                        }
                    }
                },
                '{[terrible], [horrible], [bad], [awful], [hate], [mediocre], [boring], [so-so]}': {
                    'Oh no, I am so sorry to hear that you didnt like it. What else do you want me to recommend this time, let us see if you will like it':{
                        '[{movies, films, cinemas, movie, film, cinema}]': 'movie',
                        '[{song, music, tune, songs, musics, tunes}]': 'music',
                        'error': {
                            '`sorry, I didn\'t understand that `': 'end'
                        }
                    }
                },
                'error': {
                    '`sorry, I didn\'t understand that `': 'end'
                }
            },
            '#IF(#NRECOMMENDED)`Welcome`$FIRSTNAME`, it is your`#VISITS`time here. What would you like me to recommend?`': {
                '[{movies, films, cinemas, movie, film, cinema}]': 'movie',
                '[{song, music, tune, songs, musics, tunes}]': 'music',
                'error': {
                    '`sorry, I didn\'t understand that `': 'end'
                }
            },
            'error': 'start'
    }

    movies_transitions = {
        'state': 'movie',
        '#CHANGEMOVIE`How about`#NEVERGENRE': {
            '[{no, <already, watched>, bad, hate, boring, not}]': 'movie',
            '[{what, about, explain, brief}]':{
                '`It is about`#EXPGENRE':{
                    '[{no, <already, watched>, bad, hate, boring, not}]': 'movie',
                    '[{yes, sure, <will, watch>, ok, great, fun, interesting, good}]': {
                        '#INSMOVIE`enjoy it, then!`':'end'
                    },
                    'error': 'movie'
                }
            },
            '[{yes, sure, <will, watch>, ok, great, fun, interesting, good, suitable}]': {
                '#INSMOVIE`enjoy it, then!`': 'end'
            },
            'error': 'movie'
        }
    }

    music_transitions = {
        'state': 'music',
        '#CHANGEMUSIC`How about`#NEVERMGENRE': {
            '[{no, <already, listened>, bad, hate, boring, not}]': 'music',
            '[{what, about, explain, brief}]':{
                '`It is `#EXPGENRE':{
                    '[{no, <already, listened>, bad, hate, boring, not}]': 'music',
                    '[{yes, sure, <will, watch>, ok, great, fun, interesting, good}]': {
                        '#INSMOVIE`enjoy it, then!`':'end'
                    },
                    'error': 'music'
                }
            },
            '[{yes, sure, <will, check>, ok, great, fun, interesting, good, suitable}]': {
                '#INSMOVIE`enjoy it, then!`': 'end'
            },
            'error': 'music'
        }
    }

    df = DialogueFlow('start', end_state='end')
    df.load_transitions(transitions)
    df.load_transitions(music_transitions)
    df.load_transitions(movies_transitions)
    df.load_transitions(greeting_transitions)
    df.add_macros(macros)
    return df


macros = {
    'GET_TIME': MacroTime(),
    'WEATHER': MacroWeather(),
    'GET_NAME': MacroGetName(),
    'VISITS': MacroVisits(),
    'RECOMMENDED': MacroRecommended(),
    'NRECOMMENDED': MacroNRecommended(),
    'GETMOVIE': MacroGetMovie(),
    'INSMOVIE': MacroInsMovie(),
    'NEVERGENRE': MacroGenre(),
    'EXPGENRE': MacroEXPGenre(),
    'NEVERMGENRE': MacroMGenre(),
    'CHANGEMUSIC': MacroMusic(),
    'CHANGEMOVIE': MacroMovie()
}

def save(df: DialogueFlow, varfile: str):
    df.run()
    d = {k: v for k, v in df.vars().items() if not k.startswith('_')}
    pickle.dump(d, open(varfile, 'wb'))

def load(df: DialogueFlow, varfile: str):
    d = pickle.load(open(varfile, 'rb'))
    df.vars().update(d)
    df.run()
    save(df, varfile)

if __name__ == '__main__':
    path = 'resources/visits.pkl'
    check_file = os.path.isfile(path)
    name = None
    if not check_file:
        save(visits(), 'resources/visits.pkl')
    else:
        load(visits(), 'resources/visits.pkl')