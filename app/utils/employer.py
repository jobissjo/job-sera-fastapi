from app.schemas.employer import Address, CompanyInformation, PersonalEmployerInformation,AdditionalInformation, EmployerProfile
from app.models.employer import EmployerProfileType
def employer_profile_model_schemas(employer_profile_model: EmployerProfileType) -> EmployerProfile:
    employer_id = employer_profile_model.employer_id
    personal_information_data = employer_profile_model.personal_information
    company_information_data = employer_profile_model.company_information
    additional_information_data = employer_profile_model.additional_information

    # Create Address object for CompanyInformation
    address_data = company_information_data.address
    address_dict = {
        "street": address_data.street,
        "city": address_data.city,
        "landmark": address_data.landmark,
        "state": address_data.state,
        "country": address_data.country,
        "postal_code": address_data.postal_code
    }
    address_model = Address(**address_dict)

    # Create PersonalEmployerInformation object
    personal_information = PersonalEmployerInformation(**personal_information_data.dict(), employer_profile_id=employer_id)

    # Create CompanyInformation object
    company_information = CompanyInformation(
        **company_information_data.dict(), 
        # address=address_model,
        employer_profile_id=employer_id
    )

    # Create AdditionalInformation object
    additional_information = AdditionalInformation(**additional_information_data.dict(), employer_profile_id=employer_id)

    # Create EmployerProfile object
    employer_profile = EmployerProfile(
        employer_id=employer_id,
        personal_information=personal_information,
        company_information=company_information,
        additional_information=additional_information
    )

    return employer_profile