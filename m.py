import pickle

from train import Train

model = Train()
model.fit('anna-karenina.txt')

filename = 'text_model.pkl'

# Save model
pickle.dump(model, open(filename, 'wb'))

# Load model
loaded_model = pickle.load(open(filename, 'rb'))

print(loaded_model.gen_text('о', 13))
