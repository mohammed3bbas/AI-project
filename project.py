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
    f = open("request-draft2.txt", "r")
    lines = f.readlines()
    requests = []
    counter = 0
    for i in lines:
        temp = i.strip().split(" ")
        requests.append(Request.Requests(temp[0], temp[1], temp[2], temp[3], temp[4]))
    f.close()
    return requests


def printRequestQueue(pickedRequestsQueue):
    s = ""
    if len(pickedRequestsQueue) == 0:
        return "empty"
    for i in pickedRequestsQueue:
        s += " " + i.id
    return s


def swap(list, pos1, pos2):
    temp = list
    temp[pos1], list[pos2] = temp[pos2], list[pos1]
    return temp


def backtrack(requests,index,currentlocation):
    "find another path: since the problem CSP we can't go back in path so we will find new node to serve "
    "depending on new heuristic, the closest node from the last served node will be served next "
    start = index - 1
    # print("-----")
    # print(currentlocation)
    # print("wewww")
    i=findClosestRequest(requests,currentlocation,index)
    if (i ==None):
        return None
    nearest=requests.pop(i)
    requests.insert(index,nearest)
    return requests

    # return None

def findClosestRequest(requests,currentlocation,index):
    closestIndex=index
    closest = int(locations[currentlocation][int(requests[index].pickup)])
    myTime =closest
    # print(closest)
    for i in range(index,len(requests)):
        # print("distances ")
        # print(locations[currentlocation][int(requests[i].pickup)])
        # print("---------------")
        if int(locations[currentlocation][int(requests[i].pickup)]) < closest:
            closestIndex = i
            closest=int(requests[i].pickup)
    # print(closest)
    if(myTime==closest):
        return None
    return closestIndex

def forwardChecking(requests, index, timer):
    "here we check if the current time make any problem for any request"
    for i in range(index, len(requests)):
        request = requests[i]
        if int(request.late) < timer:
            return True, request, i
    return False, None, None


def MRV(index, capacity, timer, currentlocation, pickedRequestsQueue, done, locations,requests):
    # moving on orderd requsts
    i = requests[index]
    print("-------------------------")
    print("request id :" + str(i.id))
    print("Requests queue ", printRequestQueue(pickedRequestsQueue))  # pickedRequestsQueue)
    print("available requests: ", capacity)
    # print(str(i.late) + " > " + str(
    #     timer + int(locations[currentlocation][int(i.pickup)]) + int(locations[int(i.pickup)][int(i.delivery)])))
    # if (int(i.late) > (
    #         timer + int(locations[currentlocation][int(i.pickup)]) + int(locations[int(i.pickup)][int(i.delivery)]))):
        # aza lma awslo msh late
    if i not in pickedRequestsQueue:  # if we didn't pick the order

        flag, temp, tempIndex = \
            forwardChecking(requests, index, timer + int(locations[currentlocation][int(i.pickup)]) + int(locations[int(i.pickup)][int(i.delivery)]))

        if flag == False:  # delivering the request will not cause any problem
            Inflag = False
            prevTime = timer
            pickedRequestsQueue.append(i)
            capacity = capacity - 1
            timer += int(locations[currentlocation][int(i.pickup)])  # pick the request
            print("pickup time: " + str(timer))
            if (timer < int(i.early)):
                print("wait for " + (int(i.early) - timer))
                timer += (int(i.early) - timer)  # timer now equal to early  so i can deliver it
            timer += int(locations[int(i.pickup)][int(i.delivery)])  # diliver the request
            print("dilvered time : " + str(timer))
            currentlocation = int(i.delivery)  # delivery location
            i.delivered = True
            deliverdReq = pickedRequestsQueue.pop(pickedRequestsQueue.index(i))
            done.append(deliverdReq)  # already done
            capacity = capacity + 1
            index += 1
            deliverdReq, capacity, pickedRequestsQueue = \
                moreRequestsOnThePickup(deliverdReq, requests, capacity, pickedRequestsQueue)
            deliverdReq, capacity, pickedRequestsQueue = \
                moreRequestsOnTheDelivery(deliverdReq, requests, capacity, pickedRequestsQueue)
            return (index, capacity, timer, currentlocation, pickedRequestsQueue, done, deliverdReq)
        if(flag == True):
            print("this is my current location "+str(currentlocation))
            requests=backtrack(requests,index,currentlocation)
            if requests==None:
                return (None,capacity, timer, currentlocation, pickedRequestsQueue, done, None)
            return (index, capacity, timer, currentlocation, pickedRequestsQueue, done, None)



    else:  # if already picked

        flag, temp, tempIndex = \
            forwardChecking(requests, index, timer + int(locations[currentlocation][int(i.pickup)]) + int(
                locations[int(i.pickup)][int(i.delivery)]))

    if (flag == False):
        Inflag = True
        prevTime = timer

        timer += int(locations[int(currentlocation)][int(i.delivery)])  # already picked so dilver it

        print("dilvered time : " + str(timer))

        currentlocation = int(i.delivery)

        i.delivered = True

        deliverdReq = pickedRequestsQueue.pop(pickedRequestsQueue.index(i))

        done.append(deliverdReq)  # already done

        capacity = capacity + 1

        index += 1

        deliverdReq, capacity, pickedRequestsQueue = \
            moreRequestsOnTheDelivery(deliverdReq, requests, capacity, pickedRequestsQueue)

        return (index, capacity, timer, currentlocation, pickedRequestsQueue, done, deliverdReq)

    # else:
    #     index = index + 1
    #     return (index, capacity, timer, currentlocation, pickedRequestsQueue, done, None)
        # backTrack
        # if the request is late backtracking !
        # swap the request with the last done request
        # requests[index-1].delivered=False # sarat not serverd
        # swap(requests,index,index-1) #3mlt swaping
        # timer = prevTime # timer mashi sa7
        # index =index-1
    # flag, temp, tempIndex = forwardChecking(requests, index, timer)
    # if(flag==True):
    #     backtrack(temp,done,[])

