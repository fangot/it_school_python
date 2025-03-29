class Animal:
    def __init__(self, name, breed, count_tail, count_ears):
        self.name = name
        self.breed = breed
        self.count_tail = count_tail
        self.count_ears = count_ears

    def run(self, speed):
        print(str(self.name) + " движется со скоростью " + str(speed))
