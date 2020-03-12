import pytest
from flask import url_for

from anduin.constants import OFFER_STATUS_ACCEPTED, OFFER_STATUS_REJECTED
from tests import factories


class TestOffers:
    @pytest.fixture
    def users_with_weapons(self):
        user_1 = factories.UsersFactory()
        factories.WeaponsFactory(user=user_1)
        factories.WeaponsFactory(user=user_1)

        user_2 = factories.UsersFactory()
        factories.WeaponsFactory(user=user_2)
        factories.WeaponsFactory(user=user_2)

        return [user_1, user_2]

    @pytest.fixture
    def offers(self, users_with_weapons):
        offer_1 = factories.OffersFactory()
        offer_1.users = users_with_weapons
        offer_1.weapons = [
            users_with_weapons[0].weapons[0],
            users_with_weapons[0].weapons[1],
            users_with_weapons[1].weapons[0]
        ]

        offer_2 = factories.OffersFactory()
        offer_2.users = users_with_weapons
        offer_2.weapons = [
            users_with_weapons[0].weapons[0],
            users_with_weapons[1].weapons[1]
        ]

        return [offer_1, offer_2]

    @pytest.fixture
    def accepted_offer(self, users_with_weapons):
        offer = factories.OffersFactory(status=OFFER_STATUS_ACCEPTED)
        offer.users = users_with_weapons
        offer.weapons = [
            users_with_weapons[0].weapons[0],
            users_with_weapons[1].weapons[0]
        ]
        return offer

    @pytest.fixture
    def rejected_offer(self, users_with_weapons):
        offer = factories.OffersFactory(status=OFFER_STATUS_REJECTED)
        offer.users = users_with_weapons
        offer.weapons = [
            users_with_weapons[0].weapons[0],
            users_with_weapons[1].weapons[0]
        ]
        return offer

    def test_get_offer_by_id(self, testapp, offers):
        res = testapp.get(url_for('offers_blueprint.get_offer_by_id', id=str(offers[0].id)))
        assert res.status_code == 200
        assert res.json != {}

    def test_get_offer_by_id_not_found(self, testapp):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.get(url_for('offers_blueprint.get_offer_by_id', id=bogus_id))
        assert res.status_code == 404
        assert res.json != {}

    def test_create_offer(self, testapp, users_with_weapons):
        assert 1 != 1

    def test_create_offer_user_not_found(self, testapp, users_with_weapons):
        assert 1 != 1

    def test_create_offer_weapon_not_found(self, testapp, users_with_weapons):
        assert 1 != 1

    def test_create_offer_incorrect_ownership(self, testapp, users_with_weapons):
        assert 1 != 1

    def test_accept_offer_by_id(self, testapp, offers):
        res = testapp.post(url_for('offers_blueprint.accept_offer_by_id', id=str(offers[0].id)))
        assert res.status_code == 200
        assert res.json != {}

    def test_accept_offer_by_id_not_found(self, testapp, offers):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.post(url_for('offers_blueprint.accept_offer_by_id', id=bogus_id))
        assert res.status_code == 404
        assert res.json != {}

    def test_accept_offer_by_id_already_completed(self, testapp, accepted_offer):
        res = testapp.post(url_for('offers_blueprint.accept_offer_by_id', id=str(accepted_offer.id)))
        assert res.status_code == 400
        assert res.json != {}

    def test_reject_offer_by_id(self, testapp, offers):
        res = testapp.post(url_for('offers_blueprint.reject_offer_by_id', id=str(offers[0].id)))
        assert res.status_code == 200
        assert res.json != {}

    def test_reject_offer_by_id_not_found(self, testapp, offers):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.post(url_for('offers_blueprint.reject_offer_by_id', id=bogus_id))
        assert res.status_code == 404
        assert res.json != {}

    def test_reject_offer_by_id_already_completed(self, testapp, rejected_offer):
        res = testapp.post(url_for('offers_blueprint.reject_offer_by_id', id=str(rejected_offer.id)))
        assert res.status_code == 400
        assert res.json != {}
