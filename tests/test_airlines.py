from .fixtures import fixture


def test_get_airline_by_id(requests_mock):
    with fixture('get-airline-by-id', '/airlines/id', requests_mock.get) as client:
        airline = client.airlines.get('id')
        assert airline.id == 'aln_00001876aqC8c5umZmrRds'
        assert airline.name == 'British Airways'
        assert airline.iata_code == 'BA'


def test_get_airline_by_id_without_iata_code(requests_mock):
    with fixture('get-airline-without-iata-code', '/airlines/id',
                 requests_mock.get) as client:
        airline = client.airlines.get('id')
        assert airline.id == 'some-id'
        assert airline.name == 'Duffel Airways'
        assert not hasattr(airline, 'iata_code')


def test_get_airlines(requests_mock):
    # We need a way to ensure pagination finished in a mocking environment
    end_pagination_url = 'http://someaddress/air/airlines?limit=50' + \
        '&after=g2wAAAACbQAAABBBZXJvbWlzdC1LaGFya2l2bQAAAB%3D'
    end_pagination_response = {'meta': {'after': None}, 'data': []}
    requests_mock.get(end_pagination_url, complete_qs=True, json=end_pagination_response)

    url = '/airlines?limit=50'
    with fixture('get-airlines', url, requests_mock.get) as client:
        paginated_airlines = client.airlines.list()
        airlines = list(paginated_airlines)
        assert len(airlines) == 1
        airline = airlines[0]
        assert airline.id == 'aln_00001876aqC8c5umZmrRds'
        assert airline.name == 'British Airways'
        assert airline.iata_code == 'BA'
