import random
import sys

PointList = []
ClusterList = {}

class DataPoint:    # Class construction for each datapoint
    def __init__(self, channel, region, fresh_prod, milk, grocery, frozen_prod, detergent_paper, deli):
        self.id = None
        self.channel = channel
        self.region = region
        self.fresh_prod = fresh_prod
        self.milk = milk
        self.grocery = grocery
        self.frozen_prod = frozen_prod
        self.detergent_paper = detergent_paper
        self.deli = deli
        self.cluster = None     # Which cluster does the DataPoint belong to

class Cluster:      # Class construction for each cluster
    def __init__(self, id_no):
        self.id_no = id_no
        self.centroid = None
        self.contains = []      # List of the DataPoints that belongs to the Cluster
        self.count = 0

inFile = open("costumer.data")
dp_id = 0               # Sets a start id to 0.
for line in inFile.readlines()[1:]: # Reads all but the first line of the document and puts it into classes.
    line = line[:-1] # Skips the /n in the end of each line
    channel, region, fresh_prod, milk, grocery, frozen_prod, detergents_paper, deli = line.split(",")
    newPoint = DataPoint(int(channel), int(region), int(fresh_prod), int(milk), int(grocery), int(frozen_prod), int(detergents_paper), int(deli))   # Converts the strings to ints.
    newPoint.id = dp_id     # Adds the id to the created DataPoint
    PointList.append(newPoint)  # Appends the Datapoint to the PointList.
    dp_id += 1  # Increments the id with one (for the next lines DataPoint
inFile.close()
del inFile

def k_mean_init(dp_list, k):                        # Randomly puts the datapoints in to a cluster and, creates and puts the clusters in the ClusterList
    for i in range(1, k+1):
        newCluster = Cluster(i)                     # Creates a cluster with an id from 1 and up to the number of wanted clusters.
        ClusterList[newCluster.id_no] = newCluster  # Adds the cluster to the list of clusters.
    for dp in dp_list:                              # Appends the datapoints to the "contains" list of the cluster.
        dp.cluster = random.randrange(1, k+1)       # Randomly devides the datapoints in to a cluster. i.e. 2
        ClusterList[dp.cluster].contains.append(dp) # i.e. Clusterlist[position 2], append the dp to that clusters list; "contains"

def calculate_centroid():                               # Sets all the mean values for all the Clusters.
    for cluster in ClusterList:                         # Loops thru the ClusterList
        cent = DataPoint(0, 0, 0, 0, 0, 0, 0, 0)        # Creates cent as the class DataPoint with all zeros on the variables.
        for dp in ClusterList[cluster].contains:        # Loops thru the datapoints that exists in the selected cluster.
            cent.channel += dp.channel                  # Adds the value that the datapoint has to cent to create a counter
            cent.region += dp.region                    # Adds the value that the datapoint has to cent to create a counter
            cent.fresh_prod += dp.fresh_prod            # Adds the value that the datapoint has to cent to create a counter
            cent.milk += dp.milk                        # Adds the value that the datapoint has to cent to create a counter
            cent.grocery += dp.grocery                  # Adds the value that the datapoint has to cent to create a counter
            cent.frozen_prod += dp.frozen_prod          # Adds the value that the datapoint has to cent to create a counter
            cent.detergent_paper += dp.detergent_paper  # Adds the value that the datapoint has to cent to create a counter
            cent.deli += dp.deli                        # Adds the value that the datapoint has to cent to create a counter
        cent.channel /= len(ClusterList[cluster].contains)          # Sets the mean value for the Cluster.
        cent.region /= len(ClusterList[cluster].contains)           # Sets the mean value for the Cluster.
        cent.fresh_prod /= len(ClusterList[cluster].contains)       # Sets the mean value for the Cluster.
        cent.milk /= len(ClusterList[cluster].contains)             # Sets the mean value for the Cluster.
        cent.grocery /= len(ClusterList[cluster].contains)          # Sets the mean value for the Cluster.
        cent.frozen_prod /= len(ClusterList[cluster].contains)      # Sets the mean value for the Cluster.
        cent.detergent_paper /= len(ClusterList[cluster].contains)  # Sets the mean value for the Cluster.
        cent.deli /= len(ClusterList[cluster].contains)             # Sets the mean value for the Cluster.
        ClusterList[cluster].centroid = cent                        # Sets the mean value for the Cluster.

def reassign(n):                                                # Reassign the points to there now nearest Cluster.
    changed = 0
    for point in PointList:                                     # Loops thru all the points in the PointsList.
        next_cluster = nearest(point, n)                        # Returns the cluster that the point is nearest at this point.
        if point.cluster != next_cluster:                       # If the point is nearer a nother cluster...
            ClusterList[point.cluster].contains.remove(point)   # remove it from the cluster it belongs to now and...
            ClusterList[next_cluster].contains.append(point)    # add it to the cluster it is nearest to.
            point.cluster = next_cluster                        # Set the points.cluster to the new cluster value.
            changed += 1                                        # Add 1 to the changed counter if a change has occured.
    return changed                                              # Return 0 if no changes have been made, otherwise return the number of changes.


