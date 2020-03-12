from unittest.mock import MagicMock, patch

import pytest

from anduin.constants import OFFER_STATUS_PENDING
from anduin.controllers import offers as offers_controller
from anduin.exceptions import InvalidDataIntegrity, RowNotFound
from anduin.models.offers import Offers
from anduin.models.users import Users
from anduin.models.weapons import Weapons


class TestOffersController:

    @patch.object(Offers, 'get_by_id')
    def test_get_offer_by_id(self, mock_get):
        offers_controller.get_offer_by_id('some_uuid')
        mock_get.assert_called_once()

    @patch.object(Offers, 'get_by_id')
    def test_get_offer_by_id_raise_not_found_exception(self, mock_get):
        bogus_id = 'some_bogus_id'
        mock_get(bogus_id).first.return_value = None

        with pytest.raises(RowNotFound):
            offers_controller.get_offer_by_id(bogus_id)

        assert mock_get.call_count >= 1

    @patch.object(offers_controller, '_validate_new_offer')
    @patch.object(Users, 'get_by_username')
    @patch.object(Weapons, 'get_by_id')
    @patch.object(Offers, 'save')
    def test_create_offer(self, mock_save, mock_weapon_get, mock_user_get, mock_validate):
        offers_controller.create_offer({'users': [{'username': 'bob', 'weapon_ids': ['a']}]})

        mock_save.assert_called_once()
        assert mock_weapon_get.call_count >= 1
        assert mock_user_get.call_count >= 1
        mock_validate.assert_called_once()

    @patch.object(offers_controller, '_validate_new_offer', side_effect=RowNotFound)
    def test_create_offer_reraise_validation_exception(self, mock_validate):
        with pytest.raises(RowNotFound):
            offers_controller.create_offer({'does_not': 'matter'})

        mock_validate.assert_called_once()

    @patch.object(offers_controller, '_update_offer_status_by_id')
    def test_accept_offer_by_id(self, mock_update):
        offers_controller.accept_offer_by_id('some_uuid')

        mock_update.assert_called_once()

    @patch.object(offers_controller, '_update_offer_status_by_id', side_effect=RowNotFound)
    def test_accept_offer_by_id_reraise_exception(self, mock_update):
        with pytest.raises(RowNotFound):
            offers_controller.accept_offer_by_id('some_uuid')

        mock_update.assert_called_once()

    @patch.object(offers_controller, '_update_offer_status_by_id')
    def test_reject_offer_by_id(self, mock_update):
        offers_controller.reject_offer_by_id('some_uuid')

        mock_update.assert_called_once()

    @patch.object(offers_controller, '_update_offer_status_by_id', side_effect=RowNotFound)
    def test_reject_offer_by_id_reraise_exception(self, mock_update):
        with pytest.raises(RowNotFound):
            offers_controller.reject_offer_by_id('some_uuid')

        mock_update.assert_called_once()

    @patch.object(Offers, 'get_by_id')
    def test_update_offer_status_by_id(self, mock_get):
        some_uuid = 'some_uuid'
        get_return_value = MagicMock()
        get_return_value.status = OFFER_STATUS_PENDING
        mock_get(some_uuid).first.return_value = get_return_value

        offers_controller._update_offer_status_by_id(some_uuid, 'new_status')

        assert mock_get.call_count > 1

    @patch.object(Offers, 'get_by_id')
    def test_update_offer_status_by_id_raise_not_found_exception(self, mock_get):
        some_uuid = 'some_uuid'
        mock_get(some_uuid).first.return_value = None

        with pytest.raises(RowNotFound):
            offers_controller._update_offer_status_by_id(some_uuid, 'new_status')

        assert mock_get.call_count > 1

    @patch.object(Offers, 'get_by_id')
    def test_update_offer_status_by_id_raise_invalid_data_integrity_exception(self, mock_get):
        some_uuid = 'some_uuid'
        get_return_value = MagicMock()
        get_return_value.status = 'definitely_not_pending'
        mock_get(some_uuid).first.return_value = get_return_value

        with pytest.raises(InvalidDataIntegrity):
            offers_controller._update_offer_status_by_id(some_uuid, 'new_status')

        assert mock_get.call_count > 1
