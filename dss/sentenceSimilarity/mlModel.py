import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import joblib

crime_sen=pd.read_csv(r"C:\Users\ankit\OneDrive\Documents\crime1.csv")
# calamity_sen=pd.read_csv(r"C:\Users\ankit\OneDrive\Desktop\dss_data\calamity_final.csv")
# epidemic_sen=pd.read_csv(r"C:\Users\ankit\OneDrive\Desktop\dss_data\epidemic_final.csv")
# publicGathering_sen=pd.read_csv(r"C:\Users\ankit\OneDrive\Desktop\dss_data\unique_sen_public_gathering.csv")
# rally_sen=pd.read_csv(r"C:\Users\ankit\OneDrive\Desktop\dss_data\rally_final.csv")
# print(len(calamity_sen))

model = SentenceTransformer('all-MiniLM-L6-v2')
crime_encoded_data = model.encode(crime_sen['lesson'].tolist())
# calamity_encoded_data = model.encode(calamity_sen['Lesson Learnt'].tolist())
# epidemic_encoded_data = model.encode(epidemic_sen['Lesson Learnt'].tolist())
# publicGathering_encoded_data = model.encode(publicGathering_sen.Lesson.tolist())
# rally_encoded_data = model.encode(rally_sen['Lesson Learnt'].tolist())



filename= 'saved_model.sav'
saved_model=joblib.dump(model,filename)

faiss.normalize_L2(crime_encoded_data)
crime_index_bert = faiss.IndexIDMap(faiss.IndexFlatIP(384))
crime_index_bert.add_with_ids(crime_encoded_data, np.array(range(0, len(crime_sen))))
faiss.write_index(crime_index_bert, 'crime_data.bin')

# faiss.normalize_L2(calamity_encoded_data)
# calamity_index_bert = faiss.IndexIDMap(faiss.IndexFlatIP(384))
# calamity_index_bert.add_with_ids(calamity_encoded_data, np.array(range(0, len(calamity_sen))))
# faiss.write_index(calamity_index_bert, 'calamity_data.bin')

# faiss.normalize_L2(epidemic_encoded_data)
# epidemic_index_bert = faiss.IndexIDMap(faiss.IndexFlatIP(384))
# epidemic_index_bert.add_with_ids(epidemic_encoded_data, np.array(range(0, len(epidemic_sen))))
# faiss.write_index(epidemic_index_bert, 'epidemic_data.bin')

# faiss.normalize_L2(publicGathering_encoded_data)
# publicGathering_index_bert = faiss.IndexIDMap(faiss.IndexFlatIP(384))
# publicGathering_index_bert.add_with_ids(publicGathering_encoded_data, np.array(range(0, len(publicGathering_sen))))
# faiss.write_index(publicGathering_index_bert, 'publicGathering_data.bin')

# faiss.normalize_L2(rally_encoded_data)
# rally_index_bert = faiss.IndexIDMap(faiss.IndexFlatIP(384))
# rally_index_bert.add_with_ids(rally_encoded_data, np.array(range(0, len(rally_sen))))
# faiss.write_index(rally_index_bert, 'rally_data.bin')