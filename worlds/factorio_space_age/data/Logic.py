import itertools, typing
from collections import Counter
from enum import StrEnum

ALWAYS = "(always)"
NEVER = "(never)"

class LogicOption(StrEnum):
    bypass_technology_prerequisites = "bypass_technology_prerequisites"
    burner_mining_drill_is_good_enough = "burner_mining_drill_is_good_enough"
    inserter_balancing_is_good_enough = "inserter_balancing_is_good_enough"
    water_barrel_is_good_enough = "water_barrel_is_good_enough"
    launching_metal_is_good_enough = "launching_metal_is_good_enough"
    backwards_recycling_is_interesting = "backwards_recycling_is_interesting"
    unbarreling_is_interesting = "unbarreling_is_interesting"
    walls_to_destroy_medium_asteroids_is_good_enough = "walls_to_destroy_medium_asteroids_is_good_enough"
    wait_hours_for_fish_to_spoil = "wait_hours_for_fish_to_spoil"
    lightning_schmightning = "lightning_schmightning"
    solar_panels_into_darkness = "solar_panels_into_darkness"
    slow_inserter_is_good_enough = "slow_inserter_is_good_enough"
    assembling_machine_1_is_good_enough = "assembling_machine_1_is_good_enough"
    direct_pipes_is_good_enough = "direct_pipes_is_good_enough"
    hand_building_is_good_enough = "hand_building_is_good_enough"
    belt_logistics_is_good_enough = "belt_logistics_is_good_enough"
    basic_asteroid_processing_is_good_enough = "basic_asteroid_processing_is_good_enough"
    nuclear_heating_is_good_enough = "nuclear_heating_is_good_enough"

    energy_link_recipe_early_game = "energy_link_recipe_early_game"
    energy_link_recipe_mid_game = "energy_link_recipe_mid_game"
    energy_link_recipe_fulgora = "energy_link_recipe_fulgora"
    energy_link_unlocked_from_the_start = "energy_link_unlocked_from_the_start"
    playing_without_energy_link_early_game_is_good_enough = "playing_without_energy_link_early_game_is_good_enough"
    playing_without_energy_link_mid_game_is_good_enough = "playing_without_energy_link_mid_game_is_good_enough"
    playing_without_energy_link_fulgora_is_good_enough = "playing_without_energy_link_fulgora_is_good_enough"
fmt_option = lambda option: "Option {}".format(option.value)

energy_link_bridge_recipes = {
    LogicOption.energy_link_recipe_early_game: [
        dict(type="item", amount=50, name="iron-plate"),
        dict(type="item", amount=50, name="copper-plate"),
    ],
    LogicOption.energy_link_recipe_mid_game: [
        dict(type="item", amount=1, name="accumulator"),
        dict(type="item", amount=1, name="radar"),
    ],
    LogicOption.energy_link_recipe_fulgora: [
        dict(type="item", amount=10, name="supercapacitor"),
        dict(type="item", amount=1,  name="radar"),
    ],
}


def instantiate_options(raw_logic_events, never_inline_events: set[str], never_delete_events: set[str], options_dict: dict[LogicOption, bool]):
    assert set(LogicOption) == options_dict.keys(), repr(set(LogicOption) - options_dict.keys())
    logic_events = {**raw_logic_events, **{
        fmt_option(option): ALWAYS if value else NEVER
        for option, value in options_dict.items()
    }}
    logic_events, _ = inline_exprs(logic_events, never_inline_events, never_delete_events)
    return logic_events

