import plotly.express as px
import pandas as pd
import csv

# Do not modify the line below.
countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Falkland Islands", "Guyana", "Paraguay",
             "Peru", "Suriname", "Uruguay", "Venezuela"]

# Do not modify the line below.
colors = ["blue", "green", "red", "yellow"]

# Write your code here
NO_NEIGHBOUR = ['NONE']


class my_dictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


dict_obj = my_dictionary()


def read_neighbors(myDictionary):
    with open("SouthAmerica.csv", "r", encoding="utf-8") as f:
        next(f)
        reader = csv.reader(f)

        for row in reader:
            country = row[0]
            neighbours = row[1:len(row)]
            myDictionary.add(country, neighbours)
    return myDictionary


def check_map(color_map, country, adjacency_dict):
    if dict_obj[country] == NO_NEIGHBOUR:
        return True
    for neighbour in dict_obj[country]:
        if color_map[neighbour] == color_map[country]:
            return False
    return True


def run_map_coloring(num_colors=4):
    color_map = dict(dict_obj)
    list_of_items = list(dict_obj.keys())
    set_of_assignments = colors[:num_colors]
    legal_assignment_func = check_map
    if general_backtracking(list_of_items, color_map, 0,
                            set_of_assignments, legal_assignment_func,
                            dict_obj):
        return color_map
    else:
        return None


def general_backtracking(list_of_items, dict_items_to_vals, index,
                         set_of_assignments, legal_assignment_func, *args):
    # recursion base case
    if all(value in set_of_assignments for value in
           dict_items_to_vals.values()):
        return True
    else:
        # going over every possible value
        for val in set_of_assignments:
            item_check = list_of_items[index]
            temp = dict_items_to_vals[item_check]
            # assigning the value
            dict_items_to_vals[item_check] = val
            if legal_assignment_func(dict_items_to_vals, item_check, args):
                # recursion in case action s legal
                if general_backtracking(list_of_items, dict_items_to_vals,
                                        index + 1, set_of_assignments,
                                        legal_assignment_func, *args):
                    return True
            # going one step back in case we have reached a dead-end
            dict_items_to_vals[item_check] = temp
        return False


# Do not modify this method, only call it with an appropriate argument.
# colormap should be a dictionary having countries as keys and colors as values.
def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names",
                        locations=countries,
                        color=countries,
                        color_discrete_sequence=[colormap[c] for c in countries],
                        scope="south america")
    fig.show()


# Implement main to call necessary functions
if __name__ == "__main__":
    # Creating dictionary
    read_neighbors(dict_obj)
    # Creating colormap
    myColormap = run_map_coloring()
    # coloring test
    colormap_test = {"Argentina": "blue", "Bolivia": "red", "Brazil": "yellow", "Chile": "yellow", "Colombia": "red",
                     "Ecuador": "yellow", "Falkland Islands": "yellow", "Guyana": "red", "Paraguay": "green",
                     "Peru": "green", "Suriname": "green", "Uruguay": "red", "Venezuela": "green"}

    # plot_choropleth(colormap=colormap_test)

print("Map checking\n", check_map(run_map_coloring(), 'Argentina', dict_obj))
print("Map coloring\n", run_map_coloring())
print("Dictionary\n", read_neighbors(dict_obj))
plot_choropleth(myColormap)