def nearest(point, n):      # Calculates the nearest Cluster for the point.
    near = None             # Sets the return variable to none.
    min_dist = sys.maxsize  # Gets the maximum size a variable of Py_ssize_t can have on the system and sets that to the min_dist.
    for cluster in ClusterList: # Loops thru the ClusterList
        if n == 1:                  # If Channel is chosen...
            ch = 0                  # set ch to 0...
        else:
            ch = abs(point.channel - ClusterList[cluster].centroid.channel)     # else set it to the absolute value of the points.channel value minus the clusters centroid.channel value.
        if n == 2:                  # If Region is chosen...
            re = 0                  # set re to 0...
        else:
            re = abs(point.region - ClusterList[cluster].centroid.region)       # else set it to the absolut value of the points.region value minus the clusters centroid.region value.
        if n == 3:                  # If fresh is chosen...
            fs = 0
        else:
            fs = abs(point.fresh_prod - ClusterList[cluster].centroid.fresh_prod)
        if n == 4:                  # If milk is chosen...
            mi = 0
        else:
            mi = abs(point.milk - ClusterList[cluster].centroid.milk)
        if n == 5:                  # If grocery i chosen...
            gr = 0
        else:
            gr = abs(point.grocery - ClusterList[cluster].centroid.grocery)
        if n == 6:                  # If frozen is chosen...
            fn = 0
        else:
            fn = abs(point.frozen_prod - ClusterList[cluster].centroid.frozen_prod)
        if n == 7:                  # If detergent_paper is chosen...
            dp = 0
        else:
            dp = abs(point.detergent_paper - ClusterList[cluster].centroid.detergent_paper)
        if n == 8:                  # If delicatessen is chosen...
            de = 0
        else:
            de = abs(point.deli - ClusterList[cluster].centroid.deli)

        #if __name__ == '__main__':
        dist = ch + re + fs + mi + gr + fn + dp + de        # Adds the the vars above to dist.

        if dist < min_dist:     # If dist is less then sys.maxsize..
            min_dist = dist     # set min_dist to dist...
            near = cluster      # and set the cluster to near

    return near     # Return cluster.


def count_spec(cluster, n, x):      # Counts the number of points a Cluster contains according to the chosen sorting (region or channel)
    num = 0
    if n == 1:
        for point in ClusterList[cluster].contains:
            if point.region == x:
                num += 1
    if n == 2:
        for point in ClusterList[cluster].contains:
            if point.channel == x:
                num += 1
    return num


def print_ClusterList(n):
    if n == 1:
        arg = "channel"
    if n == 2:
        arg = "region"
    for cluster in ClusterList:
        print("Cluster number:", cluster)                                       # Prints the Clusters number
        print("Number of cases:", len(ClusterList[cluster].contains))           # Prints the number of points the Cluster cointains
        if n == 1:        # If Channel is chosen
            print("Number of cases in region: Lisabon:",
                  count_spec(cluster, n, 1))  # Counts and prints how many there is of this region in the specific Cluster
            print("Number of cases in region: Oporto:",
                  count_spec(cluster, n, 2))  # Counts and prints how many there is of this region in the specific Cluster
            print("Number of cases in region: Other:",
                  count_spec(cluster, n, 3))  # Counts and prints how many there is of this region in the specific Cluster
            print("Centroid values:")
            if int(ClusterList[cluster].centroid.channel) == 1:
                print("\tChannel: Hotel/restaurant/café")
            if int(ClusterList[cluster].centroid.channel) == 2:
                print("\tChannel: Retail")

        if n == 2:                                                              # If Region is chosen
            print("Number of cases in channel hotel/restaurant/café:", count_spec(cluster, n, 1))   # Counts and prints how many there is of this channel in the specific Cluster
            print("Number of cases in channel retail:", count_spec(cluster, n, 2))                  # Counts and prints how many there is of this channel in the specific Cluster
            print("Centroid values:")
            if int(ClusterList[cluster].centroid.region) == 1:
                print("\tRegion: Lisbon")
            if int(ClusterList[cluster].centroid.region) == 2:
                print("\tRegion: Oporto")
            if int(ClusterList[cluster].centroid.region) == 3:
                print("\tRegion: Other")
        print("\tFresh produce:", int(ClusterList[cluster].centroid.fresh_prod))                    # Prints the mean value for the specific Cluster
        print("\tMilk:", int(ClusterList[cluster].centroid.milk))                                   # Prints the mean value for the specific Cluster
        print("\tGrocery:", int(ClusterList[cluster].centroid.grocery))                             # Prints the mean value for the specific Cluster
        print("\tFrozen produce:", int(ClusterList[cluster].centroid.frozen_prod))                  # Prints the mean value for the specific Cluster
        print("\tDetergent paper:", int(ClusterList[cluster].centroid.detergent_paper))             # Prints the mean value for the specific Cluster
        print("\tDeli:", int(ClusterList[cluster].centroid.deli))                                   # Prints the mean value for the specific Cluster
        print("\n------------\n")


def k_mean(k, n):
    print("\n------------------------------------\n")
    k_mean_init(PointList, k)       # Randomly puts the datapoints in to a cluster and, creates and puts the clusters in the ClusterList
    change = 1
    while change > 0:
        calculate_centroid()        # Sets all the mean_values of all the Clusters.
        change = reassign(n)        # Sets the change value to 0 if there is no more changes done.
    print_ClusterList(n)            # When done - print the Clusters.

k_value = int(input("Give k-value "))                   # Asks for input for k_value and converts it to an int.
n_value = int(input("1) Channel\n2) Region\nYour choice? "))    # Asks for input for n_value and converts it to an int.

k_mean(k_value, n_value)        # Runs k_mean with the selected values. k_mean runs the rest of the program.
