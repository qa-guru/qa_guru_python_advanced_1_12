import allure

from models.starships import ListStarships, Starships
from tests.body import RESPONSE_BODY_405, RESPONSE_BODY_404


@allure.feature('Starships')
class TestStarships:
    @allure.story('Positive tests')
    class TestPositive:
        def test_get_all_starships(self, api_session):
            response = api_session.request(path='/starships/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            starships = ListStarships.model_validate(response.json())
            pass

        def test_get_nine_starship(self, api_session):
            response = api_session.request(path='/starships/9/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            starship = Starships.model_validate(response.json())
            assert starship.name == 'Death Star'

        def test_get_second_starship(self, api_session):
            response = api_session.request(path='/starships/2/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            starship = Starships.model_validate(response.json())
            assert starship.name == 'CR90 corvette'

        def test_search_starship(self, api_session):
            response = api_session.request(path='/starships/12/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            starship = Starships.model_validate(response.json())
            assert starship.name == 'X-wing'

    @allure.story('Negative tests')
    class TestNegative:
        def test_404(self, api_session):
            response = api_session.request(path='/wrong/')
            assert response.status_code == 404
            assert response.headers.get('content-type') == 'text/html'

        def test_405(self, api_session):
            response = api_session.request(path='/starships/', method='POST')
            assert response.status_code == 405
            assert response.json() == RESPONSE_BODY_405

        def test_wrong_qwery(self, api_session):
            response = api_session.request(path='/starships/asdgf/')
            assert response.status_code == 404
            assert response.json() == RESPONSE_BODY_404