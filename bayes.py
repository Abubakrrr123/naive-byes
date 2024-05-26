import pandas as pd
import pprint
from functools import reduce


class Classifier:
    def __init__(self, filename=None, class_attribute=None):
        self.data = pd.read_csv(filename, sep=',', header=0)
        self.class_attribute = class_attribute
        #print("class attribute",self.class_attribute)
        self.class_probability = {}
        self.conditional_probabilities = {}
        self.test_data = None

    def calculate_class_prob(self):
            class_values = set(self.data[self.class_attribute])  # yes or no
            class_data = list(self.data[self.class_attribute])  #  yes| no|yes|no|yes|no
            for value in class_values:
                self.class_probability[value] = class_data.count(value) / len(class_data)
            print("Class Probabilities Values:", self.class_probability)

    def get_conditional_probability(self, attribute, attribute_value, class_value):
        data_attribute = list(self.data[attribute])  #  col attr data
        class_data = list(self.data[self.class_attribute])  #class data
        # print("class_data",class_data)  
        total = 1
        for i in range(len(data_attribute)):
            # print("data_attribute",i)  
            if class_data[i] == class_value and data_attribute[i] == attribute_value:
                total += 1
        return total / class_data.count(class_value)

    def calculate_conditional_probabilities(self, test_data):
        self.conditional_probabilities = {}
        for class_value in self.class_probability:
            # print("class_value",class_value)  
            self.conditional_probabilities[class_value] = {}
            for attribute, attribute_value in test_data.items():
                # print("class_value",class_value)  
                self.conditional_probabilities[class_value][attribute_value] = self.get_conditional_probability(attribute, attribute_value, class_value)
        print("\nCalculated Conditional Probabilities:\n")
        pprint.pprint(self.conditional_probabilities)

    def classify(self):
        print("Result:")
        for class_value, probabilities in self.conditional_probabilities.items():
            result = reduce(lambda x, y: x * y, probabilities.values()) * self.class_probability[class_value]
            print(class_value, " ==> ", result)

if __name__ == "__main__":
    c = Classifier(filename="small_dataset.csv", class_attribute="Play")
    c.calculate_class_prob()
    c.test_data = {"Outlook": 'Rainy', "Temp": "Mild", "Humidity": 'Normal', "Windy": 't'}
    c.calculate_conditional_probabilities(c.test_data)
    c.classify()
