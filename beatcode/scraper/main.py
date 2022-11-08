import leetcode
#from .auth import Authentication

#authhelper = Authentication(username="", password="")
#cookies = authhelper.get_auth_info()

# Get the next two values from your browser cookies

## leetcode_session = cookies.get
##


leetcode_session = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMzIxMjc0MiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMmY1MmQ5ZGM3MjhmNGQwNDdmZmM1MDY4MDIwNzQ3MzRkOWMzZWI4ZiIsImlkIjozMjEyNzQyLCJlbWFpbCI6ImxvdWlzZXRhbmc4QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoibG91aXNldGFuZzgiLCJ1c2VyX3NsdWciOiJsb3Vpc2V0YW5nOCIsImF2YXRhciI6Imh0dHBzOi8vczMtdXMtd2VzdC0xLmFtYXpvbmF3cy5jb20vczMtbGMtdXBsb2FkL2Fzc2V0cy9kZWZhdWx0X2F2YXRhci5qcGciLCJyZWZyZXNoZWRfYXQiOjE2Njc2NzY1NzYsImlwIjoiMTUyLjMuNDMuNDkiLCJpZGVudGl0eSI6Ijc5MmRlNTFlNGQ1YmU1MmEzNWY1NWYzNTcwMTkzZmMzIiwic2Vzc2lvbl9pZCI6MzA0MzYxNjEsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.9z0OkW3qP_-a5phVyrT_Y0UEL3C32fAewoWUA8v9klM"
csrf_token = "LKhTQMKJbAXtklynq8xvGX8lJEfSV3SHXyjM0L6GKxjESjGROAbtDff5vn0dyUpq"

# Experimental: Or CSRF token can be obtained automatically
import leetcode.auth
csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

### Calculate % of problems solved by topic 

api_response = api_instance.api_problems_topic_get(topic="algorithms")

slug_to_solved_status = {
    pair.stat.question__title_slug: True if pair.status == "ac" else False
    for pair in api_response.stat_status_pairs
}

import time

from collections import Counter


topic_to_accepted = Counter()
topic_to_total = Counter()


# Take only the first 10 for test purposes
for slug in list(slug_to_solved_status.keys())[:10]:
    time.sleep(1)  # Leetcode has a rate limiter
    
    graphql_request = leetcode.GraphqlQuery(
        query="""
            query getQuestionDetail($titleSlug: String!) {
              question(titleSlug: $titleSlug) {
                topicTags {
                  name
                  slug
                }
              }
            }
        """,
        variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=slug),
        operation_name="getQuestionDetail",
    )

    api_response = api_instance.graphql_post(body=graphql_request)
    
    for topic in (tag.slug for tag in api_response.data.question.topic_tags):
        topic_to_accepted[topic] += int(slug_to_solved_status[slug])
        topic_to_total[topic] += 1
print(topic_to_total)

# print(
#     list(
#         sorted(
#             ((topic, accepted / topic_to_total[topic]) for topic, accepted in topic_to_accepted.items()),
#             key=lambda x: x[1]
#         )
#     )
# )