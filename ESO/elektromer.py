import socket
import time

class elektromer:
    def __init__(self, price, time, sources, consumers, grid_state="A"):#consumers is [[wattage,priority,state_on_off,state_on_off_intent, name],[],[]]
        self.price=price                                #sources[0] is grid budget
        self.time=time
        self.sources=sources
        self.consumers=consumers
        self.grid_state=grid_state
        self.prev_grid_state=self.grid_state
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
        #print("Power Budget " + str(self.power_budget))
        #print("Consumer needs " + str(self.consumer_needs))
    def decide(self):
        print("Grid state: " + str(self.grid_state))
        while(self.consumer_needs>self.power_budget):
            for p in range(8,0,-1):
                if(self.consumer_needs>self.power_budget):
                    for i in self.consumers:
                        if(i[0]>self.power_budget):
                            i[2]=0
                        if(i[1]==p):
                            i[2]=0#power off
                #print("Consumers after power off: " + str(self.consumers))
                self.calculate_power_budget()
        
        if(self.prev_grid_state>self.grid_state):
            print("Grid state got better!")
            for p in range(1,9):
                if(self.consumer_needs<self.power_budget):
                    for i in self.consumers:
                        if(i[1]==p and self.consumer_needs+i[0]<self.power_budget):
                            if(i[3]):
                                i[2]=1
                        self.calculate_power_budget()
                       


        self.prev_grid_state=self.grid_state

        
        print("After Decision: " + str(self.consumers))
    def tick(self):
        self.grid_state_adjust()
        self.calculate_power_budget()
        self.decide()
        self.send_to_esp()

    def send_to_esp(self):
        HOST = "192.168.88.253"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server

        data=str(consumers[0][2]) + str(consumers[1][2]) + str(consumers[2][2]) + str(consumers[3][2])

        print("Data to send:" + str(data))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(data.encode("ascii"))
            print(f"Sent string")
            #data = s.recv(1024)

        #print(f"Received {data!r}")


if __name__ == "__main__":
    consumers=[[1000,2,1,1,"Prahosmuka4ka"],[5000, 5, 1, 1, "Kalorifer"],[3200, 3, 1, 1, "Klimatik"],[500, 1, 1, 1, "Small electronics" ]]#consumers is [[wattage,priority,state_on_off,state_on_off_intent, name]
    sources=[15000]#just power grid
    
    elektromer1 = elektromer(20,20,sources, consumers)
    elektromer1.grid_state="C"
    elektromer1.tick()
    time.sleep(1)
    elektromer1.grid_state="C"
    #elektromer1 = elektromer(20,20,sources, consumers, grid_state)
    elektromer1.tick()









