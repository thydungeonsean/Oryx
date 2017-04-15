from random import *


class NameGenerator(object):

    vowels = ('a', 'e', 'i', 'o', 'u')
    rare_vowels = ('y',)
    consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 'sh', 't', 'th', 'v', 'w', 'ch')
    rare_consonants = ('qu', 'zh', 'x')

    end_consonants = ('ck', 'dd', 'gh', 'ng', 'h', 'k', 'c', 'l', 'll', 'm', 'n', 'mn', 'g', 'ph', 'p', 'r', 's', 'ss',
                      'sh', 't', 'tt', 'th', 'v', 'w', 'x', 'ch', 'rn')
    compounds = ('ck', 'dd', 'gh', 'ng', 'll', 'mn', 'ph', 'ss', 'sh', 'tt', 'th', 'ch', 'rn')

    sibilants = ['s', 'sh', 'th']
    nasals = ['m', 'n']
    fricatives = ['f', 'v']
    liquids = ['l', 'r']

    glottal_transition = sibilants + nasals + fricatives + liquids
    liquid_transition = liquids + nasals
    nasal_transition = sibilants + nasals

    consonant_transitions = {
        'ck': glottal_transition,
        'gh': liquids,
        'h': consonants,
        'k': glottal_transition,
        'c': glottal_transition,
        'l': liquid_transition,
        'm': nasal_transition,
        'n': nasal_transition,
        'g': glottal_transition,
        'ph': nasals,
        'p': glottal_transition,
        'r': liquid_transition,
        's': nasals,
        'ss': nasals,
        't': glottal_transition,
        'th': nasals,
        'v': nasals,
        'ch': glottal_transition,
        'mn': '*',
        'ng': '*',
        'rn': '*'
    }

    premade_endings = (
        'or', 'ar', 'ur', 'ir', 'oth', 'ith', 'eth', 'ad', 'id', 'er', 'orn'
    )

    def __init__(self, sd):

        # TODO initializing a namegenerator grabs a subset of letters that will be preferred for use with generation
        self.seed = sd
        seed(sd)

        self.rare = self.set_rare()
        self.vowel_start = randint(20, 40)

    def set_rare(self):
        if randint(0, 99) < 25:
            return True
        else:
            return False

    def first_syllable(self):

        ng = NameGenerator

        syllable = ''

        if randint(0, 99) < self.vowel_start:
            con = list(ng.consonants[:])
            if self.rare:
                con.extend(ng.rare_consonants)
            syllable += choice(con)

        syllable += self.basic_syllable()

        syllable = syllable.capitalize()

        return syllable

    def basic_syllable(self, end=False):

        ng = NameGenerator

        syllable = ''

        vow = ng.vowels[:]
        if self.rare:
            vow += ng.rare_vowels

        syllable += choice(vow)

        if end and randint(0, 99) < 50:
            return syllable
        syllable += choice(ng.end_consonants)

        return syllable

    def complex_join(self, name, complexity=50):

        ng = NameGenerator

        tag = self.get_tag(name)
        next = ''
        try:
            if randint(0, 99) < complexity:
                complex_consonant = ng.consonant_transitions[tag]
                if complex_consonant == '*':
                    return ''
                next += choice(complex_consonant)
        except KeyError:
            pass

        return next

    def next_syllable(self, name, end=False):

        ng = NameGenerator

        next = ''
        next += self.complex_join(name)
        if end and randint(0, 99) < 50:
            next += choice(ng.premade_endings)
        else:
            next += self.basic_syllable(end=end)

        return next

    def get_tag(self, syllable):

        ng = NameGenerator

        if syllable[-2:] in ng.compounds:
            tag = syllable[-2:]
        else:
            tag = syllable[-1]
        return tag

    def one_syllable_name(self):

        return self.first_syllable()

    def two_syllable_name(self):

        name = self.first_syllable()

        name += self.next_syllable(name, end=True)

        return name

    def three_syllable_name(self):

        name = self.first_syllable()

        name += self.next_syllable(name)
        name += self.next_syllable(name, end=True)

        return name

    def name(self):

        option = randint(0, 99)

        if option < 5:
            return self.one_syllable_name()
        elif option < 55:
            return self.two_syllable_name()
        else:
            return self.three_syllable_name()


n = NameGenerator(1)

for i in range(100):
    print n.name()
