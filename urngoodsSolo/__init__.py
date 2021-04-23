from otree.api import *
from random import choice
c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'UrnGoods'
    instructions_template = 'urngoodsSolo/PayoutInfo.html'
    players_per_group = None
    num_rounds = 5
    jackpot = 100


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        participant = p.participant
        participant.URN = ['blue' for _ in range(50)] + ['red' for _ in range(50)]
        participant.payoff = 0
        # participant.contentsChanged = False

class Group(BaseGroup):
    #information the server needs to now
    auction_timeout = models.FloatField()


def get_state(group: Group):
    return dict(
        # top_bid=group.top_bid,
        # top_bidder=group.top_bidder,
        # second_bid=group.second_bid,
        # second_bidder=group.second_bidder,
    )


class Player(BasePlayer):
#information needed for the survey
    urnDraws = models.IntegerField(initial=0)
    contentsChanged = models.BooleanField(initial=False)
    theoreticalPayoff = models.IntegerField(initial=40)
    correctGuess = models.IntegerField(
        initial=0
        # label="What Color do you believe dominates the Urn?",
        # widget=widgets.RadioSelect,
        # choice=[[0,'']]
    )
    isGuessing = models.BooleanField(initial=False)


#Information Downward is for the survey
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

class Introduction(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Instructions(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import time

        player.group.auction_timeout = time.time() + 10

# class WaitToStart(WaitPage):
#     @staticmethod
#     def after_all_players_arrive(group: Group):
#         import time

#         group.auction_timeout = time.time() + 60


# PAGES

def set_payoffs(player: Player):
    """Is called whenever a player makes a draw or guess to correctly calculate their payoff"""
    print(f"The player has a current Payoff of {player.participant.payoff}")
    print(f"The player has made {player.urnDraws} draws in the previous round.")
    print(f"The player correctly guess the composition {player.correctGuess}")
    player.participant.payoff += player.correctGuess * 60 + (40 - player.urnDraws)
    player.isGuessing = True


def calculateTheoreticalPayoff(player: Player):
    return 60 + (40 - player.urnDraws)

def change_urn_contents(player: Player):
    """ask about how the urn contents will change upon drawing"""
    """changes the urn contents depending on the turn"""
    print("THE URN CONTENTS HAVE BEEN CHANGED")
    blue = ['blue' for _ in range(70)] + ['red' for _ in range(30)]
    red = ['blue' for _ in range(30)] + ['red' for _ in range(70)]
    currentTurn = player.urnDraws
    urnChange = choice((True, False))
    if (currentTurn % 10 == 0) and not player.contentsChanged and currentTurn != 0:
        urnChange = True
    if urnChange:
        player.participant.URN = choice((blue, red))
        player.contentsChanged = True
    else:
        if currentTurn % 10 == 0 and player.contentsChanged:
            player.participant.contentsChanged = False


class PracticeRound(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return group.auction_timeout - time.time()

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        print("live method")
        print(data)
        group = player.group
        my_id = player.id_in_group
        if data:
            if data['button'] == 'guess':
                player.isGuessing = True
                return {my_id: dict(guess=player.isGuessing)}
            elif player.urnDraws < 40:
                change_urn_contents(player)
                print(player.theoreticalPayoff)
                marble = choice(player.participant.URN)
                player.urnDraws += 1
                player.theoreticalPayoff = calculateTheoreticalPayoff(player)
                return {my_id: dict(get_state(group), currentDraws=player.urnDraws, payOff=player.theoreticalPayoff, marble=marble, totalpayOff=player.participant.payoff)}
            else:
                return {my_id: dict(get_state(group), currentDraws=player.urnDraws, payOff=player.theoreticalPayoff, totalpayOff=player.participant.payoff)}
            
        else:
            return {my_id: dict(get_state(group), totalpayOff=player.participant.payoff)}

class PracticeGuess(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        if data:
            my_id = player.id_in_group
            if player.urnDraws == 0:
                change_urn_contents(player)
                player.isGuessing = True
            urn = player.participant.URN
            #first index is blue second index is red
            marbleFrequency = [urn.count(m) for m in ['blue','red']]
            if(marbleFrequency[data['button']] == max(marbleFrequency)):
                print("made it here 1")
                player.correctGuess = 1
                return {my_id: dict(guessedCorrectly=True)}
            player.correctGuess = 0
            print('made it here 2')
            return {my_id: dict(guessedCorrectly=False)}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffs(player)


class ResultsWaitPage(WaitPage):
    pass
    # @staticmethod
    # def after_all_players_arrive(group: Group):
    #     if group.top_bidder > 0:
    #         top_bidder = group.get_player_by_id(group.top_bidder)
    #         top_bidder.payoff = Constants.jackpot - group.top_bid
    #         top_bidder.is_top_bidder = True

    #     if group.second_bidder > 0:
    #         second_bidder = group.get_player_by_id(group.second_bidder)
    #         second_bidder.payoff = -group.second_bid
    #         second_bidder.is_second_bidder = True


class Survey(Page):

    # @staticmethod
    # def is_displayed(player: Player):
    #     return player.round_number == Constants.num_rounds
    @staticmethod
    def is_displayed(player):
        return player.round_number == 5

    def before_next_page(player: Player, timeout_happened):
        for player in player.subsession.get_players():
            participant = player.participant
            # print(participant.URN)
            # print(participant.urnDraws)
            # print()

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


page_sequence = [Introduction, Instructions, PracticeRound, PracticeGuess Survey]