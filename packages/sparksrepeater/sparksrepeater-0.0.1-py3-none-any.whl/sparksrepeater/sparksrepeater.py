class sparksrepeater():

    def __init__(self,starter,speed):

        self.starter = starter
        self.speed = speed

    def repeat(self):
        while self.speed > 0:
            print(self.starter*int(self.speed))
            continue

    
