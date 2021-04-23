from os import environ


SESSION_CONFIGS = [
    dict(
        name='goNoGo',
        app_sequence=['goNoGo'],
        num_demo_participants=1,
    ),
    dict(name='doubleAuction', app_sequence=['doubleAuction'], num_demo_participants=4),
    dict(name='dollar_auction', app_sequence=['auction'], num_demo_participants=3),
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods', 'payment_info'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='guess_two_thirds',
    #     display_name="Guess 2/3 of the Average",
    #     app_sequence=['guess_two_thirds', 'payment_info'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    # ),
    dict(
        name='UrnGoods',
        num_demo_participants=5,
        app_sequence=['urngoodsSolo'],
        # app_sequence=['urngoodsSolo','urngoodsGroup']
    )
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=.008, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '1708417278112'

INSTALLED_APPS = ['otree']
PARTICIPANT_FIELDS = ['URN', 'urnDraws', 'contentsChanged', 'reaction_times']