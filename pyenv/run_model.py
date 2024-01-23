from getHands import Hands

class Queue:
    def __init__(self):
        self.hand = Hands()

    def run_queue(self, img):
        self.most_common.clear()
        try:
            letter, conf = self.hand.getHands(img)
            det = True
            conf = conf.item()
        except Exception as e:
            letter = ""
            conf = 0
            det = False
        
        return (letter, conf, det)

