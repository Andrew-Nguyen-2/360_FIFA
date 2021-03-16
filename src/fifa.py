"""
Project 4 Python - FIFA World Cup
   @author: Andrew Nguyen
   @version: 11.16.20
"""
from operator import itemgetter


def process(matches):
    points = {}
    goal_difference = {}
    group = ''
    goals = get_data(matches)[0]
    wins = get_data(matches)[1]
    losses = get_data(matches)[2]
    games = get_data(matches)[3]
    ties = get_data(matches)[4]
    goal_against = get_data(matches)[5]

    for key in goals:
        if goals[key] == 999999:
            group = key

    for key in wins:
        if key not in points:
            points[key] = wins[key] * 3

    for key in ties:
        if key not in points:
            points[key] = ties[key]
        else:
            points[key] += ties[key]

    for key in goals:
        if goals[key] != 999999:
            goal_difference[key] = goals[key] - goal_against[key]

    tmp = []
    for key in points:
        x = (points[key], wins[key], goal_difference[key], goals[key], games[key], key)
        tmp.append(x)

    tmp_sorted = multisort(list(tmp), ((0, True), (1, True), (2, True), (3, True), (4, True), (5, False)))

    out = [group]

    for i in range(len(tmp_sorted)):
        key = tmp_sorted[i][5]
        team = "{}) {} {}p, {}g ({}-{}-{}), {}gd ({}-{})".format(i+1, key, points[key], games[key], wins[key],
                                                                 ties[key], losses[key], goal_difference[key],
                                                                 goals[key], goal_against[key])
        out.append(team)

    return tuple(out)


def multisort(xs, specs):
    for key, reverse in reversed(specs):
        xs.sort(key=itemgetter(key), reverse=reverse)
    return xs


def get_data(matches):
    goals = {}
    wins = {}
    losses = {}
    games = {}
    ties = {}
    goal_scored_against = {}

    for i in range(len(matches)):
        data = matches[i]
        if i == 0:
            goals[data] = 999999
        else:
            tmp = data.split('@')
            one = tmp[0].split('#')
            two = tmp[1].split('#')
            team1 = one[0]
            team1_goal = int(one[1])
            team2 = two[1]
            team2_goal = int(two[0])

            if team1 in goals:
                goals[team1] += team1_goal
            else:
                goals[team1] = team1_goal
            if team2 in goals:
                goals[team2] += team2_goal
            else:
                goals[team2] = team2_goal

            if team1 in goal_scored_against:
                goal_scored_against[team1] += team2_goal
            else:
                goal_scored_against[team1] = team2_goal
            if team2 in goal_scored_against:
                goal_scored_against[team2] += team1_goal
            else:
                goal_scored_against[team2] = team1_goal

            if team1 in games:
                games[team1] += 1
            else:
                games[team1] = 1
            if team2 in games:
                games[team2] += 1
            else:
                games[team2] = 1

            if team1_goal > team2_goal:
                if team1 in wins:
                    wins[team1] += 1
                else:
                    wins[team1] = 1
                if team2 in losses:
                    losses[team2] += 1
                else:
                    losses[team2] = 1
                if team2 not in wins:
                    wins[team2] = 0
                if team1 not in ties:
                    ties[team1] = 0
                if team2 not in ties:
                    ties[team2] = 0
                if team1 not in losses:
                    losses[team1] = 0
            elif team1_goal < team2_goal:
                if team2 in wins:
                    wins[team2] += 1
                else:
                    wins[team2] = 1
                if team1 in losses:
                    losses[team1] += 1
                else:
                    losses[team1] = 1
                if team1 not in wins:
                    wins[team1] = 0
                if team1 not in ties:
                    ties[team1] = 0
                if team2 not in ties:
                    ties[team2] = 0
                if team2 not in losses:
                    losses[team2] = 0
            else:
                if team1 in ties:
                    ties[team1] += 1
                else:
                    ties[team1] = 1
                if team2 in ties:
                    ties[team2] += 1
                else:
                    ties[team2] = 1
                if team1 not in wins:
                    wins[team1] = 0
                if team2 not in wins:
                    wins[team2] = 0
                if team1 not in losses:
                    losses[team1] = 0
                if team2 not in losses:
                    losses[team2] = 0

    return goals, wins, losses, games, ties, goal_scored_against
