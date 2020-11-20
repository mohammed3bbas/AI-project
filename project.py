import Request
from queue import Queue
def readLocations():
    "location 2d list/ 11 locations / location [4][4] central depo"
    f = open("locations-draft.txt", "r")
    lines = f.readlines()
    locations = []
    counter = 0
    for i in lines:
        locations.append(i.strip().split("\t"))
        counter += 1
    f.close()
    return locations
def readRequests():
    "creating a list of requests (objects) each object contain (Request ID, Pickup location, Delivery location, early ,late)"
    f = open("request-draft1.txt", "r")
    lines = f.readlines()
    requests = []
    counter = 0
    for i in lines:
        temp = i.strip().split(" ")
        requests.append(Request.Requests(temp[0], temp[1], temp[2], temp[3], temp[4]))
    f.close()
    return requests
def printRequestQueue(pickedRequestsQueue):
    s=""
    if len(pickedRequestsQueue)==0:
        return "empty"
    for i in pickedRequestsQueue:
        s+=" "+i.id
    return s

locations = readLocations() #all locarions
requests=readRequests() #all requests
pickedRequestsQueue = []
capacity =3
requests.sort(key=lambda x: x.late )
timer = 0
currentlocation  = 4
for i in requests: #moving on orderd requsts
    print("-------------------------")
    print("request id :"+str(i.id))
    print("Requests queue ", printRequestQueue(pickedRequestsQueue) )#pickedRequestsQueue)
    print("available requests: ",capacity)
    if (int(i.late)>timer): #aza msh late
        if i not in pickedRequestsQueue: #if we didn't pick the order
            if capacity !=0: #there available space for requests
                pickedRequestsQueue.append(i)
                capacity=capacity-1
                timer += int(locations[currentlocation][int(i.pickup)]) #pick the request
                print("pickup time: "+str(timer))
                timer += int(locations[int(i.pickup)][int(i.delivery)]) #diliver the request
                print("dilvered time : " +str(timer))
                currentlocation = int(i.delivery) #delivery location
                i.delivered = True
                deliverdReq=pickedRequestsQueue.pop(pickedRequestsQueue.index(i))
                capacity=capacity+1
            else:
                h=0
                #how should i do it ??? back fucking tracking !!!
                #i think i can do it by using a while loop and i can affect on the requests list
                #maybe by swaping it can be done
        else:
            timer += int(locations[int(currentlocation)][int(i.delivery)]) #already picked so dilver it
            print("dilvered time : " + str(timer))
            currentlocation = int(i.delivery)
            i.delivered = True
            deliverdReq=pickedRequestsQueue.pop(pickedRequestsQueue.index(i))
            capacity=capacity+1

        for j in requests: #if  dilevery location is pickup for other request
            if (j.pickup == deliverdReq.delivery and j.delivered==False and capacity!=0):
                pickedRequestsQueue.append(j)
                print("YEES for request "+str(j.id))
                capacity=capacity-1
    print("-------------------------")