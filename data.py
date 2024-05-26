class Data:
    def __init__(self):
        self.stack_sizes = []
        self.stack_size_labels = {}
        self.highlighted_hands = {}
        self.current_stack_size = None
        self.current_label = None

    def setCurrentStackSize(self, text):
        self.current_stack_size = text

    def getCurrentStackSize(self):
        return self.current_stack_size

    def addStackSize(self, text):
        self.stack_sizes.append(text)
        self.stack_size_labels[text] = []
        self.highlighted_hands[text] = {}

    def removeStackSize(self, text):
        self.stack_sizes.remove(text)
        del self.stack_size_labels[text]
        del self.highlighted_hands[text]

    def addLabel(self, text):
        self.stack_size_labels[self.current_stack_size].append(text)
        self.highlighted_hands[self.current_stack_size][text] = ''

    def removeLabel(self, text):
        self.stack_size_labels[self.current_stack_size].remove(text)
        del self.highlighted_hands[self.current_stack_size][text]

    def getLabels(self):
        return self.stack_size_labels.get(self.current_stack_size, [])

    def getCurrentLabel(self):
        return self.current_label

    def setLabelColor(self, label, color):
        self.highlighted_hands[self.current_stack_size][label] = color

    def getHighlightedHands(self):
        return self.highlighted_hands