def inline_exprs(logic_events, never_inline_events, never_delete_events):
    def visit_readonly(expr, fn):
        if type(expr) != dict:
            fn(expr)
            return
        assert expr.keys() in ({"and"}, {"or"})
        for clause in expr[next(iter(expr.keys()))]:
            visit_readonly(clause, fn)
    def visit_replace(expr, fn):
        if type(expr) != dict: return fn(expr)
        assert expr.keys() in ({"and"}, {"or"})
        key = next(iter(expr.keys()))
        new_clauses = []
        for clause in expr[key]:
            new_clauses.append(visit_replace(clause, fn))
        return {key: new_clauses}

    while True:
        # Prune unused expressions.
        all_used_names = set()
        for expr in logic_events.values():
            visit_readonly(expr, all_used_names.add)
        unreachable_events = all_used_names - logic_events.keys() - {ALWAYS, NEVER}
        if len(unreachable_events) > 0:
            # e.g. 'Automate infinity-chest', 'Access pistol'
            logic_events = dict(
                **{event_name: NEVER for event_name in unreachable_events},
                **logic_events,
            )

        unused_events = logic_events.keys() - all_used_names - never_delete_events
        logic_events = {k: v for k, v in logic_events.items() if k not in unused_events}
        did_anything = len(unused_events) > 0

        # Inline trivial events.
        inline_these = {}
        for event_name, expr in logic_events.items():
            if event_name in never_inline_events: continue
            if type(expr) == dict: continue # too complex
            # Simple enough to inline.
            inline_these[event_name] = expr
        new_logic_events = {}
        for event_name, expr in logic_events.items():
            new_expr = visit_replace(expr, lambda expr: inline_these.get(expr, expr))
            if new_expr != expr:
                new_expr = optimize_expr(new_expr)
                did_anything = True
            new_logic_events[event_name] = new_expr
        logic_events = new_logic_events

        if not did_anything: break

    return logic_events, all_used_names

