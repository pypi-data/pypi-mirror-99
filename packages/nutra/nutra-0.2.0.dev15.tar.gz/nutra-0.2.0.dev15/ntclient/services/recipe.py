#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:14:00 2020

@author: shane
"""

from tabulate import tabulate

from ..persistence.sql.nt.funcs import (
    analyze_recipe,
    recipes as _recipes,
    recipe as _recipe_overview,
)
from ..persistence.sql.usda.funcs import analyze_foods, nutrients_overview, food_details
from ..utils.nutprogbar import print_nutprogbar


def recipes_overview():
    recipes = _recipes()[1]

    results = []
    for recipe in recipes:
        result = {
            "id": recipe[0],
            "name": recipe[1],
            "n_foods": recipe[2],
            "weight": recipe[3],
            # "guid": recipe[4],
            # "created": recipe[5],
        }
        results.append(result)

    table = tabulate(results, headers="keys", tablefmt="presto")
    print(table)
    return results


def recipe_overview(id):

    recipe = analyze_recipe(id)

    try:
        name = recipe[0][1]
    except Exception as e:
        print(repr(e))
        return None

    print(name)

    food_ids = {x[2]: x[3] for x in recipe}
    food_names = {x[0]: x[3] for x in food_details(food_ids.keys())}
    food_analyses = analyze_foods(food_ids.keys())

    table = tabulate(
        [[food_names[id], grams] for id, grams in food_ids.items()],
        headers=["food", "g"],
    )
    print(table)
    # tabulate nutrient RDA %s
    nutrients = nutrients_overview()
    # rdas = {x[0]: x[1] for x in nutrients.values()}
    print_nutprogbar(food_ids, food_analyses, nutrients)

    return recipe


def recipe_add(name, food_amts):
    print()
    print("New recipe: " + name + "\n")

    food_names = {x[0]: x[2] for x in food_details(food_amts.keys())}

    results = []
    for id, grams in food_amts.items():
        results.append([id, food_names[id], grams])

    table = tabulate(results, headers=["id", "food_name", "grams"], tablefmt="presto")
    print(table)

    confirm = input("\nCreate recipe? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")


def recipe_edit(id):

    recipe = _recipe_overview(id)

    print(recipe[1])
    confirm = input("Do you wish to edit? [Y/n] ")

    if confirm.lower() == "y":
        print("not implemented ;]")
