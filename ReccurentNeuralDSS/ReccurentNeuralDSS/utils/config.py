DATADIR = "../Imagesfiles"
#Training = ["CB55/img/training", "CS18/img/training","CS863/img/training"]
#Result = ["CB55/pixel-level-gt/training", "CS18/pixel-level-gt/training", "CS863/pixel-level-gt/training"]
Training = ["DeansTestmap/img/training"]
Result = ["DeansTestmap/pixel-level-gt/training"]
Xsize = 32
Ysize= 32
AmountOfEpochs = 5
batchSize = 20
validationSplit = 0.2
Picklefiles = "../output"


LoadTestPickle = "combined.pickle"
SaveTestImage = True
WhereTosaveTestImage = "here"
NameOfTestImage = "testimage"