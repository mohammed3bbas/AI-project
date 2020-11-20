class Requests:
    #Request ID, Pickup location, Delivery location, early ,late
    def __init__(self,id,pickup,delivery,early,late,delivered=False):
        self.id = id
        self.pickup = pickup
        self.delivery = delivery
        self.early = early
        self.late = late
        self.delivered=delivered
