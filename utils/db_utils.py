from file_upload.models import Picture, Tag, AlgorithmOne, AlgorithmTwo

# Returns list of algorithm objects given its picture *Note the list should contain
# Only one value
def retreive_algorithm_object(Picture):
    return {
        "AlgorithmOne": AlgorithmOne.objects.filter(picture=Picture),
        "AlgorithmTwo": AlgorithmTwo.objects.filter(picture=Picture)
    }[Picture.algorithmType]
