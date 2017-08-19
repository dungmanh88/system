omelet_ingredients = {"egg":2, "mushroom":5, "pepper":1, "cheese":1, "milk":1}
fridge_contents={"egg":50, "mushroom":60, "pepper":10, "cheese":30, "milk":200}
omelet_orders=100
omelet_deliverd=0

while omelet_deliverd < omelet_orders:
    break_out=False
    for ingredient in omelet_ingredients.keys():
        ingredient_needed = omelet_ingredients[ingredient]
        print "Adding %d %s into mix" % (ingredient_needed, ingredient)
        fridge_contents[ingredient] = fridge_contents[ingredient]-ingredient_needed
        if fridge_contents[ingredient] < ingredient_needed:
            print "There is not enough ingredient %s for another omelet" % ingredient
            break_out = True
    omelet_deliverd = omelet_deliverd + 1
    print "One more made omelet is deliveried"
    if break_out:
        print "Out of ingredient. Go shopping now"
        break
