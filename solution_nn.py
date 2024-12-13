from random_instance import *
import time



def wanted_date():
    options = os.listdir(os.path.join("Outputs", ))
    print(options)

    date = input('date: ')
    directory_read = os.path.join("Outputs", date)
    return date, directory_read

all_distances = []
ID_List2= []
all_totalCost = []
all_FuelConsumption = []
all_fuelPrice = []
fuel_needed = []

def readdistancesOutput(date, directory_read):
    distances_file_name = 'distances_' + date + '.csv'

    # construct the full file path using the 'directory' variable
    file_path = os.path.join(directory_read, distances_file_name)

    # read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=';')
    from_read = df['from'].tolist()
    to_read = df['to'].tolist()
    # extract the 'time' column as a list
    distances_read = df['distances'].tolist()

    for i in range(len(distances_read)):
        all_distances.append([from_read[i], to_read[i], distances_read[i]])

def readcitiesOutput(date, directory_read):
    cities_file_name = 'cities_' + date + '.csv'

    # construct the full file path using the 'directory' variable
    file_path = os.path.join(directory_read, cities_file_name)

    # read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=';')
    cityId_read = df['City ID'].tolist()

    for i in range(len(cityId_read)):
        ID_List2.append(cityId_read[i])

def readtotalCostOutput(date, directory_read):
    totalCost_file_name = 'totalCost_' + date + '.csv'

    # construct the full file path using the 'directory' variable
    file_path = os.path.join(directory_read, totalCost_file_name)

    # read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=';')
    from_read = df['from'].tolist()
    to_read = df['to'].tolist()
    # extract the 'totalCost' column as a list
    totalCost_read = df['Total Cost'].tolist()

    for i in range(len(totalCost_read)):
        all_totalCost.append([from_read[i], to_read[i], totalCost_read[i]])
        
def readFuelConsumptionOutput(date, directory_read):
    FuelConsumption_file_name = 'fuel_consumption_' + date + '.csv'

    # construct the full file path using the 'directory' variable
    file_path = os.path.join(directory_read, FuelConsumption_file_name)

    # read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=';')
    from_read = df['from'].tolist()
    to_read = df['to'].tolist()
    # extract the 'time' column as a list
    FuelConsumption_read = df['FuelConsumption'].tolist()

    for i in range(len(FuelConsumption_read)):
        all_FuelConsumption.append([from_read[i], to_read[i], FuelConsumption_read[i]])
        
def readFuelPriceOutput(date, directory_read):
    fuelPrice_file_name = 'fuel_price_' + date + '.csv'

    # construct the full file path using the 'directory' variable
    file_path = os.path.join(directory_read, fuelPrice_file_name)

    # read the CSV file into a DataFrame
    df = pd.read_csv(file_path, sep=';')
    City_ID_read = df['cityID'].tolist()
    # extract the 'time' column as a list
    fuelPrice_read = df['fuelPrice'].tolist()

    for i in range(len(fuelPrice_read)):
        all_fuelPrice.append([City_ID_read[i], fuelPrice_read[i]])

def finding_fuel_needed():
    for i in range(len(all_distances)):
        fuel_needed.append([all_distances[i][0] ,all_distances[i][1] , all_distances[i][2] * all_FuelConsumption[i][2]])


def readAllAsCSV():
    date, directory_read = wanted_date()
    readcitiesOutput(date, directory_read)
    readdistancesOutput(date, directory_read)
    readtotalCostOutput(date, directory_read)
    readFuelPriceOutput(date, directory_read)
    readFuelConsumptionOutput(date, directory_read)
    finding_fuel_needed()


def nearest_neighbor_path(start_city_id, end_city_id, all_distances):
    path = [start_city_id]
    current_city_id = start_city_id
    
    while current_city_id != end_city_id:
        # Get distances from the current city to all other cities
        distances_from_current_city = [(city_1, city_2, distance) for city_1, city_2, distance in all_distances 
                                       if city_1 == current_city_id  and distance != -1]
        
        # Calculate the distance from each neighboring city to the end city
        distances_to_end_city = {}
        for city_1, city_2, distance in all_distances:
            if city_2 == end_city_id:
                distances_to_end_city[city_1] = distance
           
        # Find the closest neighboring city that hasn't been visited yet, taking into account the distance to the end city
        closest_total_distance = float('inf')
        closest_neighbor_id = None
        for city_id1, city_id2, distance in distances_from_current_city:
            if city_id1 == current_city_id:
                neighbor_id = city_id2
                if neighbor_id not in path:
                    if neighbor_id == end_city_id:
                        distance_to_end = distance
                        total_distance = distance_to_end
                        if total_distance < closest_total_distance:
                            closest_total_distance = total_distance
                            closest_neighbor_id = neighbor_id
                    elif neighbor_id in distances_to_end_city:
                        distance_to_end = distances_to_end_city[neighbor_id]
                        total_distance = distance + distance_to_end
                        if total_distance < closest_total_distance:
                            closest_total_distance = total_distance
                            closest_neighbor_id = neighbor_id
        
        if closest_neighbor_id is None:
            closest_neighbor_id = end_city_id
            # If no unvisited neighboring city is found, terminate the loop
            
                
        # Add the closest neighbor to the path and update the current city
        path.append(closest_neighbor_id)
        current_city_id = closest_neighbor_id
        
    return path

