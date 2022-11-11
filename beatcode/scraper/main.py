import json
import leetcode


CONFIG = leetcode.Configuration()
CONFIG.api_key["Referer"] = "https://leetcode.com"
CONFIG.debug = False
API_INSTANCE = leetcode.DefaultApi(leetcode.ApiClient(CONFIG))


def get_problem_info(problem_name):
    """
    :param problem_name: problem name slug associated with problem (i.e. N Queens => "n-queens")

    returns information related to problem such as the difficulty and categories
    ex. {'difficulty': 'Hard', 'categories': ['Array', 'Backtracking']}
    """
    graphql_query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
                title
                titleSlug
                difficulty
                likes
                dislikes
                isLiked
                categoryTitle
            topicTags {
                name
                slug
            }
            status
        }
    }
    """
    graphql_request = leetcode.GraphqlQuery(
        query=graphql_query,
        variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=problem_name),
        operation_name='questionData',
    )
    try:
        res = API_INSTANCE.graphql_post(body=graphql_request).data.question
    except KeyError:
        return None

    # query res for the information we need
    problem_info = {
        'difficulty': res.difficulty,
        'categories': [topic.name for topic in res.topic_tags]
    }

    return problem_info
