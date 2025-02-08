import re
from datetime import datetime

class Score_Cookies:
    
    def __init__(self):
        pass

    async def evaluate_cookie_security(self, cookie):
        score = 0
        max_score = 6  # 6 parameters to evaluate
        score = 0
        session_name  = cookie[0][0] 
        session_value = cookie[0][1]
        domain = cookie[0][2]
        path = cookie[0][3]
        expires = cookie[0][4]
        secure = cookie[0][5]
        feedback = []

        # Session Name - Should not be empty or generic
        if not session_name or session_name == 'session':
            feedback.append("Session Name is empty or too generic.")
        else:
            score += 1

        # Session ID - Should not be simple (For simplicity, we will use regex)
        if not session_value or re.match(r'^[a-zA-Z0-9]{8,}$', session_value) is None:
            feedback.append("Session ID is too simple or invalid.")
        else:
            score += 1

        # Expires - Should not be far-off date or missing
        if not expires or datetime.strptime(expires, "%a, %d-%b-%Y %H:%M:%S GMT") < datetime.now():
            feedback.append("Expires is not set properly or has already passed.")
        else:
            score += 1

        # Path - Should not be overly broad (must be specific like `/app` or `/secure`)
        if path == '/' or not path:
            feedback.append("Path is too broad or not set.")
        else:
            score += 1

        # Domain - Should be a specific domain, not localhost or too general
        if not domain or domain in ['localhost', '127.0.0.1', '']:
            feedback.append("Domain is too generic or localhost.")
        else:
            score += 1

        # Secure - Should be True
        if secure != True:
            feedback.append("Secure flag is not set.")
        else:
            score += 1

        # Calculate the percentage score
        percentage_score = (score / max_score) * 100

        return percentage_score, feedback


    # Example cookie data for evaluation
    cookie = {
        'Session Name': 'userSession',
        'Session ID': 'abcd1234',
        'Expires': 'Wed, 10-Feb-2025 12:00:00 GMT',
        'Path': '/app',
        'Domain': 'example.com',
        'Secure': True
    }

    # Calculate and display the results
    percentage_score, issues = evaluate_cookie_security(cookie)

    print(f"Security Score: {percentage_score:.2f}%")
    if issues:
        print("Issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues found.")
