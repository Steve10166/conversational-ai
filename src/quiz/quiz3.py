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
__author__ = 'Jinho D. Choi'

from emora_stdm import DialogueFlow, Macro, Ngrams
from typing import Dict, Any, List
import re

class MacroGetName(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        r = re.compile(r'(mr|mrs|ms|dr)?([a-z]+)(\s[a-z]+)?$')
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


        return True

transitions = {
    'state': 'start',
        '`Hello, may I have your full name please?`': {
            '#GET_NAME': {
                '`It\'s nice to meet you,`$FIRSTNAME`. Do you feel like sharing a movie that you recently watched?`': {
                    '[{no, not}]': {
                        '`OK then.`': 'end'
                    },
                    '[$FAVORITE_MOVIE=#ONT(marvel)]': {
                        '`I am a super big fan of Marvel series, especially the stories of` $FAVORITE_MOVIE `! Did you enjoy their story?`': {
                            '[{yes, of course}]': {
                                '`Great! Who is your favorite avenger?`': {
                                    '[$FAVORITE_CHAR=#ONT(marvel)]': {
                                        '`I love`$FAVORITE_CHAR`so much!`': 'end'
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`I am sorry to hear that, what happened?`': {
                                    'error': {
                                        '`I understand, goodbye`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(dc)]': {
                        '$FAVORITE_MOVIE `is one of my most favorite series in the DC universe! Do you like '
                        'protagonists or antagonists in the DC universe?`': {
                            '[protagonist]': {
                                '`Great! Why do you like them so much?`': {
                                    'error': {
                                        '`Thank you for sharing!`': 'end'
                                    }
                                }
                            },
                            '[antagonist]': {
                                '`Antagonists in the DC universe do have a charm to them. Why do you like them?`': {
                                    'error': {
                                        '`Thank you for sharing! goodbye`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(action)]': {
                        '`Action movies excites me so much! Especially`$FAVORITE_MOVIE `Do you like action movies?`': {
                            '[{yes, of course}]': {
                                '`Great! Why do you like them?`': {
                                    'error': {
                                        '`That is exactly what I think!`': 'end'
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`Oh, what are some other movie genres you like?`': {
                                    'error': {
                                        '`Thank you for sharing, I will definitely check them out sometime.`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(teendrama)]': {
                        '`I absolutely love teen dystopian movies, especially` $FAVORITE_MOVIE `! Did you like the protagonist?`': {
                            '[{yes, of course}]': {
                                '`Great! Why do you like them so much?`': {
                                    'error': {
                                        '`Of course, I love their bravery and personality.`': 'end'
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`I understand, the antagonists are not necessarily evil, they are only fighting for '
                                'an ideal society. What is your reason for hating the protagonist?`': {
                                    'error': {
                                        '`That is exactly what I think.`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(disney)]': {
                        '`Disney movies like`$FAVORITE_MOVIE`really have a magic to them, don\'t they? Don\'t you think so?`': {
                            '[{yes, of course}]': {
                                '`Great! Which princess do you like?`': {
                                    '[$FAVORITE_PRINCESS=#ONT(princess)]': {
                                        '`I absolutely love`$FAVORITE_PRINCESS': 'end'
                                    },
                                    'error': {
                                        '`I never heard of her before, would you tell me more about her?`': {
                                            'error': {
                                                '`Thank you for sharing, her personality is so charming!`': 'end'
                                            }
                                        }
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`I am sorry to hear that, why would you think that way?`': {
                                    'error': {
                                        '`I understand, goodbye`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(scifi)]': {
                        '`Scifi movies like`$FAVORITE_MOVIE`excite me so much! It is almost like if you are living in '
                        'another universe. A Chinese Sci-fi called Three Body Theorem is coming out, are you gonna watch it?`': {
                            '[{yes, of course}]': {
                                '`Great! Can we watch it together sometimes?`': {
                                    'error': {
                                        '`OK, see you next time.`': 'end'
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`I am sorry to hear that. What are some other sci-fi movies that you recommend?`': {
                                    'error': {
                                        '`OK, I will watch it later.`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(thriller)]': {
                        '`Thrillers like`$FAVORITE_MOVIE`scared me when I was a kid, and they still do now. Do you '
                        'find them scary?`': {
                            '[{yes, of course}]': {
                                '`Exactly, why did you still watch it though?`': {
                                    'error': {
                                        '`Makes sense, I will challenge myself somedays probably.`': 'end'
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`You are such a brave person. Why do you think they are fun to watch?`': {
                                    'error': {
                                        '`That makes sense, maybe I will try it sometime in the future.`': 'end'
                                    }
                                }
                            }
                        }
                    },
                    '[$FAVORITE_MOVIE=#ONT(romance)]': {
                        '`Romantic movies like`$FAVORITE_MOVIE`are sad and enjoyable at the same time, I just could '
                        'not give up watching them. Did you enjoy watching`$FAVORITE_MOVIE`?`': {
                            '[{yes, of course}]': {
                                '`That is awesome, what do you think of the couples?`': {
                                    'error': {
                                        '`That is what I think, they are so cute!`': 'end'
                                    }
                                }
                            },
                            '[{no, not, bad, awful}]': {
                                '`I am sorry to hear that, what happened?`': {
                                    'error': {
                                        '`I am sorry you have to sit through the entire movie...`': 'end'
                                    }
                                }
                            }
                        }
                    },

                    'error': {
                        '`I\'ve never heard of that movie before, would you care to tell me what is it about?`': {
                            '[{no, not}]':{
                                '`Ok then, see you =(`': 'end'
                            },
                            'error': {
                                '`That sounds like a fascinating movie, I will definitely go check it out sometimes.`': 'end'
                            }
                        }
                    }
                }
            },
            'error': {
                '`sorry`': 'end'
            }
        }
}

macros = {
    'GET_NAME': MacroGetName()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.knowledge_base().load_json_file('/Users/steveli/PycharmProjects/conversational-ai/resources/ontology_quiz3.json')
df.add_macros(macros)

if __name__ == '__main__':
    df.run()