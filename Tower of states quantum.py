"""
To obtain the configurations for different energy states, to calculate the energies of these respective energy states and to calculate degeneracy factors for states.
Also, plots the change in energy of successive levels to the levels themselves, proving an inverse relatioship between the change in energy and the square root of energy.

MENU:
    1. Configuration list for first n states with degeneracy
    2. Configuration for a specific state with degeneracy
    3. Energies of first n states
    4. Energy of the nth state
    5. Energy difference between any two states
    6. Degeneracy factor of a specific state
    7. Plot dE vs. n graph for a given value of n

Authors: Chirag Bapat, Dinesh Babu S
Date and time of creation: 7th February, 2019 @ 23:57
Last save for a major change: 26th February, 2019 @ 19:50
Last major change: Fixed problem 4: PLotting working for all cases
"""


"""

PROBLEMS:
1. Degeneracy factor (FIXED)
    First occurence at sum of squares = 14 and 15

2. Refactor all code to account for revised get_config_list code (FIXED)

3. Error handling in all cases (FIXED)

4. Plotting not working for state_num <= 7 (FIXED)

"""


def sum_of_squares(temp): # Calculates sum of squares of elements of a list
    return (temp[0] ** 2) + (temp[1] ** 2) + (temp[2] ** 2)

def get_config_list(n): # Gets total list of configurations
    energy_configs = [[[1,1,1]]]
    for sq_sum in range(6, 2*n+4):
        for i in range(1, int(sq_sum / 3) + 1):
            for j in range(1, int(sq_sum / 3) + 1):
                for k in range(1, int(sq_sum / 3) + 1):
                    calc_sq_sum = sum_of_squares([i, j, k])
                    if calc_sq_sum == sq_sum:
                        test = [i,j,k]
                        test.sort()
                        for l in range(len(energy_configs)):
                            if test not in energy_configs[len(energy_configs) - 1]:
                                if sum_of_squares(test) == sum_of_squares(energy_configs[len(energy_configs) - 1][0]):
                                    energy_configs[len(energy_configs) - 1].append(test)
                                else:
                                    energy_configs.append([test])

    return energy_configs

def get_specific_config(config_list, state_num): # Gets configuration of a given state
    specific_config = []
    for x in config_list[state_num - 1]:
        specific_config.append(x)
    
    return specific_config


def calculate_energy(config_list, state_num, a): # Gets energy of a given state divided by the actual scalar factor
    h = 6.626e-34
    m = 9.1e-31

    sum_of_configs_for_state = (config_list[state_num - 1][0][0] ** 2) + (config_list[state_num - 1][0][1] ** 2)+(config_list[state_num - 1][0][2] ** 2)
    E = ((h ** 2) / (8 * m * (a ** 2) * 1.6)) * sum_of_configs_for_state * (10 ** 39) #- Actual energy
    #E = sum_of_configs_for_state # Simplified energy

    return E

def list_energies(config_list, state_num, a): # Lists energies of states till a limit
    for i in range(state_num):
        print("Energy of state #", str(i + 1), "=", str(calculate_energy(config_list, i + 1, a)), "eV")

    return

def energy_diff(config_list, state1, state2, a): # Gets energy difference between any two states
    E_low = calculate_energy(config_list, state1, a)
    E_high = calculate_energy(config_list, state2, a)
    
    return E_high - E_low

def degeneracy(config_list, state_num): # Gets degeneracy factor for a specific state
    degeneracy = 0

    for x in config_list[state_num - 1]:
        if x[0] == x[1] and x[0] == x[2]:
            degeneracy += 1
        elif x[0] == x[1] or x[1] == x[2] or x[2] == x[0]:
            degeneracy += 3
        else:
            degeneracy += 6

    return degeneracy

def plot_dE_n(config_list, state_num, a): # Plots graph between change in energy on y axis and energy state on x axis
    
    dE = [energy_diff(config_list, i, i + 1, a) for i in range(1, state_num)]
    n = [i for i in range(1, state_num)]

    import matplotlib.pyplot as plt
    plt.axis([0, state_num + 1, -5, 5])
    plt.hlines(0, 0, state_num, linestyles = 'dashed', label = 'Degenerate')
    plt.axvline(x = 0, linestyle = 'dashed', color = 'black')
    plt.grid()
    plt.plot(n, dE)    
    plt.show()

    return


# Start of execution of script

continue_flag = True

