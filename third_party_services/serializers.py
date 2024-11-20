import json
from rest_framework import serializers
from third_party_services.helpers import mask_string, validate_nin


class NinDetailsSerializer(serializers.Serializer):
    nin = serializers.CharField(max_length=14, required=True)

    def details(self, unmasked=False):
        self.is_valid(raise_exception=True)
        nin =  self.validated_data.get('nin')

        resp = validate_nin(nin)

        try:

            if resp.status == 500:
                raise serializers.ValidationError({'detail': 'Internal server error'})
            
            elif resp.status == 400:
                resp_data = json.loads(resp.data.decode('utf-8'))
                raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

            elif resp.status == 200:
                resp_data = json.loads(resp.data.decode('utf-8'))
                if resp_data['niraDataAsync'].get('isValid') == True:

                    personNationalId =  resp_data['niraDataAsync'].get('personNationalId', '')
                    personSurname =  resp_data['niraDataAsync'].get('personSurname', '')
                    personGivenNames =  resp_data['niraDataAsync'].get('personGivenNames', '')
                    personMaidenNames = resp_data['niraDataAsync'].get('personMaidenNames', '')
                    personOtherNames =  resp_data['niraDataAsync'].get('personOtherNames', '')
                    personDateOfBirth =  resp_data['niraDataAsync'].get('personDateOfBirth', '')
                    personNationality = resp_data['niraDataAsync'].get('personNationality', '')
                    transactionStatus = resp_data['niraDataAsync'].get('transactionStatus', '')
                    isValid = resp_data['niraDataAsync'].get('isValid', '')
                    message = resp_data['niraDataAsync'].get('message', '')

                    return {
                        "personNationalId": personNationalId,
                        "personSurname": personSurname,
                        "personGivenNames": personGivenNames,
                        "personMaidenNames": personMaidenNames if unmasked else  mask_string(personMaidenNames),
                        "personOtherNames": personOtherNames if unmasked else  mask_string(personOtherNames),
                        "personDateOfBirth": personDateOfBirth if unmasked else  mask_string(personDateOfBirth, 1),
                        "personNationality": personNationality if unmasked else  mask_string(personNationality, 1),
                    }
                
                else:
                    raise serializers.ValidationError({'detail': resp_data.get('errorS')[0]['errorDesc']})

            return resp
        
        except:
            return []