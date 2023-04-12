from details.models.calamity import Calamity
from details.models.crime import Crime
from details.models.epidemic import Epidemic
from details.models.publicGathering import PublicGathering
from details.models.rally import Rally
from  sentenceSimilarity.models import crimeSen,calamitySen,epidemicSen,publicGatheringSen,rallySen
from rest_framework.parsers import JSONParser 
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


crime_sen=pd.read_csv(r"C:\Users\ankit\Downloads\DSS- Lesson Learned For Law and order  - Crime (1).csv")
calamity_sen=pd.read_csv(r"C:\Users\ankit\Downloads\DSS- Lesson Learned For Law and order  - Calamity (1).csv")
epidemic_sen=pd.read_csv(r"C:\Users\ankit\Downloads\DSS- Lesson Learned For Law and order  - Epidemic (1).csv")
publicGathering_sen=pd.read_csv(r"C:\Users\ankit\Downloads\DSS- Lesson Learned For Law and order  - Public Gathering (1).csv")
rally_sen=pd.read_csv(r"C:\Users\ankit\Downloads\DSS- Lesson Learned For Law and order  - Rally (2).csv")

    