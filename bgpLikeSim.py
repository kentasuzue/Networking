# Task: Create some functions for a simplified BGP router
#   Specifically, the withdraw, update, and next_hop functions of the Router
#   The class Route will be used.
# 
#   withdraw(rt) - rt is type Route. If a simplified BGP router gets this message, it will   
#


class Route:
    # A prefix is in form 
    neighbor = ""  # The router that send this router - will be a.b.c.d
    prefix = ""    # The IP address portion of a prefix - will be a.b.c.d
    prefix_len = 0 # The length portion of a prefix - will be an integer
    path = []      # the AS path - list of integers

    def __init__(self, neigh, p, plen, path):
        self.neighbor = neigh
        self.prefix = p
        self.prefix_len = plen
        self.path = path 

    # convert Route to a String    
    def __str__(self):
        return self.prefix+"/"+str(self.prefix_len)+"- ASPATH: " + str(self.path)+", neigh: "+self.neighbor

    # Get the prefix in the a.b.c.d/x format
    def pfx_str(self):
        return self.prefix+"/"+str(self.prefix_len)


# Implement the following functions:
#  update - the router received a route advertisement (which can be a new one, or an update
#         - the function needs to store the route in the RIB
#  withdraw - the router received a route withdraw message
#          - the function needs to delete the route in the RIB
#  nexthop - given ipaddr in a.b.c.d format as a string (e.g., "10.1.2.3"), perform a longest prefix match in the RIB
#          - Select the best route among multiple routes for that prefix by path length.  
#          - if same length, return either

class Router:
    # You can use a different data structure
    # dictionary with key of the prefix, value a list of Route
    # example: rib["10.0.0.0/24"] = [Route("1.1.1.1", "10.0.0.0", 24, [1,2,3]), 
    #                                Route("2.2.2.2", "10.0.0.0", 24, [10,20])]
    #          rib["10.0.0.0/22"] = [Route("3.3.3.3", "10.0.0.0", 22, [33,44,55,66]]
    rib = {} 

    # If you use the same data structure for the rib, this will print it
    def printRIB(self):
        for pfx in self.rib.keys():
            for route in self.rib[pfx]:
                print(route) 

    # helper function added by me
    # assumes rib has at least one entry for the prefix
    # if the parameter Route is matched by 
    # a rib Route with the same neighbor, prefix, and prefix_len (but the AS path not considered)
    # then return the list index with the matching rib Route
    # for the list that is the rib dict value for the rib dict key rt.pfx_str(), 
    # rt being the function parameter 
    def findRouteRIB(self, rt: Route):
        for index, route in enumerate(self.rib[rt.pfx_str()]):
            # print("rt = ", rt, "route = ", route)
            if rt.neighbor == route.neighbor and \
                rt.prefix == route.prefix and \
                rt.prefix_len == route.prefix_len:
                return index
        return -1

    # TASK
    def update(self, rt):

        # YOUR CODE HERE
        if rt.pfx_str() not in self.rib:
            self.rib[rt.pfx_str()] = [rt]
        else:
            index = self.findRouteRIB(rt)
            # index == -1 if the RIB dict entry with dict key of the route prefix (rt.pfx_str())
            # has a dict value of a route list 
            # that has no route with a matching neighobor, prefix, and prefix length (as path not considered)
            if index != -1:
                self.rib[rt.pfx_str()][index] = rt
            else:
                self.rib[rt.pfx_str()].append(rt)
        return



    # TASK    
    def withdraw(self, rt):

        # YOUR CODE HERE
        # if rib dict has no dict key equal to the prefix, then there's no Route to withdraw
        if rt.pfx_str() in self.rib.keys():
            index = self.findRouteRIB(rt)
            # index == -1 if the RIB dict entry with dict key of the route prefix (rt.pfx_str())
            # has a dict value of a route list 
            # that has no route with a matching neighobor, prefix, and prefix length
            if index != -1:
                if self.rib[rt.pfx_str()][index].path == rt.path:
                    del(self.rib[rt.pfx_str()][index])
                # if the RIB dict entry with dict key of the route prefix (rt.pfx_str())
                # has a dict value of an empty route list
                # then delete the dict key with the route prefix (rt.pfx_str()) from the RIB dict 
                if len(self.rib[rt.pfx_str()]) == 0:
                    del(self.rib[rt.pfx_str()])

        return 
    
    def convertToBinaryString(self, ip):
        vals = ip.split(".")
        a = format(int(vals[0]), 'b').rjust(8, '0')
        b = format(int(vals[1]), 'b').rjust(8, '0')
        c = format(int(vals[2]), 'b').rjust(8, '0')
        d = format(int(vals[3]), 'b').rjust(8, '0')
        return a+b+c+d



    # ipaddr in a.b.c.d format
    # find longest prefix that matches
    # then find shortest path of routes for that prefix
    def next_hop(self, ipaddr):
        retval = None

        # YOUR CODE HERE
        # print(self.convertToBinaryString(ipaddr))
        # initialize longest_matching_prefix_len to 0 
        # since any subseuent match will replace it 
        longest_matching_prefix_len = 0
        longest_matching_prefix = None
        for prefix in self.rib:
            # assumes rib keys "prefix_ip/prefix_len"
            prefix_ip, prefix_len = prefix.split('/')
            # print(prefix, prefix_ip, prefix_len)
            prefix_len = int(prefix_len)
            # if the first prefix_len bits of the IP address match, 
            # then there's a prefix match 
            if self.convertToBinaryString(prefix_ip)[:prefix_len] == \
                self.convertToBinaryString(ipaddr)[:prefix_len]:
                # print("prefix match!")
                # replace if there's a longer prefix match
                if prefix_len > longest_matching_prefix_len:
                    longest_matching_prefix_len = prefix_len
                    longest_matching_prefix = prefix

        # print("longest_matching_prefix_len = ", longest_matching_prefix_len, \
            # "longest_matching_prefix = ", longest_matching_prefix)
        
        if longest_matching_prefix_len > 0:
            # initialize shortest_path_length to infinity
            # so that any AS path will replace it
            shortest_path_length = float('inf')
            shortest_route = None
            for route in self.rib[longest_matching_prefix]:
                # print("matching route: ", route)
                if len(route.path) < shortest_path_length:
                    shortest_path_length = len(route.path)
                    shortest_route = route
        
            # print("shortest_route = ", shortest_route, "shortest_path_length = ", shortest_path_length)
            # the return value is the neighbor field of the saved path
            # that was saved while finding the shortest path in the paths that are the list dict value
            # of the rib dict key with the longest matching prefix
            retval = shortest_route.neighbor
        return retval




