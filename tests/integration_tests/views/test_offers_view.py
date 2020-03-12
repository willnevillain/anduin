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
        assert 'offer' in res.json
        offer = res.json['offer']

        expected_keys = ['id', 'created_at', 'status', 'users', 'weapons']
        assert all([key in offer for key in expected_keys])
        assert len(offer['users']) == len(offers[0].users)
        assert len(offer['weapons']) == len(offers[0].weapons)

    def test_get_offer_by_id_not_found(self, testapp):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.get(url_for('offers_blueprint.get_offer_by_id', id=bogus_id), expect_errors=True)
        assert res.status_code == 404
        assert f'No offer found for id {bogus_id}' in res.json['error']

    def test_create_offer(self, testapp, users_with_weapons):
        req_body = {
            'users': [
                {
                    'username': users_with_weapons[0].username,
                    'weapon_ids': [str(weapon.id) for weapon in users_with_weapons[0].weapons]
                },
                {
                    'username': users_with_weapons[1].username,
                    'weapon_ids': [str(weapon.id) for weapon in users_with_weapons[1].weapons]
                }
            ]
        }

        res = testapp.post_json(url_for('offers_blueprint.create_offer'), req_body)

        assert res.status_code == 201
        assert 'offer' in res.json
        offer = res.json['offer']
        expected_keys = ['id', 'created_at', 'status', 'users', 'weapons']
        assert all([key in offer for key in expected_keys])
        assert len(offer['users']) == 2
        assert len(offer['weapons']) == len(users_with_weapons[0].weapons) + len(users_with_weapons[0].weapons)

    def test_create_offer_user_not_found(self, testapp, users_with_weapons):
        bogus_username = 'hunter2'
        req_body = {
            'users': [
                {
                    'username': users_with_weapons[0].username,
                    'weapon_ids': [str(weapon.id) for weapon in users_with_weapons[0].weapons]
                },
                {
                    'username': bogus_username,
                    'weapon_ids': []
                }
            ]
        }

        res = testapp.post_json(url_for('offers_blueprint.create_offer'), req_body, expect_errors=True)

        assert res.status_code == 404
        assert f'No user found for username {bogus_username}' in res.json['error']

    def test_create_offer_weapon_not_found(self, testapp, users_with_weapons):
        bogus_id = '37fd92b8-d872-4bec-a742-3c476f26fd83'
        req_body = {
            'users': [
                {
                    'username': users_with_weapons[0].username,
                    'weapon_ids': [str(weapon.id) for weapon in users_with_weapons[0].weapons]
                },
                {
                    'username': users_with_weapons[1].username,
                    'weapon_ids': [bogus_id]
                }
            ]
        }

        res = testapp.post_json(url_for('offers_blueprint.create_offer'), req_body, expect_errors=True)

        assert res.status_code == 404
        assert f'No weapon found for id {bogus_id}' in res.json['error']

    def test_create_offer_incorrect_ownership(self, testapp, users_with_weapons):
        # Note that the weapons are swapped
        req_body = {
            'users': [
                {
                    'username': users_with_weapons[0].username,
                    'weapon_ids': [str(weapon.id) for weapon in users_with_weapons[1].weapons]
                },
                {
                    'username': users_with_weapons[1].username,
                    'weapon_ids': [str(weapon.id) for weapon in users_with_weapons[0].weapons]
                }
            ]
        }

        res = testapp.post_json(url_for('offers_blueprint.create_offer'), req_body, expect_errors=True)

        assert res.status_code == 400
        assert f'does not belong to user' in res.json['error']

    def test_accept_offer_by_id(self, testapp, offers):
        res = testapp.post(url_for('offers_blueprint.accept_offer_by_id', id=str(offers[0].id)))

        assert res.status_code == 200
        assert res.json['offer']['status'] == OFFER_STATUS_ACCEPTED


    def test_accept_offer_by_id_not_found(self, testapp, offers):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'

        res = testapp.post(url_for('offers_blueprint.accept_offer_by_id', id=bogus_id), expect_errors=True)

        assert res.status_code == 404
        assert f'Offer not found for id {bogus_id}' in res.json['error']

    def test_accept_offer_by_id_already_completed(self, testapp, accepted_offer):

        res = testapp.post(url_for('offers_blueprint.accept_offer_by_id', id=str(accepted_offer.id)), expect_errors=True)

        assert res.status_code == 400
        assert f'{str(accepted_offer.id)} is already in final state {accepted_offer.status}' in res.json['error']

    def test_reject_offer_by_id(self, testapp, offers):
        res = testapp.post(url_for('offers_blueprint.reject_offer_by_id', id=str(offers[0].id)))

        assert res.status_code == 200
        assert res.json['offer']['status'] == OFFER_STATUS_REJECTED

    def test_reject_offer_by_id_not_found(self, testapp, offers):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'

        res = testapp.post(url_for('offers_blueprint.reject_offer_by_id', id=bogus_id), expect_errors=True)

        assert res.status_code == 404
        assert f'Offer not found for id {bogus_id}' in res.json['error']

    def test_reject_offer_by_id_already_completed(self, testapp, rejected_offer):
        res = testapp.post(url_for('offers_blueprint.reject_offer_by_id', id=str(rejected_offer.id)), expect_errors=True)

        assert res.status_code == 400
        assert f'{str(rejected_offer.id)} is already in final state {rejected_offer.status}' in res.json['error']
