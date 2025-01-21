import json
from rest_framework import serializers
from third_party_services.helpers import mask_email, mask_string, validate_brn, validate_nin, validate_tin, validate_vehicle


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
                        "personDateOfBirth": personDateOfBirth,
                        "personNationality": personNationality if unmasked else  mask_string(personNationality, 1),
                        "isValid": isValid
                    }
                
                else:
                    raise serializers.ValidationError({'detail': resp_data.get('errorS')[0]['errorDesc']})

            return resp
        
        except:
            return []
class TinDetailsSerializer(serializers.Serializer):
    tin = serializers.CharField(max_length=10, required=True)

    def details(self, unmasked=False):
        self.is_valid(raise_exception=True)
        tin =  self.validated_data.get('tin')

        resp = validate_tin(tin)

        try:

            if resp.status == 500:
                raise serializers.ValidationError({'detail': 'Internal server error'})
            
            elif resp.status == 400:
                resp_data = json.loads(resp.data.decode('utf-8'))
                raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

            elif resp.status == 200:
                resp_data = json.loads(resp.data.decode('utf-8'))
                if resp_data.get('errorDesc') == 'SUCCESS':
                    contactNumber = resp_data.get('contactNumber', '')
                    county = resp_data.get('county', '')
                    district = resp_data.get('district', '')
                    errorCode = resp_data.get('errorCode', '')
                    errorDesc = resp_data.get('errorDesc', '')
                    isCustomsAgent = resp_data.get('isCustomsAgent', '')
                    isLicenseValid = resp_data.get('isLicenseValid', '')
                    licenseNumber = resp_data.get('licenseNumber', '')
                    mobileNumber = resp_data.get('mobileNumber', '')
                    postalAddress= resp_data.get('postalAddress', '')
                    registrationStatus= resp_data.get('registrationStatus', '')
                    subCounty = resp_data.get('subCounty', '')
                    taxPayerEmail= resp_data.get('taxPayerEmail', '')
                    taxPayerName= resp_data.get('taxPayerName', '')
                    telephoneNumber= resp_data.get('telephoneNumber', '')
                    typeofUser = resp_data.get('typeofUser', '')
                    village= resp_data.get('village', '')
                    tin= resp_data.get('tin', '')

                    return {
                        "contactNumber": contactNumber if unmasked else  mask_string(contactNumber),
                        "county": county if unmasked else  mask_string(county),
                        "district": district if unmasked else  mask_string(district),
                        "isCustomsAgent": isCustomsAgent,
                        "mobileNumber": mobileNumber if unmasked else  mask_string(mobileNumber),
                        "postalAddress": postalAddress if unmasked else  mask_string(postalAddress),
                        "registrationStatus": registrationStatus,
                        "subCounty": subCounty if unmasked else  mask_string(subCounty),
                        "taxPayerEmail":taxPayerEmail,
                        "taxPayerName": taxPayerName,
                        "telephoneNumber":telephoneNumber if unmasked else  mask_string(telephoneNumber),
                        "village": village if unmasked else  mask_string(village),
                        "tin": tin
                    }
                
                else:
                    raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

            return resp
        
        except:
            return []
    
    

class BrnDetailsSerializer(serializers.Serializer):
    brn = serializers.CharField(max_length=14, required=True)

    def details(self, unmasked=False):
        self.is_valid(raise_exception=True)
        brn =  self.validated_data.get('brn')

        resp = validate_brn(brn)

        try:

            if resp.status == 500:
                raise serializers.ValidationError({'detail': 'Internal server error'})
            
            elif resp.status == 400:
                resp_data = json.loads(resp.data.decode('utf-8'))
                raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

            elif resp.status == 200:
                resp_data = json.loads(resp.data.decode('utf-8'))
                if resp_data.get('errors') == None:

                    entityName =  resp_data['brnDetailsFromUrsb'].get('entityName', '')
                    isValid =  resp_data['brnDetailsFromUrsb'].get('isValid', '')
                    

                    return {
                        "entityName": entityName,
                        "isValid" : isValid == True
                    }
                
                else:
                    raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

            return resp

        except:
            return []
        

class VehicleDetailsSerializer(serializers.Serializer):
    number_plate = serializers.CharField(max_length=25, required=True)

    def details(self, unmasked=False):
        self.is_valid(raise_exception=True)
        plate =  self.validated_data.get('number_plate')

        resp = validate_vehicle(plate)

        if resp.status == 500:
            raise serializers.ValidationError({'detail': 'Internal server error'})
        
        elif resp.status == 400:
            resp_data = json.loads(resp.data.decode('utf-8'))
            raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

        elif resp.status == 200:
            resp_data = json.loads(resp.data.decode('utf-8'))
            if resp_data.get('errorDesc') == 'SUCCESS':
                tax_payer_name = resp_data.get('taxPayerName', '')
                mobile_number = resp_data.get('mobileNumber', '')
                email = resp_data.get('email', '')
                tin = resp_data.get('tinNo', '')
                make_year = resp_data.get('manufactureYear', '')
                model = resp_data.get('modelName', '')
                engine_number = resp_data.get('engineNo', '')
                chasis_number = resp_data.get('chasisNo', '')
                color = resp_data.get('color', '')
            
                return {
                    'tax_payer_name': tax_payer_name if unmasked else  mask_string(tax_payer_name),
                    'mobile_number': mobile_number if unmasked else mask_string(mobile_number),
                    'email': email if unmasked else mask_email(email),
                    'tin': tin if unmasked else mask_string(tin),
                    'make_year': make_year if unmasked else mask_string(make_year),
                    'model': model if unmasked else mask_string(model),
                    'engine_number': engine_number if unmasked else mask_string(engine_number),
                    'chasis_number': chasis_number if unmasked else mask_string(chasis_number),
                    'color': color if unmasked else mask_string(color),
                    'is_individual': resp_data.get('taxPayerType') == 'INDI',
                    'seat_capacity': resp_data.get('seatCapacity'),
                    'category_name': resp_data.get('categoryName'),
                    'purpose': resp_data.get('purpose'),
                    'tonnage': (int(resp_data.get('grossWeight', 0)) - int(resp_data.get('netWeight', 0))) / 1000,
                    'errorDesc': resp_data.get('errorDesc')
                }
            else:
                raise serializers.ValidationError({'detail': resp_data.get('errorDesc')})

        return resp