def nearest_neighbor_path_cost(start_city_id, end_city_id, all_costs, distances):
    path = [start_city_id]
    current_city_id = start_city_id
    
    while current_city_id != end_city_id:
        # Get costs from the current city to all other cities
        costs_from_current_city = [(city_1, city_2, cost) for city_1, city_2, cost in all_costs 
                                   if city_1 == current_city_id]
        
        # Calculate the cost from each neighboring city to the end city
        costs_to_end_city = {}
        for city_1, city_2, cost in all_costs:
            if city_2 == end_city_id:
                costs_to_end_city[city_1] = cost
           
        # Find the closest neighboring city that hasn't been visited yet, taking into account the cost to the end city
        closest_total_cost = float('inf')
        closest_neighbor_id = None
        for city_id1, city_id2, cost in costs_from_current_city:
            if city_id1 == current_city_id:
                neighbor_id = city_id2
                if neighbor_id not in path:
                    # Find the corresponding distance between city_id1 and city_id2
                    distance = next((dist for dist in distances if dist[0] == city_id1 and dist[1] == city_id2), None)
                    if distance is not None and distance[2] != -1:
                        if neighbor_id == end_city_id:
                            cost_to_end = cost
                            total_cost = cost_to_end
                            if total_cost < closest_total_cost:
                                closest_total_cost = total_cost
                                closest_neighbor_id = neighbor_id
                        elif neighbor_id in costs_to_end_city:
                            cost_to_end = costs_to_end_city[neighbor_id]
                            total_cost = cost + cost_to_end
                            if total_cost < closest_total_cost:
                                closest_total_cost = total_cost
                                closest_neighbor_id = neighbor_id
        
        if closest_neighbor_id is None:
            closest_neighbor_id = end_city_id
            # If no unvisited neighboring city is found, terminate the loop

        # Add the closest neighbor to the path and update the current city
        path.append(closest_neighbor_id)
        current_city_id = closest_neighbor_id
        
    return path

def minimize_fuel_cost(path, fuel_needed, fuel_price, max_fuel_capacity, starting_fuel):
    fuel_cost = 0  # Initialize total fuel cost
    current_fuel = starting_fuel  # Initialize current fuel level
    fuel_purchases = []  # List to store fuel purchases
    
    fuel_prices_in_path = {}  # Dictionary to store fuel prices of cities in the path
    
    # Find the fuel prices of cities in the path
    for city, price in fuel_price:
        if city in path:
            fuel_prices_in_path[city] = price
    
    # Create a copy of fuel_prices_in_path
    modified_fuel_prices = fuel_prices_in_path.copy()

    # Set the last element's value to infinity
    last_key = path[-1]
    modified_fuel_prices[last_key] = float('inf')

    # Sort the modified dictionary by values
    sorted_fuel_prices = sorted(modified_fuel_prices.items(), key=lambda x: x[1])
    

       
    # Iterate through each city in the path
    for i in range(len(path)-1):
        source_city = path[i]
        destination_city = path[i+1]
        fuel_needed_current_leg = None
        
        # Find the fuel needed for the current leg of the journey
        for fuel_leg in fuel_needed:
            if fuel_leg[0] == source_city and fuel_leg[1] == destination_city:
                fuel_needed_current_leg = fuel_leg[2]
                break
        
        # Check if the destination is the last city
        if i ==  path[len(path) - 2] and i == path[0]:
            
            # Finish the journey at the destination city (no need to buy fuel)
            if fuel_needed_current_leg <= current_fuel:
                current_fuel = current_fuel - fuel_needed_current_leg
                continue
            else:
                # Fill the tank with the amount of fuel needed for the current leg
                fuel_to_buy = fuel_needed_current_leg - current_fuel
                fuel_cost += fuel_to_buy * fuel_prices_in_path[source_city]
                current_fuel = 0
                fuel_purchases.append((source_city, fuel_to_buy))
                break
                
                
                
                
        # Check if the destination is the minimum fuel price city
        if source_city == sorted_fuel_prices[0][0]:
            # Fill the tank with the amount of fuel on hand to reach the next city
            fuel_to_buy = max_fuel_capacity - current_fuel
            fuel_cost += fuel_to_buy * fuel_prices_in_path[source_city]
            current_fuel = max_fuel_capacity - fuel_needed_current_leg
            fuel_purchases.append((source_city, fuel_to_buy))
            
        else:
            # Check if it's possible to reach the destination with current fuel
            if fuel_needed_current_leg <= current_fuel:
                current_fuel = current_fuel - fuel_needed_current_leg
                # Find the next minimum fuel price city that is reachable with current fuel
                continue       
            else:
                # Fill the tank with the amount of fuel needed for the current leg
                fuel_to_buy = fuel_needed_current_leg - current_fuel
                fuel_cost += fuel_to_buy * fuel_prices_in_path[source_city]
                current_fuel = 0
                fuel_purchases.append((source_city, fuel_to_buy))
    
    # Return the list of fuel purchases and the total fuel cost
    return fuel_purchases, fuel_cost


