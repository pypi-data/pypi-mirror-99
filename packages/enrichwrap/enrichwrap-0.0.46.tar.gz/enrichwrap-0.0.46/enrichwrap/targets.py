enrich_targets = {}


def set_default_targets(http_url=None, http_port=None):
    global enrich_targets
    starthttp = 'http://localhost:8100/'
    if http_url is not None and http_port is not None:
        starthttp = 'http://' + http_url + ':' + http_port + '/'
        
    enrich_targets = {
        'socure': {
            'url': starthttp + 'socure/items',
            'body': {
                'modules': [
                    'fraud', 'phonerisk', 'addressrisk', 'emailrisk', 'kyc', 'social', 'watchliststandard', 'alertlist'
                ],
                'firstName': '',
                'surName': '',
                'email': '',
                'dob': '',
                'physicalAddress': '',
                'physicalAddress2': '',
                'city': '',
                'state': '',
                'country': '',
                'zip': '',
                'mobileNumber': '',
                'nationalId': '',
                'driverLicense': '',
                'driverLicenseState': '',
            },
            'mechanism': 'POST'
        },
        'giact': {
            'url': starthttp + 'giact/items',
            'mechanism': 'GET'
        },
        # TODO - need to check on payfone site for details if different than ID360/boss
        'payfonetrust': {
            'url': starthttp + 'payfone/trust/v2',
            'body': {
                'requestId': '',
                'details': '',
                'consentStatus': '',
                'phoneNumber': '',
            },
            'mechanism': 'POST'
        },
        'payfoneverify': {
            'url': starthttp + 'payfone/identity/verify/v2',
            'body': {
                'requestId': '',
                'payfoneAlias': '',
                'firstName': '',
                'lastName': '',
                'address': '',
                'extendedAddress': '',
                'city': '',
                'region': '',
                'postalCode': '',
                'lastVerified': '',
                'details': False,
                'phoneUpdate': False,
            },
            'mechanism': 'POST'
        },
        'threatmetrix': {
            'url': starthttp + 'threadmetrix',
            'params': [],
            'mechanism': 'GET'
        },
        #    'giact': starthttp + 'giact/items',
        'biocatch': {
            'url': starthttp + 'biocatch/items',
            'params': [],
            'mechanism': 'GET'
        },
        'bokugpir': {
            # getPhoneIdentificationResult
            'url': starthttp + 'boku/retrieve-evurl/items',
            'body': {
                'merchantId':'',
                'correlationId': '',
                'associationKey': '',
                'match': {
                    'consumerMdn': ''
                }
            },
            'mechanism': 'POST'
        },
        'bokumaa': {
            'url': starthttp + 'boku/match/items',
            'body': {
                'merchantId': '',
                'subMerchantId': '',
                'consentId': '',
                'consentTimeStamp': '',
                'msisdn': '',
                'correlationId': '',
                'firstName': '',
                'lastName': '',
                'address1': '',
                'address2': '',
                'city': '',
                'state': '',
                'postalCode': '',
                'countryCode': '',
                'nationalId': '',
                'dateOfBirth': ''
            },
            'mechanism': 'POST'
        }
    }

    return enrich_targets


def update_target(which_enrich, map_new_data):
    # Validate that I have what I need
    if 'url' not in map_new_data.keys() or 'mechanism' not in map_new_data.keys():
        print('MISSING values in updating enrich target - ignoring.  '
                      'Need "url" and "mechanism" at the least [%s]'%map_new_data)
        return
    mechanism = map_new_data.get('mechanism')
    if mechanism.lower() == 'post' and 'body' not in map_new_data.keys():
        print('If POST is the mechanism, then body must be provided [%s]' % map_new_data)
        return
    elif mechanism.lower() == 'get' and 'params' not in map_new_data.keys():
        print('If GET is the mechanism, then params must be provided [%s]' % map_new_data)
        return

    enrich_targets[which_enrich] = map_new_data


def get_target(which_enrich):
    if len(enrich_targets) == 0:
        set_default_targets()
    return enrich_targets[which_enrich]


def set_enrich_targets(map):
    global enrich_targets
    enrich_targets = map
    return enrich_targets


def get_targets():
    return enrich_targets
