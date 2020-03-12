from anduin import constants


class TestConstants:
    """Static Tests"""

    def test_environments(self):
        assert constants.ENV_DEV == 'Dev'
        assert constants.ENV_PROD == 'Prod'
        assert constants.ENV_TEST == 'Test'

    def test_offer_statuses(self):
        assert constants.OFFER_STATUS_ACCEPTED == 'Accepted'
        assert constants.OFFER_STATUS_PENDING == 'Pending'
        assert constants.OFFER_STATUS_REJECTED == 'Rejected'
        assert constants.OFFER_STATUSES == [
            constants.OFFER_STATUS_ACCEPTED,
            constants.OFFER_STATUS_PENDING,
            constants.OFFER_STATUS_REJECTED
        ]

    def test_races(self):
        assert constants.RACE_DWARF == 'Dwarf'
        assert constants.RACE_ELF == 'Elf'
        assert constants.RACE_WIZARD == 'Wizard'
        assert constants.RACES == [
            constants.RACE_DWARF,
            constants.RACE_ELF,
            constants.RACE_WIZARD
        ]

    def test_weapon_categories(self):
        assert constants.WEAPON_AXE == 'Axe'
        assert constants.WEAPON_STAFF == 'Staff'
        assert constants.WEAPON_SWORD == 'Sword'
        assert constants.WEAPON_CATEGORIES == [
            constants.WEAPON_AXE,
            constants.WEAPON_STAFF,
            constants.WEAPON_SWORD
        ]