def moreRequestsOnTheDelivery(deliverdReq,requests,capacity,pickedRequestsQueue):
    if (deliverdReq != None):
        for j in requests:  # if  dilevery location is pickup for other request
            if (j.pickup == deliverdReq.delivery and j.delivered == False and capacity != 1 and (j not in pickedRequestsQueue)):
                # why capacity != 1
                # 3shan ydal fe wasa3 ll jayat bl tare2 :D
                pickedRequestsQueue.append(j)
                print("from delivery location YEES for request " + str(j.id))
                capacity = capacity - 1
        # print("-------------------------")
    return (deliverdReq, capacity, pickedRequestsQueue)

def moreRequestsOnThePickup(deliverdReq,requests,capacity,pickedRequestsQueue):
    if (deliverdReq != None):
        for j in requests:  # if  pickup location is pickup for other request
            if (j.pickup == deliverdReq.pickup and j.delivered == False and capacity != 1 and (j not in pickedRequestsQueue)):
                # why capacity != 1
                # 3shan ydal fe wasa3 ll jayat bl tare2 :D
                pickedRequestsQueue.append(j)
                print("from pick up location YEES for request " + str(j.id))
                capacity = capacity - 1
        # print("-------------------------")
    return (deliverdReq,capacity,pickedRequestsQueue)

def printRequests(requests,message):
    print(message)
    for i in requests:
        print("Request id : "+i.id)

locations = readLocations()  # all locarions
requests = readRequests()  # all requests
pickedRequestsQueue = []  # the requestes on the car
capacity = 3  # car capacity
requests.sort(key=lambda x: x.late)  # order requests on late time
timer = 0
currentlocation = 4  # central depp
index = 0
done = []  # deliverd requests
prevTime = 0
printRequests(requests,"request orderd by late time")
# MRV algorithm
while index < len(requests):
    index, capacity, timer, currentlocation, pickedRequestsQueue, done, deliverdReq = \
        MRV(index, capacity, timer, currentlocation, pickedRequestsQueue, done, locations,requests)
    if index==None:
        print("NO SOLUOTION")
        # print("--------Deliverd requests--------")
        printRequests(done,"--------Deliverd requests--------")
        break


