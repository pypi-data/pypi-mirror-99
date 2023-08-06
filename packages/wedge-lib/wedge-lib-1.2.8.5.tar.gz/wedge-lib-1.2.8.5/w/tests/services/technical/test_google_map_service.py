from django.conf import settings
from w.services.technical.google_map_service import GoogleMapService
from w.tests.mixins.testcase_mixin import TestCaseMixin

TEST_URL = "ma grosse adresses avec # des caratères à la con !$"
TEST_PLACE_ID = "ChIJN1t_tDeuEmsRUsoyG83frY4"


class TestGMapService(TestCaseMixin):
    def test_build_geocode_url(self):
        url = GoogleMapService.build_geocode_url(TEST_URL)
        assert (
            url == "https://maps.googleapis.com/maps/api/geocode/json?address="
            "ma+grosse+adresses+avec+%23+des+carat%C3%A8res+%C3%A0+la+con+"
            "%21%24&key=AIzaSyAYU9lXqmmetI3s7feQi_Yc6_f7KGvVPz4"
        )

    def test_geocode_service(self):
        resp = GoogleMapService.geocode_address(
            "Royal Albert Hall, Kensington Gore, Londres, Royaume-Uni"
        )
        if settings.MOCK_GMAP_CALLS:
            assert resp["lat"] == 10
            assert resp["lng"] == 10
        else:
            assert resp["lat"] == 51.5009088
            assert resp["lng"] == -0.177366

    def test_place_autocomplete(self):
        url = GoogleMapService.build_autocomplete_place_url(TEST_URL, "mysession_token")
        assert (
            url == "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?"
            "input=ma+grosse+adresses+avec+%23+des+carat%C3%A8res+%C3%A0+la+con+%21%24"
            "&key=AIzaSyAYU9lXqmmetI3s7feQi_Yc6_f7KGvVPz4&langage=fr&components=country"
            "%3Afr%7Ccountry%3Ach%7Ccountry%3Abe%7Ccountry%3Ade%7Ccountry%3Aes"
            "&sessiontoken=mysession_token"
        )

    def test_autocomplete_address(self):
        resp = GoogleMapService.autocomplete_address("rue du mascaret, Bordeaux")
        if settings.MOCK_GMAP_CALLS:
            assert resp["location"]["lat"] == 10
            assert resp["location"]["lng"] == 10
        else:
            assert (
                resp["formatted_address"] == "Rue du Mascaret, 33800 Bordeaux, France"
            )
            assert resp["location"]["lat"] == 44.8262542
            assert resp["location"]["lng"] == -0.5518803

    def test_build_place_detail_address(self):
        url = GoogleMapService.build_place_detail_url(TEST_PLACE_ID)
        assert (
            url == "https://maps.googleapis.com/maps/api/place/details/json?"
            "place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&key=AIzaSyAYU9lXqmmetI3s7feQi_Yc6_"
            "f7KGvVPz4&fields=geometry,formatted_address,place_id"
        )

    def test_get_place_detail(self):
        resp = GoogleMapService.get_place_detail(TEST_PLACE_ID)
        self.assert_equals_resultset(resp)
