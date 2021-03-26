from otree.api import *

c = Currency
doc = """
start application with 'otree devserver'
go to internet and click on 'http://localhost:8000'
"""


class Constants(BaseConstants):
    name_in_url = 'UrnGoods'
    instructions_template = 'urngoodsSolo/PayoutInfo.html'
    players_per_group = None
    num_rounds = 5
    endowment = c(40)

    numberOfDraws = 40
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    game_finished = models.BooleanField()


def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        participant = p.participant
        participant.URN = ['blue' for _ in range(50)] + ['red' for _ in range(50)]
        participant.UrnChanges = 0

class Player(BasePlayer):
#Information every player needs durin drawing
    drawsLeft = models.IntegerField(
        initial=Constants.numberOfDraws
    )
    currentDraw = models.IntegerField(initial=0)

#Information Needed in the Guessin Portion of game
    willGuess = models.BooleanField(
        initial=False,
        label='Would you like to guess or draw?',
        widget=widgets.RadioSelect,
        choices=[[True,'Guess'],[False, 'Draw']]
    )

#Infoomation Downward is for the survey
    age = models.IntegerField(
        label='What is your Age?'
    )
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female']],
        label='What is your gender?'
    )
    genderIdentity = models.StringField(
        choices=[['Male','Male'],['Female','Female'],['Non-Binary','Non-Binary'],['Prefer Not to Disclose','Prefer not to disclose']],
        label='What is your gender identity?',
        widget=widgets.RadioSelect
    )
    originCountry = models.StringField(
        label='In what country were you born?'
    )
    isLatino = models.BooleanField(
        label='Are you Hispanic, Latino, or of Spanish Origin?',
        widget=widgets.RadioSelect,
        choices=[[True,'Yes'],[False, 'No']]
    )
    race = models.StringField(
        choices=[['American Indian/Alaskan Native','American Indian/Alaskan Native'],
                ['Asian','Asian'],
                ['Black/African-American','Black/African-American'],
                ['Native Hawaiian/Pacific Islander','Native Hawaiian/Pacific Islander'],
                ['White/Caucasian','White/Caucasian'],
                ['Multi-Racial','Multi-Racial'],
                ['Other','Other']
        ],
        label="How would you describe yourself?",
    )
    classification = models.StringField(
        choices=[['First-Year','First-Year'],['Sophomore','Sophomore'],['Junior','Junior'],['Senior','Senior']],
        label='What is your gender identity?',
        widget=widgets.RadioSelect
    )
    major = models.StringField(
        choices=[['Economics','Economics'],
                ['Math','Math'],
                ['Psychology','Psychology'],
                ['Humanities','Humanities'],
                ['Arts','Arts'],
                ['Undecided','Undecided'],
                ['Other Science','Other Science'],
                ['Other Social Sciences','Other Social Sciences'],
                ['Other','Other']
        ],
        label="How would you describe yourself?",
    )
    econCoursesTaken = models.IntegerField(
        label='How many Economics Courses have you taken?'
    )
    groupDecisions = models.LongStringField(
        label='How did your group make decisions?'
    )
    knownParticipants = models.IntegerField(
        label='How many of the other participants did you know?'
    )

def set_payoffs(group):
    pass
    # players = group.get_players()
    # contributions = [players.pim
    # group.total_contribution = sum(contributions)
    # group.individual_share = group.total_contribution * Constants.multiplier / Constants.players_per_group
    # for player in players:
    #     player.payoff = Constants.endowment + group.individual_share

#Pages
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Instructions(Page):

#We only want to show the instructions if its our first round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class PracticeRound(Page):
    #the life met hod shoud chage contents of URn
    form_model = ['player']
    @staticmethod
    def live_method(player: Player, data):
        print(data)
        if data == 'true':
            print('we in here')
            player.willGuess = True
            player.group.game_finished = True
            response = dict(ID=player.id_in_group, draws=player.drawsLeft, guess=True)
            return {player.id_in_group: response}
        else:

            player.drawsLeft -= 1
            print(player.drawsLeft)
            player.group.game_finished = False
            response = dict(ID=player.id_in_group, draws=player.drawsLeft, guess=False)
            return {player.id_in_group: response}
    
    def js_vars(player:Player):
        return dict(my_id=player.id_in_group,myDraws=player.drawsLeft, guess=player.willGuess)


def changeUrnContents(player: Player):
    """Given a Partiipcant, retrieve their URN, change the contents, and return the new URN"""
    urn = participant.URN

class PracticeGuess(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.willGuess or not player.drawsLeft)

    @staticmethod
    def live_method(player: Player, data):
        pass


class Survey(Page):

    #only show this page if we are at the final round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds
    form_model = 'player'
    form_fields = ['age',
                'genderIdentity',
                'originCountry',
                'isLatino',
                'race',
                'classification',
                'major',
                'econCoursesTaken',
                'groupDecisions',
                'knownParticipants']

class Results(Page):
    pass


page_sequence = [
    Introduction,
    Instructions,
    PracticeRound,
    PracticeGuess,
    Survey
]
