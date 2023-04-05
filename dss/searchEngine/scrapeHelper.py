from keywords import result
from duckduckgo_search import ddg
import time



addon_keywords={"awards":['recognized awards site:.gov.in','recognized awards site:.niti.gov.in','recognized awards site:.nic.in'],'research':['research paper site:.sciencedirect.com','research paper site:.researchgate.com','research paper site:.scholar.google.com','research paper site:.niti.gov.in'],
                'educational':['prestigious university research site:.edu','prestigious university research site:.iitd.ac.in'],
                'implemented':['related program or scheme implemented by government site:.gov.in','related program or scheme implemented by government site:.un.org','related program or scheme implemented by government site:.usa.gov','related program or scheme implemented by government site:.niti.gov.in']
                }


def scrape(request):
    for q in result:
        for addon in addon_keywords:
            for regex in addon_keywords[addon]:
                query=q+" "+regex
                
                outputs = ddg(query, region='hi-in', safesearch='moderate', time='y',max_results=10,page=1)
                print(query)
                if outputs is None:
                    print("No result")
                else:
                    print("results")
                    # for res in outputs:
                    #     print(res)
                time.sleep(2)
    return "success"

scrape("abx")