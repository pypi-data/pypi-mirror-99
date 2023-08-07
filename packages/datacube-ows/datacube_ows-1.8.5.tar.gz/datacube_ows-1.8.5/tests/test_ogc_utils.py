import datacube_ows.ogc_utils
import datetime

import pytest

class DSCT:
    def __init__(self, meta):
        self.center_time = datetime.datetime(1970,1,1,0,0,0)
        self.metadata_doc = meta

def test_dataset_center_time():
    dct = datacube_ows.ogc_utils.dataset_center_time
    ds = DSCT({})
    assert dct(ds).year == 1970
    ds = DSCT({
        "properties": {
            "dtr:start_datetime": "1980-01-01T00:00:00"
        },
    })
    assert dct(ds).year == 1980
    ds = DSCT({
        "extent": {
            "center_dt": "1990-01-01T00:00:00"
        },
        "properties": {
            "dtr:start_datetime": "1980-01-01T00:00:00"
        },
    })
    assert dct(ds).year == 1990

def test_get_service_base_url():

    # not a list
    allowed_urls = "https://foo.hello.world"
    request_url = "https://foo.bar.baz"
    ret = datacube_ows.ogc_utils.get_service_base_url(allowed_urls, request_url)
    assert ret == "https://foo.hello.world"

    # Value not in list
    allowed_urls = ["https://foo.hello.world", "https://alice.bob.eve"]
    request_url = "https://foo.bar.baz"
    ret = datacube_ows.ogc_utils.get_service_base_url(allowed_urls, request_url)
    assert ret == "https://foo.hello.world"

    # Value in list
    allowed_urls = ["https://foo.hello.world","https://foo.bar.baz", "https://alice.bob.eve"]
    request_url = "https://foo.bar.baz"
    ret = datacube_ows.ogc_utils.get_service_base_url(allowed_urls, request_url)
    assert ret == "https://foo.bar.baz"

    # Trailing /
    allowed_urls = ["https://foo.bar.baz", "https://alice.bob.eve"]
    request_url = "https://foo.bar.baz/"
    ret = datacube_ows.ogc_utils.get_service_base_url(allowed_urls, request_url)
    assert ret == "https://foo.bar.baz"

    #include path
    allowed_urls = ["https://foo.bar.baz", "https://foo.bar.baz/wms/"]
    request_url = "https://foo.bar.baz/wms/"
    ret = datacube_ows.ogc_utils.get_service_base_url(allowed_urls, request_url)
    assert ret == "https://foo.bar.baz/wms"

    # use value from list instead of request
    allowed_urls = ["https://foo.bar.baz", "https://foo.bar.baz/wms/"]
    request_url = "http://foo.bar.baz/wms/"
    ret = datacube_ows.ogc_utils.get_service_base_url(allowed_urls, request_url)
    assert ret == "https://foo.bar.baz/wms"


def test_parse_for_base_url():
    url = "https://hello.world.bar:8000/wms/?CheckSomething"
    ret = datacube_ows.ogc_utils.parse_for_base_url(url)
    assert ret == "hello.world.bar:8000/wms"


def test_create_geobox():
    geobox = datacube_ows.ogc_utils.create_geobox("EPSG:4326",
                                                  140.7184, 145.6924, -16.1144, -13.4938,
                                                  1182, 668)
    geobox_ho = datacube_ows.ogc_utils.create_geobox("EPSG:4326",
                                                  140.7184, 145.6924, -16.1144, -13.4938,
                                                  1182, 668)
    geobox_wo = datacube_ows.ogc_utils.create_geobox("EPSG:4326",
                              140.7184, 145.6924, -16.1144, -13.4938,
                              1182, 668)
    for gb in (geobox, geobox_ho, geobox_wo):
        assert geobox.width == 1182
        assert geobox.height == 668
    with pytest.raises(Exception) as excinfo:
        geobox_no = datacube_ows.ogc_utils.create_geobox("EPSG:4326",
                                                         140.7184, 145.6924, -16.1144, -13.4938)
    assert "Must supply at least a width or height" in str(excinfo.value)
