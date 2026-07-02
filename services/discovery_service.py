
from services.scoring_service import score

def discover():
    ideas=[
        {"title":"AI Compliance Copilot","revenue":95,"pain":92,"competition":70,"ai":100,"solo":75,"trend":90,
         "description":"Automate compliance workflows for SMBs."},
        {"title":"AI Proposal Writer","revenue":90,"pain":88,"competition":65,"ai":95,"solo":90,"trend":85,
         "description":"Generate proposals and RFP responses."},
        {"title":"AI Vendor Risk Scanner","revenue":85,"pain":91,"competition":60,"ai":90,"solo":80,"trend":82,
         "description":"Assess vendor risk using AI."},
    ]
    for i in ideas:
        i["score"]=score(i)
    return sorted(ideas,key=lambda x:x["score"],reverse=True)
