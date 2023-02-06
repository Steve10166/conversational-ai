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

from emora_stdm import DialogueFlow

transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': {
        '<{appointment, book}, haircut>': {
            '`Sure. What date and time are you looking for?`': {
                '<{tuesday, tue}, [!2 pm]>': {
                    '`Your appointment is set. See you!`': 'end'
                },
                '<{monday, mon}, [!{2 pm, 10 am, 1 pm}]>': {
                    '`Your appointment is set. See you!`': 'end'
                },
                '{<[!{tuesday, tue}, -2 pm, {am, pm}]>, <[!{monday, mon}, -{2 pm, 10 am, 1 pm}, {am, pm}]>, '
                '<{wednesday, thursday, friday, saturday, wed, thur, fri, sat}, {am, pm}>}': {
                    '`Sorry, that slot is not available for a haircut`': {
                        'error': {
                            '`Goodbye`': 'end'
                        }
                    }
                },
                'error': {
                    '`Sorry, I didn\'t understand you.`': 'end'
                }
            }
        },
        '<{appointment, book}, {perm, perms}>': {
            '`Sure. What date and time are you looking for?`': {
                '[{friday, fri}, [!{10 am, 11 am, 1 pm, 2 pm}]]': {
                    '`Your appointment is set. See you!`': 'end'
                },
                '[{saturday, sat}, [!{2 pm, 10 am}]]': {
                    '`Your appointment is set. See you!`': 'end'
                },
                '{[!{friday, fri}, -{10 am, 11 am, 1 pm, 2 pm}, {am, pm}], [!{saturday, sat}, -{2 pm, 10 am}, {am, '
                'pm}], [{monday, tuesday, wednesday, thursday, mon, tue, wed, thur}, {am, pm}]}': {
                    '`Sorry, that slot is not available for a perm`': {
                        'error': {
                            '`Goodbye`': 'end'
                        }
                    }
                },
                'error': {
                    '`Sorry, I didn\'t understand you.`': 'end'
                }
            }
        },
        '<{appointment, book}, hair coloring>': {
            '`Sure. What date and time are you looking for?`': {
                '[{wednesday, wed}, [!{10 am, 11 am, 1 pm}]]': {
                    '`Your appointment is set. See you!`': 'end'
                },
                '[{thursday, thur}, [!{11 am, 10 am}]]': {
                    '`Your appointment is set. See you!`': 'end'
                },
                '{[!{wednesday, wed}, -{10 am, 11 am, 1 pm}, {am, pm}], [!{thur, thursday}, -{11 am, 10 am}, {am, '
                'pm}], [{monday, tuesday, friday, saturday, mon, tue, fri, sat}, {am, pm}]}': {
                    '`Sorry, that slot is not available for a hair coloring`': {
                        'error': {
                            '`Goodbye`': 'end'
                        }
                    }
                },
                'error': {
                    '`Sorry, I didn\'t understand you.`': 'end'
                }
            }
        },
        '<[!{book, appointment}, -{hair coloring, perm, haircut, perms}]>': {
            '`Sorry, we do not provide that service`': {
                'error': {
                    '`Goodbye`': 'end'
                }
            }
        },
        'error': {
            '`Sorry, I didn\'t understand you.`': 'end'
        }
    }
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)

if __name__ == '__main__':
    df.run()