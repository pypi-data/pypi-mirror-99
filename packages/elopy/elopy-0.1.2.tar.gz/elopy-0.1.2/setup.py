# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elopy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'elopy',
    'version': '0.1.2',
    'description': 'A package to simplify Elo calculations',
    'long_description': "# Elopy\n\nThis is a module to allow you to maintain state for teams as you progress them\nthrough games played against opponents. This uses the the constants set out\nfrom [538's NBA Elo](https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/). But\nyou could inherit and overload the functions to work for any sport you wanted.\n\nCode Examples:\n\n```\nfrom elopy.elo import Elo\n\nteam_a = Elo(start_elo=1600, k=20, hca = 100)\nteam_b = Elo(start_elo=1400, k=20, hca = 100)\n\n#To get the win probability of team_a beating team_b at home\n\nteam_a_probs = team_a.win_probs(team_b, is_home=True)\n\n#To get the win probability of team_b beating team_a at home\n\nteam_b_probs = team_b.win_probs(team_a, is_home=True)\n\n#If you want to get away probabilities then set is_home to False\n\n#To get the point spread of team_a vs. team_b. Positive represents an underdog\n#negative represents a favorite\n\n#at home\npoint_spread_home = team_a.point_spread(team_b, is_home=True)\n\n#not at home. Will return a value\npoint_spread_away = team_a.point_spread(team_b, is_home=False)\n\n#update elo's after a team has played the other. Let's say team a beat team b\n#by 15 points as a visitor\n\nteam_a.play_game(team_b, 15, is_home=False)\n\n#This will update both team a and team b's Elo ratings. If you run the same line\nas above again it will be as if both teams are playing a second game\n\nteam_a.play_game(team_b, 15, is_home=False)\n\n#This means that team a played team b again and beat them by 15 points again as\nthe visitor\n\n\n",
    'author': 'Matt Barlowe',
    'author_email': 'mcbarlowe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcbarlowe/elopy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
