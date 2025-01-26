from app.models.employer import (
    Address,
    CompanyInformation,
    PersonalEmployerInformation,
    AdditionalInformation,
    EmployerProfile,
)
from app.schema.employer import EmployerProfileType


def employer_profile_model_schemas(
    employer_profile_model: EmployerProfileType,
) -> EmployerProfile:
    employer_id = employer_profile_model.employer_id
    personal_information_data = employer_profile_model.personalInformation
    company_information_data = employer_profile_model.companyInformation
    additional_information_data = employer_profile_model.additionalInformation

    # Create Address object for CompanyInformation
    address_data = company_information_data.address
    address_dict = {
        "street": address_data.street,
        "city": address_data.city,
        "landmark": address_data.landmark,
        "state": address_data.state,
        "country": address_data.country,
        "postalCode": address_data.postalCode,
    }
    address_model = Address(**address_dict)

    # Create PersonalEmployerInformation object
    personal_information = PersonalEmployerInformation(
        **personal_information_data.dict(), employer_profile_id=employer_id
    )

    # Create CompanyInformation object
    company_information = CompanyInformation(
        **company_information_data.dict(),
        # address=address_model,
        employer_profile_id=employer_id,
    )

    # Create AdditionalInformation object
    additional_information = AdditionalInformation(
        **additional_information_data.model_dump(), employer_profile_id=employer_id
    )

    # Create EmployerProfile object
    employer_profile = EmployerProfile(
        employer_id=employer_id,
        personalInformation=personal_information,
        companyInformation=company_information,
        additionalInformation=additional_information,
    )

    return employer_profile
