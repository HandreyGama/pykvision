from pykvision.models.schemes.intelligent import IntelligentScheme


def test_set_fd_lib_capabilities_maps_new_fields():
    scheme = IntelligentScheme()
    payload = {
        "isSupport": "true",
        "isSupportStandardSearch": "false",
        "isSupportCustomFaceLibID": "true",
        "isSupportPicCertification": "true",
    }

    scheme.set_fd_lib_capabilities(payload)

    assert scheme.fd_lib.fd_lib_cap.is_support_fc_search_data_package is True
    assert scheme.fd_lib.fd_lib_cap.is_support_standard_search is False
    assert scheme.fd_lib.fd_lib_cap.is_support_custom_face_lib_id is True
    assert scheme.fd_lib.fd_lib_cap.is_support_pic_certification is True
