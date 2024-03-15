class elektromer:
    def __init__(self, price, time, sources, consumers):#consumers is [[wattage,priority,state_on_off,state_on_off_intent, name],[],[]]
        self.price=price                                #sources[0] is grid budget
        self.time=time
        self.sources=sources
        self.consumers=consumers
        self.grid_state="C"
    def grid_state_adjust(self):
        if(self.grid_state=="A"):
            self.sources[0]=15000
        if(self.grid_state=="B"):
            self.sources[0]=10000
        if(self.grid_state=="C"):
            self.sources[0]=6000
        if(self.grid_state=="D"):
            self.sources[0]=3000
        if(self.grid_state=="E"):
            self.sources[0]=1500
        if(self.grid_state=="F"):
            self.sources[0]=750


    def calculate_power_budget(self):
        s=0
        for i in self.sources:
            s+=i
        c=0
        for i in self.consumers:
            if(i[2]):#if it's on
                c+=i[0]#add to consumers

        self.power_budget=s
        self.consumer_needs=c
        self.margin_watts=s-c
        self.margin_percentage=((s-c)/s)*100
        print("Power Budget " + str(self.power_budget))
        print("Consumer needs " + str(self.consumer_needs))
    def decide(self):
        while(self.consumer_needs>self.power_budget):
            for p in range(8,0,-1):
                if(self.consumer_needs>self.power_budget):
                    for i in self.consumers:
                        if(i[1]==p):
                            i[2]=0#power off
                print("Consumers after power off: " + str(self.consumers))
                self.calculate_power_budget()
                
        print("After Decision: " + str(self.consumers))
    def tick(self):
        self.grid_state_adjust()
        self.calculate_power_budget()
        self.decide()



if __name__ == "__main__":
    consumers=[[1000,2,1,1,"Prahosmuka4ka"],[5000, 5, 1, 1, "Kalorifer"],[3200, 3, 1, 1, "Klimatik"],[500, 1, 1, 1, "Small electronics" ]]#consumers is [[wattage,priority,state_on_off,state_on_off_intent, name]
    sources=[15000]#just power grid
    elektromer1 = elektromer(20,20,sources, consumers)

    elektromer1.tick()







