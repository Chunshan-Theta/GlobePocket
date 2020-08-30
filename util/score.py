class ScoreBoard:
    def __init__(self,items:dict):
        self.items = items

    @staticmethod
    def greater_threshold(thresholds,val)-> float:
        level = 0
        for t in thresholds:
            if val > t:
                return 1-(level/len(thresholds))
            level+=1
        return 1-(level/len(thresholds))

    @staticmethod
    def lesser_threshold(thresholds,val)-> float:
        level = 0
        for t in thresholds:
            if val < t:
                return 1-(level/len(thresholds))
            level += 1
        return 1-(level/len(thresholds))

    @staticmethod
    def in_threshold(thresholds, val) -> float:
        center = len(thresholds)/2
        stage = 0
        for t in thresholds:
            if val < t:
                return 1-abs(stage-center)
            stage += 1

        return 1-abs(stage-center)

    def computer(self,place_detail:dict):
        score = 0
        for k,v in place_detail.items():
            if k in self.items.keys():
                thresholds = self.items[k][1]
                weight = self.items[k][0]
                func_computer = self.items[k][2]
                score += (weight*func_computer(thresholds=thresholds,val=v))
        return score

place_detail = {
    "rain": 0.9,
    "see": 30,
    "temp": 25
}
weather_board =ScoreBoard(items={
    "rain": (0.1, [0.3, 0.6, 0.8], ScoreBoard.lesser_threshold),
    "see": (0.5, [10, 20, 25], ScoreBoard.greater_threshold),
    "temp": (0.4, [0, 10, 30, 35], ScoreBoard.in_threshold)
})
print(weather_board.computer(place_detail))
