import pytest
from flask import url_for

from anduin.database import db
from anduin.models.users import Users
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
        assert 'users' in res.json
        assert len(res.json['users']) >= 1

        user = [u for u in res.json['users'] if u['id'] == str(user_with_weapons.id)][0]
        expected_keys = ['id', 'created_at', 'username', 'race', 'weapons']
        assert all([key in user for key in expected_keys])
        assert len(user['weapons']) == len(user_with_weapons.weapons)

    def test_get_user_by_id(self, testapp, user_with_weapons):
        res = testapp.get(url_for('users_blueprint.get_user_by_id', id=str(user_with_weapons.id)))

        assert res.status_code == 200
        assert 'user' in res.json

        user = res.json['user']
        expected_keys = ['id', 'created_at', 'username', 'race', 'weapons']

        assert all([key in user for key in expected_keys])
        assert user['id'] == str(user_with_weapons.id)

    def test_get_user_by_id_not_found(self, testapp):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.get(url_for('users_blueprint.get_user_by_id', id=bogus_id), expect_errors=True)

        assert res.status_code == 404
        assert f'No user found with id {bogus_id}' in res.json['error']

    def test_get_user_by_username(self, testapp, user_with_weapons):
        res = testapp.get(url_for('users_blueprint.get_user_by_username', username=str(user_with_weapons.username)))

        assert res.status_code == 200
        assert 'user' in res.json

        user = res.json['user']
        expected_keys = ['id', 'created_at', 'username', 'race', 'weapons']

        assert all([key in user for key in expected_keys])
        assert user['username'] == str(user_with_weapons.username)

    def test_get_user_by_username_not_found(self, testapp):
        bogus_username = 'hunter2'
        res = testapp.get(url_for('users_blueprint.get_user_by_username', username=bogus_username), expect_errors=True)

        assert res.status_code == 404
        assert f'No user found with username {bogus_username}' in res.json['error']

    def test_get_user_inventory_by_id(self, testapp, user_with_weapons):
        res = testapp.get(url_for('users_blueprint.get_user_inventory_by_id', id=str(user_with_weapons.id)))

        assert res.status_code == 200
        assert 'inventory' in res.json

        weapons = res.json['inventory']
        original_user_weapon_ids = [str(weapon.id) for weapon in user_with_weapons.weapons]
        assert len(weapons) == len(user_with_weapons.weapons)
        assert all([weapon['id'] in original_user_weapon_ids for weapon in weapons])

    def test_get_user_inventory_by_id_not_found(self, testapp, user_with_weapons):
        bogus_id = 'cc9deeab-b652-4b4c-be72-da5b2dfed5d3'
        res = testapp.get(url_for('users_blueprint.get_user_inventory_by_id', id=bogus_id), expect_errors=True)

        assert res.status_code == 404
        assert f'No user found with id {bogus_id}' in res.json['error']
