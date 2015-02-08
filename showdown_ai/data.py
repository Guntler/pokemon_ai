import json
from smogon import Smogon
from move_list import moves as MOVES
MOVE_CORRECTIONS = {"ExtremeSpeed": "Extreme Speed",
                    "ThunderPunch": "Thunder Punch",
                    "SolarBeam": "Solar Beam",
                    "DynamicPunch": "Dynamic Punch"}

NAME_CORRECTIONS = {"Keldeo-Resolute": "Keldeo",
                    "Pikachu-Belle": "Pikachu",
                    "Pikachu-Cosplay": "Pikachu",
                    "Pikachu-Libre": "Pikachu",
                    "Pikachu-PhD": "Pikachu",
                    "Pikachu-Pop-Star": "Pikachu",
                    "Pikachu-Rock-Star": "Pikachu",
                    "Meowstic": "Meowstic-M",
                    "Gourgeist-*": "Gourgeist"}

class PokeData(object):
    def __init__(self, smogon_data, smogon_bw_data, graph, graph_poke, move_list, poke_moves):
        self.smogon_data = smogon_data
        self.smogon_bw_data = smogon_bw_data
        self.graph = graph
        self.graph_poke = graph_poke
        self.move_list = move_list
        self.poke_moves = poke_moves


def correct_mega(poke):
    if poke == "Charizard-Mega-X" or poke == "Charizard-Mega-Y":
        poke = "Charizard"
    if poke[-5:] == "-Mega":
        poke = poke[:-5]
    return poke

def get_move(move):
    return MOVES[move]

def correct_name(poke):
    if poke in NAME_CORRECTIONS:
        return NAME_CORRECTIONS[poke]
    return poke

def get_hidden_power(poke, data):
    movesets = data[poke].movesets
    hidden_power = None
    for moveset in movesets:
        for move in moveset['moves']:
            if "Hidden Power" in move:
                hidden_power = move
                break
        if hidden_power:
            break
    return hidden_power

def load_data(data_dir):
    with open("%s/graph_poke.json" % data_dir) as fp:
        graph_poke = json.loads(fp.read())
    with open("%s/poke2.json" % data_dir) as fp:
        data = json.loads(fp.read())
        data = Smogon.convert_to_dict(data)
    with open("%s/poke_bw.json" % data_dir) as fp:
        bw_data = json.loads(fp.read())
        bw_data = Smogon.convert_to_dict(bw_data)
    with open("%s/poke_moves.json" % data_dir) as fp:
        poke_moves = json.loads(fp.read())

    poke_list = graph_poke['frequencies'].keys()
    for poke in poke_list:
        if poke != "Meowstic":
            poke = correct_name(poke)
        if poke not in data:
            continue
        hidden_power = get_hidden_power(poke, data)

        if "Hidden Power" in graph_poke['frequencies'][poke]:
            if hidden_power:
                old_value = graph_poke['frequencies'][poke]['Hidden Power']
                graph_poke['frequencies'][poke][hidden_power] = old_value
            del graph_poke['frequencies'][poke]['Hidden Power']

        if "Hidden Power" in graph_poke['cooccurences'][poke]:
            if hidden_power:
                old_value = graph_poke['cooccurences'][poke]['Hidden Power']
                graph_poke['cooccurences'][poke][hidden_power] = old_value
            del graph_poke['cooccurences'][poke]['Hidden Power']

        for move,moves in graph_poke['cooccurences'][poke].items():
            if "Hidden Power" in moves:
                if hidden_power:
                    old_value = graph_poke['cooccurences'][poke][move]['Hidden Power']
                    graph_poke['cooccurences'][poke][move][hidden_power] = old_value
                del graph_poke['cooccurences'][poke][move]['Hidden Power']
    return PokeData(data, bw_data, None, graph_poke, MOVES, poke_moves)