def optimize_expr(expr):
    def recurse(expr):
        if type(expr) != dict: return expr
        if "or" in expr:
            clauses = expr["or"]
            if len(clauses) == 0: return NEVER
            if len(clauses) == 1: return recurse(clauses[0])
            new_clauses = []
            for clause in clauses:
                clause = recurse(clause)
                if clause == NEVER: continue # A or False == A
                if clause == ALWAYS: return ALWAYS # A or True == True
                if clause in new_clauses: continue # A or A == A
                if type(clause) == dict and "and" in clause:
                    # A or (A and B) == A
                    if any(sub_clause in new_clauses for sub_clause in clause["and"]): continue
                if type(clause) == dict and "or" in clause:
                    # A or (B or C) == A or B or C
                    new_clauses.extend(clause["or"])
                else:
                    new_clauses.append(clause)
            # (A and B) or (A and C) == A and (B or C)
            counter = Counter(itertools.chain.from_iterable(
                set(sub_clause for sub_clause in sub_expr["and"] if type(sub_clause) == str)
                for sub_expr in new_clauses if type(sub_expr) == dict and "and" in sub_expr
            ))
            omnipresent_sub_clauses = set(sub_clause for sub_clause, count in counter.items() if count == len(new_clauses))
            if len(omnipresent_sub_clauses) > 0:
                return {"and": [
                    *omnipresent_sub_clauses,
                    {"or": [
                        {"and": [
                            sub_clause for sub_clause in clause["and"]
                            if not (type(sub_clause) == str and sub_clause in omnipresent_sub_clauses)
                        ]} for clause in new_clauses
                    ]},
                ]}
            elif any(value >= 2 for value in counter.values()):
                # Not omnipresent, but popular.
                # (A and X) or (B and X) or (J and K) == (X and (A or B)) or (J and K)
                # (access product AND operater recycler) OR (access another product AND operate recycler) OR (just craft the thing)
                popular_sub_clause = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
                clauses_with = []
                clauses_without = []
                for sub_expr in new_clauses:
                    if type(sub_expr) == dict and "and" in sub_expr and popular_sub_clause in sub_expr["and"]:
                        clauses_with.append(sub_expr)
                    else:
                        clauses_without.append(sub_expr)
                return {"or": [
                    *clauses_without, # e.g. craft the thing normally
                    {"and": [
                        popular_sub_clause, # e.g. operate recycler
                        {"or": [
                            {"and": [
                                sub_clause for sub_clause in sub_expr["and"]
                                if sub_clause != popular_sub_clause
                            ]} for sub_expr in clauses_with
                        ]},
                    ]},
                ]}
            return {"or": new_clauses}

        elif "and" in expr:
            clauses = expr["and"]
            if len(clauses) == 0: return ALWAYS
            if len(clauses) == 1: return recurse(clauses[0])
            new_clauses = []
            for clause in clauses:
                clause = recurse(clause)
                if clause == ALWAYS: continue # A and True == A
                if clause == NEVER: return NEVER # A and False == False
                if clause in new_clauses: continue # A and A == A
                if type(clause) == dict and "or" in clause:
                    # A and (A or B) == A
                    if any(sub_clause in new_clauses for sub_clause in clause["or"]): continue
                if type(clause) == dict and "and" in clause:
                    # A and (B and C) == A and B and C
                    new_clauses.extend(clause["and"])
                else:
                    new_clauses.append(clause)

            # (A or B) and (A or C) == A or (B and C)
            counter = Counter(itertools.chain.from_iterable(
                set(sub_clause for sub_clause in sub_expr["or"] if type(sub_clause) == str)
                for sub_expr in new_clauses if type(sub_expr) == dict and "or" in sub_expr
            ))
            omnipresent_sub_clauses = set(sub_clause for sub_clause, count in counter.items() if count == len(new_clauses))
            if len(omnipresent_sub_clauses) > 0:
                return {"or": [
                    *omnipresent_sub_clauses,
                    {"and": [
                        {"or": [
                            sub_clause for sub_clause in clause["or"]
                            if not (type(sub_clause) == str and sub_clause in omnipresent_sub_clauses)
                        ]} for clause in new_clauses
                    ]},
                ]}
            return {"and": new_clauses}

        else: assert False
        return expr

    import json
    original_expr = json.dumps(expr,sort_keys=True,separators=(',', ':'))
    while True:
        expr = recurse(expr)
        new_expr = json.dumps(expr,sort_keys=True,separators=(',', ':'))
        if original_expr == new_expr: break
        original_expr = new_expr

    def sorted_recursive(expr):
        if type(expr) != dict: return expr
        expr = {k: (sorted_recursive(x) for x in v) for k, v in expr.items()}
        expr = {k: sorted(v, key=json.dumps) for k, v in expr.items()}
        return expr
    return sorted_recursive(expr)

def compile_expr(expr) -> typing.Callable[[dict[str, int]], bool]:
    INTERPRETED = False # Change this to debug I guess.
    if INTERPRETED:
        def access_rule_fn(d):
            def recurse(expr):
                if expr == ALWAYS: return True
                if expr == NEVER: return False
                if type(expr) != dict: return d[expr] > 0
                if "or" in expr:
                    for clause in expr["or"]:
                        if recurse(clause):
                            return True
                    return False
                elif "and" in expr:
                    for clause in expr["and"]:
                        if not recurse(clause):
                            return False
                    return True
                else: assert False
            return recurse(expr)
        return access_rule_fn
    else:
        def recurse(expr):
            if expr == ALWAYS: return "True"
            if expr == NEVER: return "False"
            if type(expr) != dict: return "d[{}]".format(repr(expr))
            if "or" in expr:
                return "({})".format(" or ".join(recurse(clause) for clause in expr["or"]))
            elif "and" in expr:
                return "({})".format(" and ".join(recurse(clause) for clause in expr["and"]))
            else: assert False
        code = recurse(expr)
        fn = eval("lambda d: " + code)
        return fn

if __name__ == "__main__":
    # Some tests
    assert optimize_expr({"or": [
        "Reach gleba",
        {"and": ["Access agricultural-tower", "Access jellynut-seed", "Reach gleba"]}
    ]}) == "Reach gleba"
