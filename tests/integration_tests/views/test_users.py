import pytest
from flask import url_for

from tests import factories


class TestUsers:
    @pytest.fixture
    def user_with_weapons(self):
        user = factories.UsersFactory()
        factories.WeaponsFactory(user=user)
        factories.WeaponsFactory(user=user)
        return user

    def test_get_users(self, testapp, user_with_weapons):
        res = testapp.get(url_for('users_blueprint.get_users'))
        assert res.status_code == 200
        assert res.json != {}

    def test_get_users_empty_response(self, testapp):
        res = testapp.get(url_for('users_blueprint.get_users'))
        assert res.status_code == 200
        assert res.json != {}

    def test_get_user_by_id(self, testapp, user_with_weapons):
        res = testapp.get(url_for('users_blueprint.get_user_by_id', id=str(user_with_weapons.id)))
        assert res.status_code == 200
        assert res.json != {}

    def test_get_user_by_id_not_found(self, testapp):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.get(url_for('users_blueprint.get_user_by_id', id=bogus_id))
        assert res.status_code == 404
        assert res.json != {}

    def test_get_user_inventory_by_id(self, testapp, user_with_weapons):
        res = testapp.get(url_for('users_blueprint.get_user_inventory_by_id', id=str(user_with_weapons.id)))
        assert res.status_code == 200
        assert res.json != {}

    def test_get_user_inventory_by_id_not_found(self, testapp, user_with_weapons):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.get(url_for('users_blueprint.get_user_inventory_by_id', id=bogus_id))
        assert res.status_code == 404
        assert res.json != {}