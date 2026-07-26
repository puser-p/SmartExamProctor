from detection.dataset_creator import DatasetCreator

dc = DatasetCreator()

images = dc.capture("101")

print(images)