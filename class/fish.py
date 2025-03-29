from animal import Animal

class Fish(Animal):
    def run(self, speed):
        print(str(self.name) + " плывет со скоростью " + str(speed))
