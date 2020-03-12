from unittest.mock import patch

import pytest

from anduin.controllers import users as users_controller
from anduin.exceptions import RowNotFound
from anduin.models.users import Users


class TestUsersController:

    @patch.object(Users, 'get')
    def test_get_users(self, mock_get):
        users_controller.get_users()
        mock_get.assert_called_once()

    @patch.object(Users, 'get')
    def test_get_users_empty_response(self, mock_get):
        mock_get.all.return_value = []
        
        res = users_controller.get_users()
        
        assert res == []
        mock_get.assert_called_once()

    @patch.object(Users, 'get_by_id')
    def test_get_user_by_id(self, mock_get):
        users_controller.get_user_by_id('some_uuid')
        mock_get.assert_called_once()

    @patch.object(Users, 'get_by_id')
    def test_get_user_by_id_raise_not_found_exception(self, mock_get):
        bogus_id = 'some_bogus_id'
        mock_get(bogus_id).first.return_value = None

        with pytest.raises(RowNotFound):
            users_controller.get_user_by_id('some_bogus_id')

        assert mock_get.call_count >= 1

    @patch.object(Users, 'get_by_id')
    def test_get_user_inventory_by_id(self, mock_get):
        users_controller.get_user_inventory_by_id('some_uuid')
        mock_get.assert_called_once()

    @patch.object(Users, 'get_by_id')
    def test_get_user_inventory_by_id_raise_not_found_exception(self, mock_get):
        # This test especially reveals a code smell of poor composition, not testing the to_dict calls at all
        bogus_id = 'some_bogus_id'
        mock_get(bogus_id).first.return_value = None

        with pytest.raises(RowNotFound):
            users_controller.get_user_inventory_by_id('some_bogus_id')

        assert mock_get.call_count >= 1