def calculate_path_distance(path, all_distances):
    total_distance = 0
    
    for i in range(len(path)-1):
        city_id1 = path[i]
        city_id2 = path[i+1]
        
        # Look up the distance between the two cities
        for (city_1,city_2, distance) in all_distances:
            if (city_id1, city_id2) == (city_1,city_2) or (city_id2, city_id1) == (city_1,city_2) and distance != -1:
                total_distance += distance
                break
                
    return total_distance


def sol_with_ids(i,j):
    start_city_id  = i
    end_city_id = j
    path = nearest_neighbor_path(start_city_id, end_city_id, all_distances)
    total_distance = calculate_path_distance(path, all_distances)  
    print(f"Path from {start_city_id} to {end_city_id}: {path}")
    print(f"Total Distance: {total_distance}")
    
   
    
def sol_with_ids_cost(i,j):
    start_city_id  = i
    end_city_id = j
    path = nearest_neighbor_path_cost(start_city_id, end_city_id, all_totalCost, all_distances)
    total_costs = calculate_path_distance(path, all_totalCost)  
    print(f"Path from {start_city_id} to {end_city_id}: {path}")
    print(f"Total Cost: {total_costs}")
    
    return path

def sol_for_all():
    for i in ID_List2:    
        for j in ID_List2:
            if i!= j:
                start_city_id = i
                end_city_id = j
                path = nearest_neighbor_path(start_city_id, end_city_id, all_distances)
                total_distance = calculate_path_distance(path, all_distances)  
                print(f"Path from {start_city_id} to {end_city_id}: {path}")
                print(f"Total Distance: {total_distance}")  
            
            
saveNNdistance_csv = []            

    
def save_for_nn_distance():          
    
    for i in ID_List2: 
        for j in ID_List2:
            if i!=j:
                start_city_id = i
                end_city_id = j
                path = nearest_neighbor_path(start_city_id, end_city_id, all_distances)
                total_distance = calculate_path_distance(path, all_distances)  
                total_costs = calculate_path_distance(path, all_totalCost) 
                fuel_purchase , fuel_cost = minimize_fuel_cost(path, fuel_needed, all_fuelPrice, F, Sf)
                saveNNdistance_csv.append([start_city_id, end_city_id, path, total_distance, total_costs + fuel_cost, fuel_purchase, fuel_cost])

        

def saveSolutionNNDistanceOutput():
    df_SolutionNNMatrix = pd.DataFrame(saveNNdistance_csv)
    # define csv file name
    solutionNN_file_name = 'solution_NN_distance' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    # set column names
    df_SolutionNNMatrix.columns = ['from', 'to', 'path', 'distances', 'totalcost', 'City_Amount', 'fuel cost' ]
    # writing data frame to a CSV file
    if not os.path.exists(sol_nn_directory):
        os.makedirs(sol_nn_directory)
    # writing data frame to a CSV file
    df_SolutionNNMatrix.to_csv(os.path.join(sol_nn_directory, solutionNN_file_name), sep=';', index=False)
   


saveNNcost_csv = [] 
    
def save_for_nn_cost():          
    
    for i in ID_List2: 
        for j in ID_List2:
            if i!=j:
                start_city_id = i
                end_city_id = j
                path = nearest_neighbor_path_cost(start_city_id, end_city_id, all_totalCost, all_distances)
                total_costs = calculate_path_distance(path, all_totalCost)  
                total_distance = calculate_path_distance(path, all_distances)
                fuel_purchase , fuel_cost = minimize_fuel_cost(path, fuel_needed, all_fuelPrice, F, Sf)
                saveNNcost_csv.append([start_city_id, end_city_id, path, total_costs + fuel_cost, total_distance, fuel_purchase, fuel_cost])
                

        

def saveSolutionNNCostOutput():
    df_SolutionNNMatrix = pd.DataFrame(saveNNcost_csv)
    # define csv file name
    solutionNN_file_name = 'solution_NN_cost' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
    # set column names
    df_SolutionNNMatrix.columns = ['from', 'to', 'path', 'totalcost', 'distances', 'City_Amount', 'fuel cost' ]
    # writing data frame to a CSV file
    if not os.path.exists(sol_nn_directory):
        os.makedirs(sol_nn_directory)
    # writing data frame to a CSV file
    df_SolutionNNMatrix.to_csv(os.path.join(sol_nn_directory, solutionNN_file_name), sep=';', index=False)
   
        
def saveNN():
    readAllAsCSV()
    save_for_nn_distance()
    saveSolutionNNDistanceOutput()
    save_for_nn_cost()
    saveSolutionNNCostOutput()  
    
#saveNN()

#readAllAsCSV()
start_time = time.time()
#sol_with_ids_cost(2,450)
#sol_for_all() 

end_time = time.time()
elapsed_time = end_time - start_time
#print("Passing time: {:.5f} seconds".format(elapsed_time))