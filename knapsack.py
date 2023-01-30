# -*- coding: utf-8 -*-
"""
knapsack.py - CS6515, Intro to Graduate Algorithms, Spring 2023

Implement a Dynamic Programming Solution to the knapsack problem.   The program will be given a
dictionary of items and an overall weight limit.  It should select the combination of items
which achieves the highest value without exceeding the weight limit.

NOTE:  Each item may be selected at most one time (non-repeating).

About the Input:

    itemsDict -- a dictionary of items, where the key is an integer 1...N (inclusive),
                 and the value is a tuple (name, weight, value) where
                    name is the text name of the item
                    weight is the item weight
                    value is the item value

    maxWt -- the maximum weight supported by the knapsack

    There is at least one item available to process
    All weights and values are >0
    All test cases will have a solution (at least one item can be inserted in the knapsack)
"""
import argparse  # argparse allows the parsing of command line arguments

import GA_ProjectUtils as util  # utility functions for cs 6515 projects


def initTable(numItems, maxWt):
    """
    Initialize the table to be used to record the best value possible for given
    item idx and weight
    NOTE : this table must:
                      -- be 2 dimensional (i.e. T[x][y])
                      -- contain a single numeric value (no tuples or other complicated abstract data types)
    """
    # TODO Replace the following with your code to initialize the table properly

    T = [[0 for _ in range(maxWt + 1)] for _ in range(numItems + 1)]
    return T


def buildItemIterable(numItems):
    """
    Build item iterable to iterate through all available items
            numItems : number of items

    Note: the index (key value) for items are integer values 1..N inclusive
    """
    # TODO Replace the following with your code to build the item iterable

    return range(1, numItems + 1)


def buildWeightIterable(maxWt):
    """
    Build weight iterable to interate through all possible integer weight values
            maxWt : maximum weight available
    """
    # TODO Replace the following with your code to build the weight iterable

    return range(1, maxWt + 1)


def subProblem(T, weight, itemIDX, itemWt, itemVal):
    """
    Define the subproblem to solve for each table entry - set the value to be maximum for a given
    item and weight value
            T : the table being populated
            weight : weight from iteration through possible weight values
            itemIDX : the index (key value) of the item from the loop iteration
            itemWt : the weight of the item
            itemVal : the value of the item
    """
    # TODO Replace the following with your code to solve the subproblem appropriately!
    if itemWt <= weight:
        return max(T[itemIDX - 1][weight - itemWt] + itemVal, T[itemIDX - 1][weight])
    else:
        return T[itemIDX - 1][weight]


def buildResultList(T, itemsDict, maxWt):
    """
    Construct list of items that have been selected.
            T : the populated table of subproblems, indexed by item idx and weight
            itemsDict : dictionary of items   Note: items are indexed 1..N
            maxWt : maximum weight allowed

            result: a list composed of item tuples
    """
    result = []

    # TODO Your code goes here to build the list of chosen items!
    n = len(itemsDict)
    total_val = T[n][maxWt]

    w = maxWt
    for i in range(n, 0, -1):
        if total_val <= 0:
            break
        if total_val == T[i - 1][w]:
            continue
        else:
            _, weight, val = itemsDict[i]
            total_val = total_val - val
            w = w - weight
            result.append(itemsDict[i])

    return result


######## Do not modify any of the lines below #######


def knapsack(itemsDict, maxWt):
    """
    Solve the knapsack problem for the passed list of items and max allowable weight
    DO NOT MODIFY THE FOLLOWING FUNCTION
    NOTE : There are many ways to solve this problem.  You are to solve it
                    using a 2D table, by filling in the function templates above.
                    If not directed, do not modify the given code template.
    """
    numItems = len(itemsDict)
    # initialize table properly
    table = initTable(numItems, maxWt)
    # build iterables
    # item iterable
    itemIterable = buildItemIterable(numItems)
    # weight iterable
    weightIterable = buildWeightIterable(maxWt)

    for itmIdx in itemIterable:
        # query item values from list
        item, itemWt, itemVal = itemsDict[itmIdx]
        for w in weightIterable:
            # expand table values by solving subproblem
            table[itmIdx][w] = subProblem(table, w, itmIdx, itemWt, itemVal)

    # build list of results - chosen items to maximize value for a given weight
    return buildResultList(table, itemsDict, maxWt)


def main():
    """
    The main function
    """
    # DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    # You may change default values, but any values you set will be overridden when autograded
    parser = argparse.ArgumentParser(description="Knapsack Coding Quiz")
    parser.add_argument(
        "-i",
        "--items",
        help="File holding list of possible Items (name, wt, value)",
        default="defaultItems.txt",
        dest="itemsListFileName",
    )
    parser.add_argument(
        "-w",
        "--weight",
        help="Maximum (integer) weight of items allowed",
        type=int,
        default=400,
        dest="maxWeight",
    )

    # args for autograder, DO NOT MODIFY ANY OF THESE
    parser.add_argument(
        "-a",
        "--autograde",
        help="Autograder-called (2) or not (1=default)",
        type=int,
        choices=[1, 2],
        default=1,
        dest="autograde",
    )
    args = parser.parse_args()

    # DO NOT MODIFY ANY OF THE FOLLOWING CODE
    itemsDict = util.buildKnapsackItemsDict(args)
    itemsChosen = knapsack(itemsDict, args.maxWeight)
    util.displayKnapSack(args, itemsChosen)


if __name__ == "__main__":
    main()
