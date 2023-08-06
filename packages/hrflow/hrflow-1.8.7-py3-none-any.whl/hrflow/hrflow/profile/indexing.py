from ..utils import format_item_payload, validate_key, validate_response


class ProfileIndexing():
    """Manage embedding related profile calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def add_json(self, source_key, profile_json):
        """Use the api to add a new profile using profile_data."""
        profile_json['source_key'] = validate_key("Source", source_key)
        response = self.client.post("profile/indexing", json=profile_json)
        return validate_response(response)

    def edit(self, source_key, key, profile_json):
        """Use the api to add a new profile using profile_data."""
        profile_json['source_key'] = validate_key("Source", source_key)
        profile_json['key'] = validate_key("Profile", key)
        response = self.client.put("profile/indexing", json=profile_json)
        return validate_response(response)

    def get(self, source_key, key=None, reference=None, email=None):
        """
        Retrieve the interpretability information.

        Args:
            source_key:             <string>
                                    source_key
            key:                    <string>
                                    key
            reference:              <string>
                                    profile_reference
            email:                  <string>
                                    profile_email

        Returns
            Get information

        """
        query_params = format_item_payload('profile', source_key, key, reference, email)
        response = self.client.get('profile/indexing', query_params)
        return validate_response(response)

    def archive(self, source_key, key=None, reference=None, email=None):
        """
        Archive Profile.

        Args:
            source_key:             <string>
                                    source_key
            key:                    <string>
                                    key
            reference:              <string>
                                    profile_reference
            email:                  <string>
                                    profile_email

        Returns
            Archive profile

        """
        payload = format_item_payload('profile', source_key, key, reference, email)
        response = self.client.patch("profile/indexing/archive", json=payload)
        return validate_response(response)
