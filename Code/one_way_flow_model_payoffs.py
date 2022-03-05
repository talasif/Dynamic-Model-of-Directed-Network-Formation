# One-Way Flow Model
import random as rd
from itertools import permutations as pm
import numpy as np
import math as mt
import copy as cp
from scipy.stats import sem

payoffs = []

# Variables:
SIZE = 100                   # options of probability
N = 3                       # Number of players   - - - Change by |N|
STOP = 0.01                 # Ratio of convergence
ROUNDS = 1000
ROUND_STOP = 2
for R in [0.01, 0.2, 0.5, 0.8]:
    for C in [0.5]:
        def my_perms(lst):
            """
            permutes all variations of all sizes
            :param lst:
            :return:
            """
            perms = []
            for i in range(len(lst) + 1):
                all_pm = pm(lst, i)
                for j in all_pm:
                    elem = list(j)
                    elem.sort()
                    if elem not in perms:
                        perms.append(elem)
            return perms


        def show_one(x_i, lst):
            """
            shows the connections a player executed
            :param x_i: name of player
            :param lst: other players he connected to
            :return: None
            """
            print(x_i, ' ---> ', lst)


        def show_all(my_lst):
            """
            Prints all players state
            :param my_lst: list of lists of connections of each player & the
            connections
            :return: None
            """
            for each1 in range(len(my_lst)):   # prints every players state
                show_one(my_lst[each1][0], my_lst[each1][1])


        def init_choice(xi, n_size):
            """
            Gives an agent a set of other agents connected to in the beginning
            of a game. The size of the set - a random number between 0 and n-1.
            :param xi: individual
            :param n_size: size of whole group (number of players)
            :return: list of agent & list of all ones connected to initially
            """
            num_of_init = rd.randint(0, n_size - 1)  # how many connections
            init_conct = []
            while len(init_conct) != num_of_init:
                chosen = rd.choice(range(1, n_size + 1))
                if chosen != xi and chosen not in init_conct:
                    init_conct.append(chosen)
            return [xi, init_conct]


        def init_all(all_of_us, num):
            """
            :param all_of_us: list of players
            :param num: number of players
            :return: list of tuples of connections
            """
            everyone = []
            for i in all_of_us:  # runs initial choice for every player
                everyone.append(init_choice(i, num))  # Change for random payoff.
                # everyone.append([i, []])            # Change for empty payoff.
            return everyone
        # Function to update for empty payoffs


        def free_will(prob=R):
            """
            chooses 1 or 0 by probability
            :param prob: probability
            :return: T or F
            """
            ops = [1]*SIZE
            for j in range(int(prob*SIZE)):
                # defines list of chances of probability
                ops[j] = 0
            return rd.choice(ops)


        def is_connected(ag1, ag2, lstag):
            """
            Logical function returning True or False if ag1 is connected to ag2
            :param ag1: agent 1 - the agent being potentially wooed
            :param ag2: agent 2 - checked if agent 1 is connected to
            :param lstag: list of agent 2
            :return: T or F
            """
            if ag2 in lstag[ag1 - 1][1]:
                return True
            else:
                return False


        def build_empty(ag, length=N):
            """
            :param ag:
            :param length: size of game
            :return: vector of binary values - 1 for ag and 0 otherwise
            """
            empty = [0]*length
            empty[ag - 1] = 1
            return empty


        def get_concts(ag, lst):
            """
            Gets agents connections
            :param ag: agent (1st degree) connected
            :param lst: everyone
            :return: list of connections of ag
            """
            go1 = find_loc(ag, lst)
            return lst[go1][1]


        def find_loc(ag, lst):
            """
            :param ag: variable (not index)
            :param lst:
            :return: index of ag in lst
            """
            where = []
            for xy in lst:
                where.append(xy[0])
            return where.index(ag)


        def one_link(link, ag, board, done):
            """
            Recursion Function
            Outputs list of ones ag has access to their information (N_(i;g))
            :param link: list of 1 and 0 showing connections until now
            :param ag:
            :param board:
            :param done: updated continuously vector through recursion -
            prevents repetitivity
            :return: list of binary agents position - data accessed
            """
            concts = get_concts(ag, board)
            if len(board) > 0 and concts:
                link[ag - 1] = 1
                done.append(ag)
                for i in concts:
                    if i not in done:
                        done.append(i)
                        link[i - 1] = 1
                        conctsi = get_concts(i, board)
                        if conctsi:
                            link = one_link(link, i, board, done)
                return link
            return link


        def find_links(ag, board):
            """
            Gets all options of next round
            :param ag:
            :param board:
            :return: list of lists of binary knowledge access
            """
            all_links = []
            for m in board:
                agent = m[0]
                base_link = build_empty(agent, len(board))
                base_link[ag - 1] = 1
                m_link = one_link(base_link, agent, board, [])
                all_links.append(m_link)
            return all_links


        def get_index_positions(list_of_elems, element):
            """Returns the indexes of all occurrences of give element in
            the list- listOfElements """
            index_pos_list = []
            index_pos = 0
            while True:
                try:
                    # Search for item in list from indexPos to the end of list
                    index_pos = list_of_elems.index(element, index_pos)
                    # Add the index position in list
                    index_pos_list.append(index_pos)
                    index_pos += 1
                except ValueError as e:
                    break
            return index_pos_list


        def combin(lst_o_bin):
            """
            returns 1 vector after summation off all vectors in lst_o_bin
            :param lst_o_bin: list of binary vectors
            :return: list type
            """
            if lst_o_bin:
                new_bin = np.array(lst_o_bin[0])
                for my_bin in lst_o_bin[1:]:
                    new_bin += np.array(my_bin)
                for elem in range(len(list(new_bin))):
                    if new_bin[elem] != 0:
                        new_bin[elem] = 1
                return list(new_bin)


        def remove_self(ag, lst):
            """
            returns a list with all variables except for 'ag' index'
            :param ag: index of agent
            :param lst:
            :return: list
            """
            return lst[:ag] + lst[ag + 1:]


        def empty_self(ag, brd):
            """
            returns the board with the empty connection for agent 'ag'
            :param ag:
            :param brd:
            :return: board (list of lists)
            """
            brd[ag - 1][1] = []
            return brd


        def plc_o_link(lst, locs):
            """
            returns a list of the variables in lst in indices 'locs'
            :param lst:
            :param locs: indices (list of locations)
            :return: list
            """
            return list(lst[i - 1] for i in locs)


        def info_n_cost(lst):
            """
            takes list of information accessed from certain permutations
            :param lst: list of pairs of info and links
            :return: list type
            """
            info_cost = []
            for ag in range(len(lst)):
                info_cost.append([sum(lst[ag][0]), len(lst[ag][1])])
            return info_cost


        def payoff(lst, c=C):
            """
            returns utility/ payoff of agent from any move according to cost
            :param lst: get list from info_n_cost function
            :param c: cost
            :return: list of payoffs
            """
            pay = []
            for ag in range(len(lst)):
                pay.append(lst[ag][0] - (lst[ag][1] * c))
            return pay


        def perm_combine(ag, links, perms):
            """
            finds all connection options by permutation
            :param ag: agent
            :param links: age
            :param perms: permutations
            :return: list
            """
            best_response = []
            for p in perms:
                if not p:
                    best_response.append([build_empty(ag, N), p])
                    continue
                links_plc = plc_o_link(links, p)
                best_response.append([combin(links_plc), p])
            return best_response


        def find_next_move(ag, board):
            """
            finds all best responses for each agent and chooses one
            :param ag: agent
            :param board: board
            :return: new move in board list mode
            """
            agents = list(range(1, len(board) + 1))
            agents.remove(ag)
            board1 = empty_self(ag, board[:])
            links = find_links(ag, board1)
            perms = my_perms(agents)
            best_response = perm_combine(ag, links, perms)
            info = info_n_cost(best_response)
            utility = payoff(info, C)
            index = get_index_positions(utility, max(utility))
            indices = [i + 1 for i in index]
            best = plc_o_link(perms, indices)
            return best


        def next_play(ag, brd):
            """
            applies new move or declares inertia of agent to board
            :param ag: agent
            :param brd: game board
            :return: new board with move added
            """
            new_board = cp.deepcopy(brd)
            if free_will(R):
                my_ops = find_next_move(ag, brd)
                my_next = rd.choice(my_ops)
                new_board[ag - 1][1] = my_next
                return [new_board, True]
            return [new_board, False]


        def binary_me(ag, brd):
            link = [0]*len(brd)
            link[ag - 1] = 1
            for i in get_concts(ag, brd):
                link[i - 1] = 1
            return link


        def dynamic_game():
            """
            plays a dynamic single game
            :return: number of rounds (turns / number of players)
            """
            lst_o_agents = list(range(1, N + 1))   # initiate list of agents
            init_game = init_all(lst_o_agents, N)  # sets the initial state
            my_board = init_game[:]
            count = 0
            turns = 0
            same = 0
            ag_costs = [0]*len(lst_o_agents)
            ag_payoffs = [0]*len(lst_o_agents)
            prob_stop = mt.log(STOP, R) if R else 0
            while count <= ROUNDS:  # max number of runs - include other stops
                count += 1
                if same < max(prob_stop, ROUND_STOP * N):
                    for ag in lst_o_agents:
                        turns += 1
                        last_board = cp.deepcopy(my_board)
                        state = next_play(ag, my_board)
                        if last_board == state[0]:
                            same += 1
                        else:
                            same = 0
                        my_board = state[0]
                        ag_costs[ag - 1] = len(my_board[ag - 1][1])
                        lnk = binary_me(ag, my_board)
                        updt_lnk = one_link(lnk, ag, my_board, [])
                        ag_payoffs[ag - 1] += (sum(updt_lnk) - C*ag_costs[ag - 1])
                else:
                    break
            return ag_payoffs


        for i in range(500):
            payoffs.append(dynamic_game())

        print("R = ", R, "&", "C = ", C, "&", "N = ", N)

        avgs = []
        for i in range(N):
            avgs.append([])
        for pay in payoffs:
            for j in range(N):
                avgs[j].append(pay[j])

        for k in range(N):
            print("The average payoff of agent", k, "is:",
                  round(np.average(avgs[k]), 2), "\nand the SE is:",
                  round(sem(avgs[k]), 2), "\n")
