# Per convertire ogni elemento di count in percentuale
def count_total_general(array):
    count = 0
    for value in array.values():
        for sentiment in value.values():
            count += sentiment
    
    return count

def count_total_months(array):
    count = 0
    print(array)
    for value in array.values():
        for sentiment in value:
            count += sentiment
    
    return count