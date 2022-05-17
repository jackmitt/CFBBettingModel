import data_manipulation as dm
import pickle


with open("./csv_data/last_prior.pkl","rb") as inputFile:
    priors = pickle.load(inputFile)
print (priors)
