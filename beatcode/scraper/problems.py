import requests


def get_problem_info(problem_name):
    """
    :param problem_name: problem name slug associated with problem (i.e. N Queens => "n-queens")

    returns information related to problem such as the difficulty and categories
    ex. {'difficulty': 'Hard', 'categories': ['Array', 'Backtracking']}
    """
    graphql_query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        problemsetQuestionList: questionList(
            categorySlug: $categorySlug
            limit: $limit
            skip: $skip
            filters: $filters
        ) {
            total: totalNum
            questions: data {
                difficulty
                status
                title
                titleSlug
                topicTags {
                    name
                    id
                    slug
                }
            }
        }
    }
    """
    graphql_variables = {'categorySlug': '', 'limit': 1, 'skip': 0, 'filters': {'searchKeywords': problem_name}}
    res = requests.post(
        url='https://leetcode.com/graphql/',
        json={'query': graphql_query, 'variables': graphql_variables}
    ).json()
    if 'errors' not in res:
        problem_data = res['data']['problemsetQuestionList']['questions'][0]

        # query res for the information we need
        problem_info = {
            'title_slug': problem_data['titleSlug'],
            'difficulty': problem_data['difficulty'],
            'categories': [topic['name'] for topic in problem_data['topicTags']]
        }
        return problem_info
    return -1
