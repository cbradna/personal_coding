import random
import sys
import time
h = [0,50]
f = [100, 50]
nodes = []

# constant of proportionality that depends on dimentions of grid
# This constant corresponds to the greatest possible distance than can be traveled in the grid
alpha = ((100**2)+100)**2

#### Function used




# Generate nodes randomly
def gen_nodes():
    num_n = int(input('How many nodes in the grid?  '))
    nodes.append(h)
    while len(nodes) < num_n+1:
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        new_node = [x,y]
        if new_node not in nodes:
            nodes.append(new_node)
    nodes.append(f)

# Creates random paths out of the nodes
def choice():
    choices = []
    def current_choice():
        choice_arr = []
        choice_arr.append(nodes[0])
        current_choice = nodes[0]
        curr_ch_indx = nodes.index(current_choice)
        previous_node = 0
        while current_choice != nodes[-1]:
            next_node = random.choice(nodes)
            if next_node != previous_node:
                if next_node != current_choice:
                    if next_node not in choice_arr:
                        curr_ch_indx = nodes.index(next_node)
                        previous_node = current_choice
                        current_choice = next_node
                        choice_arr.append(current_choice)
        return choice_arr
        
    # repeat the creation of paths until all nodes are included.
    def node_check(cho):
        cho_f = [y for x in cho for y in x]
        check_buff = []
        for i in cho_f:
            if i not in check_buff:
                check_buff.append(i)
        if len(nodes) == len(check_buff):
            check = 1
        else:
            check = 0
        return check
    check = node_check(choices)
    
    while check != 1:
        choice_a = current_choice()
        if choice_a not in choices:
            choices.append(choice_a)
        check = node_check(choices)
    
    return choices

# Analyzes the nodes and determines possible next choices
def init_compatib_chart(cho):
    table_0 = [[] for i in range(0, len(nodes)-1)]
    for i in cho:
        for j in i:
            # current_node = j
            curr_nd_indx_in_nodes = nodes.index(j)
            curr_nd_indx_in_path = i.index(j)
            food = nodes[-1]
            if j != food:
                next_node_indx_path = curr_nd_indx_in_path+1
                next_node_in_path = i[next_node_indx_path]
                table_0[curr_nd_indx_in_nodes].append(next_node_in_path)
    return table_0
    
# Pythagorean theorem; used to find distance between two nodes
def pythag(x,y):
    base = y[0]-x[0]
    base = base**2
    height = y[1]-x[1]
    height = height**2
    dist = base+height
    dist = dist**.5
    return dist


# Representation of ant: traverses paths and adds "pheromone"
def ant(a):
    choice_arr = []
    choice_arr.append(nodes[0])
    current_choice = nodes[0]
    curr_ch_indx = nodes.index(current_choice)
    while current_choice != nodes[-1]:
        next_node = random.choice(a[curr_ch_indx])
        if next_node != current_choice:
            curr_ch_indx = nodes.index(next_node)
            current_choice = next_node
            choice_arr.append(current_choice)
    i = 0
    trip_tot = 0
    while i < len(choice_arr)-1:
        init_point_indx = i
        init_point = choice_arr[init_point_indx]
        chosen_node_indx = i + 1
        chosen_node = choice_arr[chosen_node_indx]
        trip = pythag(init_point,chosen_node)
        trip_tot += trip

        i = i + 1

    i = 0
    
    while i < len(choice_arr)-1:
        init_point_indx = i
        init_point = choice_arr[init_point_indx]
        chosen_node_indx = i + 1
        chosen_node = choice_arr[chosen_node_indx]
        gamma = int(round(0.01*(alpha/(trip_tot**2)))) # could also make it inversly proportional to the number of nodes taken
        k = 0
        crrnt_lmnt_indx_in_nodes = nodes.index(init_point)
        while k < gamma:
            a[crrnt_lmnt_indx_in_nodes].append(chosen_node)
            k = k+1
        i = i + 1
        

    return choice_arr,a,trip_tot

# Executions of functions

choice_s = choice()
table_0 = [[] for i in range(0, len(nodes)-1)]
init_compatib_chart(choice_s)


def main_loop():
    gen_nodes()
    choice_s = choice()
    table1 = init_compatib_chart(choice_s)
    ants = 0
    print ("Nodes generated: ",nodes)
    print ("Paths generated: ",choice_s)
    c=1
    for i in table_0:
        print ('Node',c,": ",i)
        c+=1
    while 1:
        choices_init,table1,trip_d = ant(table1)
        time.sleep(0.25)
        print ("\nData for ant # ",ants)
        # print "Choices made: ", choices_init
        table_f1 = [y for x in table1 for y in x]
        print ('Node Frequency',len(table_f1))
        print ('Trip distance: ',trip_d)
        print ('Path taken: ',choices_init)
        ants = ants + 1

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)

