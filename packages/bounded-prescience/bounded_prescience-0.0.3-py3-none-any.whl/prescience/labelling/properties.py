from prescience.labelling.Freeway import Hit
from prescience.labelling.Death import Death
from prescience.labelling.Assault import Overheat
from prescience.labelling.Below_Reward import Below_Reward
from prescience.labelling.Bowling import No_Hit
from prescience.labelling.Bowling import No_Strike
from prescience.labelling.DoubleDunk import Out_Of_Bounds
from prescience.labelling.DoubleDunk import Shoot_Bf_Clear
from prescience.labelling.Seaquest import Early_Surface
from prescience.labelling.Seaquest import Out_Of_Oxygen
from prescience.labelling.InstantNegativeReward import Instant_Negative_Reward
from prescience.labelling.Frostbite import Freezing
from prescience.labelling.Gravitar import Fuel
from prescience.labelling.Hero import Dynamite
from prescience.labelling.KungFuMaster import Energy_Loss

prop_map = {
    "Freeway": {
        "hit": (Hit, {})
    },
    "Assault": {
        "overheat": (Overheat, {}),
        "death": (Death, {})
    },
    "Boxing": {
        "knock-out": (Below_Reward, {'threshold': -99, 'count_pos': False}),
        "lose": (Below_Reward, {'threshold': 0}),
        "no-enemy-ko": (Below_Reward, {'threshold': 99, 'count_neg': False})
    },
    "FishingDerby": {
        "lose": (Below_Reward, {'threshold': 99, 'count_neg': False})
    },
    "BeamRider": {
        "death": (Death, {})
    },
    "Bowling": {
        "no-hit": (No_Hit, {}),
        "no-strike": (No_Strike, {})
    },
    "Frostbite": {
        "death": (Death, {}),
        "freezing": (Freezing, {})
    },
    "Berzerk": {
        "death": (Death, {})
    },
    "DoubleDunk": {
        "out-of-bounds": (Out_Of_Bounds, {}),
        "shoot-bf-clear": (Shoot_Bf_Clear, {})
    },
    "Seaquest": {
        "death": (Death, {}),
        "early-surface": (Early_Surface, {}),
        "out-of-oxygen": (Out_Of_Oxygen, {})
    },
    "Enduro": {
        "crash-car": (Instant_Negative_Reward, {})
    },
    "Alien": {
        "death": (Death, {})
    },
    "Amidar": {
        "death": (Death, {})    
    },
    "Asterix": {
        "death": (Death, {})
    },
    "Asteroids": {
        "death": (Death, {})
    },
    "Atlantis": {
        "death": (Death, {})
    },
    "BattleZone": {
        "death": (Death, {})
    },
    "Breakout": {
        "death": (Death, {})
    },
    "Centipede": {
        "death": (Death, {})
    },
    "CrazyClimber": {
        "death": (Death, {})
    }, 
    "DemonAttack": {
        "death": (Death, {})
    },
    "Gopher": {
        "lose-carrot": (Death, {})
    },
    "Gravitar": {
        "death": (Death, {}),
        "fuel": (Fuel, {})
    },
    "Jamesbond": {
        "death": (Death, {})
    },
    "IceHockey": {
        "enemy-score": (Instant_Negative_Reward, {})
    },
    "Kangaroo": {
        "death": (Death, {})
    },
    "KungFuMaster": {
        "death": (Death, {}),
        "energy-loss": (Energy_Loss, {})
    },
    "Hero": {
        "death": (Death, {}),
        "dynamite": (Dynamite, {})
    },
    "MsPacman": {
        "death": (Death, {})
    },
    "NameThisGame": {
        "death": (Death, {})
    },
    "BankHeist": {
        "death": (Death, {})
    }
}
env_endings = ["NoFrameskip-v4", "Deterministic-v4", "-v0", "-v4"]


def get_property(env, prop_string):
    env_string = env.unwrapped.spec.id
    to_call = prop_map[strip_env_string(env_string)][prop_string]
    return to_call[0](env, **to_call[1])


def strip_env_string(string):
    for suffix in env_endings:
        if string.endswith(suffix):
            return string[:-len(suffix)]
