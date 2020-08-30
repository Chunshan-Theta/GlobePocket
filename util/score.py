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
        most_distence = (len(thresholds)/2)
        stage = 0
        for t in thresholds:
            if val < t:
                temp_distence = abs(stage-center)
                return 1-temp_distence/most_distence
            stage += 1
        temp_distence = abs(stage - center)
        return 1-temp_distence/most_distence



    @staticmethod
    def worce_cause(obj:dict):
        def sort_by_key(obj: dict):
            return [(k, obj[k]) for k in sorted(obj.keys())]
        source_list = {}
        for k,v in obj.items():
            got_score = v['score']
            source_val = v['source_val']
            source_list[got_score]= (k,source_val)

        return sort_by_key(source_list)



    def computer(self,place_detail:dict,cause_detail_option=False):
        score = 0
        items_detail_score = {}
        for k,v in place_detail.items():
            if k in self.items.keys():
                thresholds = self.items[k][1]
                weight = self.items[k][0]
                func_computer = self.items[k][2]

                temp_score = (weight*func_computer(thresholds=thresholds,val=v))
                weight_temp_score = (weight*temp_score)
                items_detail_score.update({
                    k: {
                        'source_val':v,
                        'score':temp_score,
                        'final_score':weight_temp_score,
                        'weight':weight
                    }
                })
                score += temp_score
                #print(k,temp_score,weight_temp_score)
        return score if not cause_detail_option else {
            'score':score,
            'detail':items_detail_score,
            'worse': self.worce_cause(items_detail_score)
        }

example_place_detail = {
    "rain": 0.9,
    "see": 30,
    "temp": 18
}
example_board =ScoreBoard(items={
    "rain": (0.1, [0.3, 0.6, 0.8], ScoreBoard.lesser_threshold),
    "see": (0.5, [10, 20, 25], ScoreBoard.greater_threshold),
    "temp": (0.4, [1, 8, 16, 24, 31, 35], ScoreBoard.in_threshold)
})
default_board =ScoreBoard(items={
    "pop": (0.2, [0.3, 0.6, 0.8], ScoreBoard.lesser_threshold),
    "rain": (0.3, [3,10,25,50,100,150,200,250], ScoreBoard.lesser_threshold),
    "uvi": (0.1, [3, 5, 7, 10], ScoreBoard.lesser_threshold),
    "temp": (0.4, [1, 8, 16, 24, 31, 35], ScoreBoard.in_threshold)
})
#print(example_board.computer(example_place_detail,cause_detail_option=True))
