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

from emora_stdm import DialogueFlow, Ngrams, Macro
from typing import Dict, Any, List
import openai
import json
import re

PATH_API_KEY = 'resources/openai_api.txt'
openai.api_key_path = PATH_API_KEY


class MacroHair(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        model = 'gpt-3.5-turbo'
        content = 'The user wants to make appointment for a haircut, I asked the user \'What date and time are you ' \
                  'looking for?\' Haircut is only available on Monday 10 AM, 1 PM, 2 PM and Tuesday at 2 PM, ' \
                  'based on the following response from user, return True if the user a valid time, False if ' \
                  'otherwise, (the user may type extra words other than time, please just extract time):'
        content = content + ngrams.raw_text()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip()
        if output == 'True':
            vars['CHECK'] = True
            vars['ANTICHECK'] = False
        else:
            vars['CHECK'] = False
            vars['ANTICHECK'] = True

        return True

class MacroColor(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        model = 'gpt-3.5-turbo'
        content = 'The user wants to make appointment for a hair coloring, I asked the user \'What date and time are you ' \
                  'looking for?\' hair coloring is only available on Wednesday 10 AM, 11 AM, 1 PM and Thursday at 10 AM and 11 AM, ' \
                  'based on the following response from user, return True if the user a valid time, False if ' \
                  'otherwise, (the user may type extra words other than time, please just extract time):'
        content = content + ngrams.raw_text()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip()
        if output == 'True':
            vars['CHECK'] = True
            vars['ANTICHECK'] = False
        else:
            vars['CHECK'] = False
            vars['ANTICHECK'] = True

        return True

class MacroPerm(Macro):
    def run(self, ngrams: Ngrams, vars: Dict[str, Any], args: List[Any]):
        model = 'gpt-3.5-turbo'
        content = 'The user wants to make appointment for a perm, I asked the user \'What date and time are you ' \
                  'looking for?\' Perm is only available on Friday 10 AM, 11 AM, 1 PM, 2 PM and Saturday at 10 AM, 2 PM, ' \
                  'based on the following response from user, return True if the user a valid time, False if ' \
                  'otherwise, (the user may type extra words other than time, please just extract time):'
        content = content + ngrams.raw_text()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'user', 'content': content}]
        )
        output = response['choices'][0]['message']['content'].strip()
        if output == 'True':
            vars['CHECK'] = True
            vars['ANTICHECK'] = False
        else:
            vars['CHECK'] = False
            vars['ANTICHECK'] = True

        return True


transitions = {
    'state': 'start',
    '`Hello, how can I help you?`': {
        '[{haircut, <cut, hair>}]': {
            '`Sure. What date and time are you looking for?`': {
                '#HAIRCUT': {
                    '#IF($CHECK)`Your appointment is set. See you!`': 'end',
                    '#IF($ANTICHECK)`Sorry, that time is not available for a haircut`': 'end'
                }
            }
        },
        '[{<hair, colored>, <hair, coloring>, <hair, color>, <hair, dye>}]': {
            '`Sure. What date and time are you looking for?`': {
                '#HAIRDYE': {
                    '#IF($CHECK)`Your appointment is set. See you!`': 'end',
                    '#IF($ANTICHECK)`Sorry, that time is not available for a hair coloring`': 'end'
                }
            }
        },
        '[{perm, perms}]': {
            '`Sure. What date and time are you looking for?`': {
                '#PERM': {
                    '#IF($CHECK)`Your appointment is set. See you!`': 'end',
                    '#IF($ANTICHECK)`Sorry, that time is not available for a perm`': 'end'
                }
            }
        },
        'error': {
            '`Sorry, we don\'t provide that service. `': 'start'
        }
    }
}

macros = {
    'HAIRCUT': MacroHair(),
    'HAIRDYE': MacroColor(),
    'PERM': MacroPerm()
}

df = DialogueFlow('start', end_state='end')
df.load_transitions(transitions)
df.add_macros(macros)

if __name__ == '__main__':
    df.run()
