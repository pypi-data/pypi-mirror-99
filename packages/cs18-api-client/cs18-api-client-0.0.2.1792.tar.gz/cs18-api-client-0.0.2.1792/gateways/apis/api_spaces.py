from gateways.apis.api_base_class import ApiBase


class ApiSpaces(ApiBase):
    def spaces(self):
        return self.build_route("spaces")

    def space_by_name(self, space_name: str):
        return self.build_route("spaces/{space_name}".format(**locals()))

    def get_images(self, space_name: str, cloud_account_name: str, region_id: str):
        return self.build_route("spaces/{space_name}/cloud_accounts/AWS/{cloud_account_name}/regions/{region_id}/private_images"
                                .format(**locals()))

    def space_users(self, space_name: str):
        """Astronauts"""
        return self.build_route("spaces/{space_name}/users".format(**locals()))

    def space_repositories(self, space_name: str, repository_type: str = None):
        if repository_type is None:
            return self.build_route("spaces/{space_name}/repositories".format(**locals()))
        if repository_type == 'bitbucket':
            return self.space_bitbucket_repositories(space_name)

        return self.space_github_repositories(space_name)

    def space_cloud_accounts(self, space_name: str):
        return self.build_route("spaces/{space_name}/cloud_accounts".format(**locals()))

    def space_cloud_account(self, space_name: str, cloud_account: str):
        return self.build_route(
            "spaces/{space_name}/cloud_accounts/{cloud_account}".format(**locals())
        )

    def space_cloud_account_compute_services(self, space_name: str, cloud_account: str):
        return self.build_route(
            "spaces/{space_name}/cloud_accounts/{cloud_account}/compute_services".format(**locals())
        )

    def space_cloud_account_compute_service(self, space_name: str, cloud_account: str, compute_service: str):
        return self.build_route(
            "spaces/{space_name}/cloud_accounts/{cloud_account}/compute_services/{compute_service}".format(**locals())
        )

    def space_github_repositories(self, space_name: str):
        return self.build_route(
            "spaces/{space_name}/repositories/github".format(**locals())
        )

    def space_bitbucket_repositories(self, space_name: str):
        return self.build_route(
            "spaces/{space_name}/repositories/bitbucket".format(**locals())
        )

    def user_permissions(self, space_name: str):
        return self.build_route("spaces/{space_name}/user_permissions".format(**locals()))

    def space_user(self, space_name: str, user_email: str):
        return self.build_route("spaces/{space_name}/users/{user_email}".format(**locals()))

    def user_space_role(self, space_name: str, user_email: str, space_role_name: str):
        return self.build_route(
            "spaces/{space_name}/users/{user_email}/space_role?value={space_role_name}".format(**locals())
        )

    def space_cloud_account_regions(self, space_name: str, cloud_account_name: str):
        return self.build_route(
            "spaces/{space_name}/cloud_accounts/{cloud_account_name}/regions".format(**locals())
        )

    def space_sandbox_repository(self, space_name):
        return self.build_route(
            "spaces/{space_name}/sandbox_repository".format(**locals())
        )

    def space_production_repository(self, space_name):
        return self.build_route(
            "spaces/{space_name}/production_repository".format(**locals())
        )