while continue_flag is True:
    # Print Menu
    print("1. Get all configurations for a number of states (with degeneracy factors)")
    print("2. Get specific configuration for a given state (with degeneracy factor)")
    print("3. Get all energies for a number of states")
    print("4. Get energy of a specific state")
    print("5. Get energy difference between any two states")
    print("6. Get degeneracy factor of a specific state")
    print("7. Plot change in energy vs. n graph")
    ch = input("Enter choice: ")
    print("")

    if ch == "1":
        n = input("Enter number of states: ")
        
        if (n.isnumeric() is True) and (n != "0"):
            config_list = get_config_list(int(n))
        
            for i in range(int(n)):
                if len(config_list[i]) > 1:
                    print("Energy level configurations for state #" + str(i + 1), "(Degeneracy factor = " + str(degeneracy(config_list, i + 1)) + "): ")
                    for x in config_list[i]:
                        print("(", str(x[0]), ",", str(x[1]), ",", str(x[2]), ")")
                else:
                    print("Energy level configuration for state #" + str(i + 1), "(Degeneracy factor = " + str(degeneracy(config_list, i + 1)) + "): ")
                    print("(", str(config_list[i][0][0]), ",", str(config_list[i][0][1]), ",", str(config_list[i][0][2]), ")")

        else:
            print("Wrong input")
            
    elif ch == "2":
        state_num = input("Enter state for which configuration is to be found: ")
        
        if (state_num.isnumeric() is True) and (state_num != "0"):
            config_list = get_config_list(int(state_num))
            cur_config = get_specific_config(config_list, int(state_num))
            print("Energy level configurations for state #" + state_num, ": (Degeneracy factor:", str(degeneracy(config_list, int(state_num))) + ")")

            for i in range(len(cur_config)):
                print(str(i + 1) + ": (", str(cur_config[i][0]), ",", str(cur_config[i][1]), ",", str(cur_config[i][2]), ")")

        else:
            print("Wrong input")

    elif ch == "3":
        a = input("Enter dimension of infinite well (in angstroms): ")
        
        if (a.isnumeric() is True) and (a != "0"):
            state_num = input("Enter energy state limit: ")
            
            if (state_num.isnumeric() is True) and (state_num != "0"):
                config_list = get_config_list(int(state_num))
                list_energies(config_list, int(state_num), int(a))

            else:
                print("Wrong input")

        else:
            print("Wrong input")

    elif ch == "4":
        a = input("Enter dimension of infinite well (in angstroms): ")
        
        if (a.isnumeric() is True) and (a != "0"):
            state_num = input("Enter energy state for which energy is to be calculated: ")
            
            if (state_num.isnumeric() is True) and (state_num != "0"): 
                config_list = get_config_list(int(state_num))
                print("Energy of state #" + state_num, " = ", calculate_energy(config_list, int(state_num), int(a)), "eV")

            else:
                print("Wrong input")
                
        else:
            print("Wrong input")

    elif ch == "5":
        a = input("Enter dimension of infinite well (in angstroms): ")

        if (a.isnumeric() is True) and (a != "0"):
            state1 = input("Enter the lower energy state: ")

            if (state1.isnumeric() is True) and (state1 != "0"):
                state2 = input("Enter the higher energy state: ")

                if (state2.isnumeric() is True) and (state2 != "0") and (int(state1) <= int(state2)):
                    config_list = get_config_list(int(state2))
                    print("E_" + state2, "- E_" + state1, "=", energy_diff(config_list, int(state1), int(state2), int(a)), "eV")

                else:
                    print("Wrong input")

            else:
                print("Wrong input")

        else:
            print("Wrong input")

    elif ch == "6":
        state_num = input("Enter state for which degeneracy is to be calculated: ")

        if (state_num.isnumeric() is True) and (state_num != "0"):
            config_list = get_config_list(int(state_num))
            print("Degeneracy of state #" + state_num, "=", str(degeneracy(config_list, int(state_num))))

        else:
            print("Wrong input")

    elif ch == "7":
        state_num = input("Enter the maximum value of state number: ")

        if (state_num.isnumeric() is True) and (state_num != "0"):
            a = input("Enter dimension of infinite well (in angstroms): ")

            if (a.isnumeric() is True) and (a != "0"):
                config_list = get_config_list(int(state_num))
                plot_dE_n(config_list, int(state_num), int(a))

            else:
                print("Wrong input")

        else:
            print("Wrong input")

    else:
        print("Wrong option entered")

    print("")
    continue_ch = (input("Enter 1 to continue, anything else to exit: "))
    if continue_ch != "1":
        continue_flag = False
    print("")


print("Goodbye!")