def test_cases():
    rtr = Router()

    #Test that withdrawing a non-existant route works
    rtr.withdraw (Route("1.1.1.1", "10.0.0.0", 24, [3,4,5]))

    #Test updates work - same prefix, two neighbors
    rtr.update (Route("1.1.1.1", "10.0.0.0", 24, [3,4,5]))
    # print("RIB") # I added
    # rtr.printRIB() # I added
    rtr.update (Route("2.2.2.2", "10.0.0.0", 24, [1,2]))

    print("RIB") #
    rtr.printRIB() #

    #Test updates work - overwriting an existing route from a neighbor
    rtr.update (Route("2.2.2.2", "10.0.0.0", 24, [1, 22, 33, 44]))

    print("RIB") #
    rtr.printRIB() #

    #Test updates work - an overlapping prefix (this case, a shorter prefix)
    rtr.update (Route("2.2.2.2", "10.0.0.0", 22, [4,5,7,8]))

    #Test updates work - completely different prefix
    rtr.update (Route("2.2.2.2", "12.0.0.0", 16, [4,5]))
    rtr.update (Route("1.1.1.1", "12.0.0.0", 16, [1, 2, 30]))

    print("RIB") #
    rtr.printRIB() #

    # Should not return an ip
    nh = rtr.next_hop("10.2.0.13")
    assert nh == None

    # Should return an ip
    nh = rtr.next_hop("10.0.0.13")
    assert nh == "1.1.1.1"

    # Test withdraw - withdraw the route from 1.1.1.1 that we just matched
    rtr.withdraw (Route("1.1.1.1", "10.0.0.0", 24, [3,4,5]))

    # Should match something different
    nh = rtr.next_hop("10.0.0.13")
    assert nh == "2.2.2.2"

    # Re-announce - so, 1.1.1.1 would now be best route
    rtr.withdraw (Route("1.1.1.1", "10.0.0.0", 24, [3,4,5]))

    
    rtr.update (Route("2.2.2.2", "10.0.0.0", 22, [4,5,7,8]))
    # Should match 10.0.0.0/22 (next hop 2.2.2.2) but not 10.0.0.0/24 (next hop 1.1.1.1)
    nh = rtr.next_hop("10.0.1.77")
    assert nh == "2.2.2.2"

    # Test a different prefix
    nh = rtr.next_hop("12.0.12.0")
    assert nh == "2.2.2.2"

    rtr.update (Route("1.1.1.1", "20.0.0.0", 16, [4,5,7,8]))
    rtr.update (Route("2.2.2.2", "20.0.0.0", 16, [44,55]))
    nh = rtr.next_hop("20.0.12.0")
    assert nh == "2.2.2.2"

    rtr.update (Route("1.1.1.1", "20.0.12.0", 24, [44,55,66,77,88]))
    nh = rtr.next_hop("20.0.12.0")
    assert nh == "1.1.1.1"


    # Remember to delete the entry from the RIB, not just removing the specific route
    # That is, when you withdraw, remove the route for the prefix, and if there are 0 routes, remove the prefix from the RIB
    rtr.withdraw(Route("1.1.1.1", "20.0.12.0", 24, [44,55,66,77,88]))
    nh = rtr.next_hop("20.0.12.0")
    assert nh == "2.2.2.2"








if __name__ == "__main__":
    test_cases()
    

