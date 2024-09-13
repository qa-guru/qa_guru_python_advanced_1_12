import allure

from models.people import People, ListPeople
from tests.body import RESPONSE_BODY_405, RESPONSE_BODY_404


@allure.feature('People')
class TestPeople:
    @allure.story('Positive tests')
    class TestPositive:

        def test_get_all_people(self, api_session):
            response = api_session.request(path='/people/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            pass

        def test_get_first_people(self, api_session):
            response = api_session.request(path='/people/1/')

            assert response.status_code == 200
            people = People.model_validate(response.json())
            assert people.name == 'Luke Skywalker'

        def test_get_second_people(self, api_session):
            response = api_session.request(path='/people/2/')
            assert response.status_code == 200
            people = People.model_validate(response.json())
            assert people.name == 'C-3PO'

        def test_get_without_header_user_agent(self, api_session):
            api_session.headers.pop('user-agent')
            response = api_session.request(path='/people/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'

        def test_search_people(self, api_session):
            # params = {'name': 'Obi-Wan Kenobi'}
            response = api_session.request(path='/people/10/')
            assert response.status_code == 200
            assert response.headers.get('content-type') == 'application/json'
            people = People.model_validate(response.json())
            assert people.name == 'Obi-Wan Kenobi'

    @allure.story('Negative tests')
    class TestNegative:
        def test_404(self, api_session):
            response = api_session.request(path='/wrong/')
            assert response.status_code == 404
            assert response.headers.get('content-type') == 'text/html'

        def test_405(self, api_session):
            response = api_session.request(path='/people/', method='POST')
            assert response.status_code == 405
            assert response.json() == RESPONSE_BODY_405

        def test_wrong_qwery(self, api_session):
            response = api_session.request(path='/people/asdgf/')
            assert response.status_code == 404
            assert response.json() == RESPONSE_BODY_404
