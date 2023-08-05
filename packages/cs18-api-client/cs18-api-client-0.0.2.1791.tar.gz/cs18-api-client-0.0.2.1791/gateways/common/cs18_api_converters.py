from typing import List, Optional
from datetime import datetime
import dateutil.parser
from gateways.common.cs18_api_classes import AccessLink
from gateways.common.cs18_api_errors import SandboxError, Error
from gateways.common.cs18_api_requests import AwsCloudProviderSettingsModel
from gateways.common.cs18_api_responses import (
    SpaceAdmin,
    SpaceCloudAccount,
    GetSpacesResponse,
    CatalogForGetResponse,
    CatalogForGetAllResponse,
    BlueprintResponse,
    CloudAccountResponse,
    BlueprintInputResponse,
    SandboxResponse,
    ProductionBlueResponse, ProductionGreenResponse,
    SandboxOwnerResponse,
    SandboxResponseLean,
    ProductionResponseLean,
    CloudResponse,
    ApplicationResponse,
    ApplicationResponseLean,
    AppInstanceResponse,
    HyperlinkResponse,
    BlueprintApplicationResponse,
    BlueprintRegionResponse,
    BlueprintCloudResponse,
    TokenResponse,
    CatalogApplicationResponse,
    UserPermittedToSpaceResponse,
    SourceControlDetailsResponse,
    BlueprintFileResponse,
    UserInvitationResponse,
    RepositoryResponse,
    InputResponse,
    RoleListItemResponse,
    AccountStatusResponse,
    ArtifactRepoCreatedUser,
    AccountStatusUserDetails,
    ArtifactRepoResponse,
    UserForAllUsersResponse,
    ServiceResponse,
    BlueprintServiceResponse,
    LaunchingProgress, LaunchingProgressStep, CloudAccountInSpaceResponse, CloudAccountConnectivityResponse,
    CloudAccountInfraSetResponse, CloudAccountSubnetsResponse, RegionResponse, GetImagesResponse,
    VerifyCloudProviderResponse, VerifyCloudProviderResourceResponse, AccountRepositoryResponse,
    BlueprintValidationResponse, BlueprintSourceResponse, CloudAccountCostResponse,
    ComputeServiceInAccountResponse, ComputeServiceInSpaceResponse, ComputeServiceSpaceSpecResponse,
    K8SComputeServiceSpaceInfraSettingsResponse, BlueprintComputeServiceResponse,
    AccountRepositoryDetailsBranchResponse, AccountRepositoryDetailsResponse,
    SpaceRepositoryResponse, DirectAwsSshResponse, DirectAzureSshResponse, DirectRdpResponse, ParameterStoreItem,
    ParameterStoreValue, ParameterStoreOrigin, LiteralValue, AwsSsmValue)


class Converters:
    """
    Converts provided dictionaries into requested Response objects
    """

    @staticmethod
    def create_spaces_response(space: dict):
        admins = [
            SpaceAdmin(
                first_name=admin["first_name"],
                last_name=admin["last_name"],
                account_role=admin["account_role"],
            )
            for admin in space["admins"]
        ]
        space_cloud_accounts = [
            SpaceCloudAccount(
                name=cloud_account["name"], cloud_account_type=cloud_account["type"]
            )
            for cloud_account in space["cloud_accounts"]
        ]
        return GetSpacesResponse(
            name=space["name"],
            admins=admins,
            users_count=space["users_count"],
            cloud_accounts=space_cloud_accounts,
        )

    @staticmethod
    def create_catalog_blueprint_full_response(catalog: dict) -> CatalogForGetResponse:
        """
        Returns CatalogForGetResponse based on provided dictionary
        :param catalog: dict
        :return: CatalogForGetResponse
        """
        return CatalogForGetResponse(
            name=catalog["blueprint_name"],
            description=catalog["description"],
            url=catalog["url"],
            last_modified=catalog["last_modified"],
            modified_by=catalog["modified_by"],
            clouds=catalog["clouds"] if catalog["clouds"] else [],
            applications=[
                Converters._create_catalog_app_response(app)
                for app in catalog["applications"]
            ]
            if catalog["applications"]
            else [],
            links=[Converters._create_link_response(link) for link in catalog["links"]]
            if catalog["links"]
            else [],
            artifacts=catalog.get("artifacts", {}),
            errors=catalog.get("errors"),
        )

    @staticmethod
    def create_catalog_blueprint_response(catalog: dict) -> CatalogForGetAllResponse:
        """
        Returns CatalogForGetAllResponse based on provided dictionary
        :param catalog: dict
        :return: CatalogForGetAllResponse
        """
        return CatalogForGetAllResponse(
            name=catalog["blueprint_name"],
            description=catalog["description"],
            url=catalog["url"],
            last_modified=catalog["last_modified"],
            modified_by=catalog["modified_by"],
            clouds=catalog["clouds"] if catalog["clouds"] else [],
            links=[Converters._create_link_response(link) for link in catalog["links"]]
            if catalog["links"]
            else [],
            artifacts=catalog.get("artifacts", {}),
            errors=catalog.get("errors"),
        )

    @staticmethod
    def create_artifact_repo_response(obj: dict) -> ArtifactRepoResponse:
        created_by_json = obj["created_by"]
        return ArtifactRepoResponse(
            obj["type"],
            dateutil.parser.parse(obj["created_date"]),
            obj["location"],
            ArtifactRepoCreatedUser(
                created_by_json["email"],
                created_by_json["first_name"],
                created_by_json["last_name"],
            ),
        )

    @staticmethod
    def create_blueprint_validation_response(blueprint: dict) -> BlueprintValidationResponse:
        return BlueprintValidationResponse(
            name=blueprint["blueprint_name"],
            description=blueprint["description"],
            url=blueprint["url"],
            source=Converters.create_blueprint_validation_source_response(blueprint.get("source")),
            artifacts=blueprint.get("artifacts", {}),
            inputs=[Converters._create_blueprint_input_response(i) for i in blueprint.get("inputs") or []],
            errors=[Error(e) for e in blueprint["errors"]],
            services=[Converters._create_blueprint_service_response(x) for x in blueprint.get("services") or []],
            applications=[Converters._create_blueprint_app_response(x) for x in blueprint.get("applications") or []],
            clouds=[Converters._create_blueprint_cloud_response(cloud) for cloud in blueprint.get("clouds") or []]
        )

    @staticmethod
    def create_blueprint_validation_source_response(source: dict) -> Optional[BlueprintSourceResponse]:
        if not source:
            return None
        return BlueprintSourceResponse(
            branch=source.get("branch"),
            commit=source.get("commit")
        )

    @staticmethod
    def create_blueprint_response(blueprint: dict) -> BlueprintResponse:
        """
        Returns BlueprintResponse based on provided dictionary
        :param blueprint: dict
        :return: BlueprintResponse
        """
        return BlueprintResponse(
            name=blueprint["blueprint_name"],
            description=blueprint["description"],
            url=blueprint["url"],
            enabled=blueprint["enabled"],
            last_modified=blueprint["last_modified"],
            is_sample=blueprint["is_sample"],
            modified_by=blueprint["modified_by"],
            clouds=[
                Converters._create_blueprint_cloud_response(cloud)
                for cloud in blueprint["clouds"]
            ]
            if blueprint["clouds"]
            else [],
            applications=[
                Converters._create_blueprint_app_response(app)
                for app in blueprint["applications"]
            ]
            if blueprint["applications"]
            else [],
            links=[
                Converters._create_link_response(link) for link in blueprint["links"]
            ],
            artifacts=blueprint.get("artifacts", {}),
            inputs=[
                Converters._create_blueprint_input_response(i)
                for i in blueprint.get("inputs", [])
            ],
            errors=[Error(e) for e in blueprint["errors"]],
            services=[
                Converters._create_blueprint_service_response(app)
                for app in blueprint["services"]
            ]
            if blueprint["services"]
            else []
        )

    @staticmethod
    def _create_cloud_account_cost_response(cloud_account: dict) -> CloudAccountCostResponse:
        cost: dict = cloud_account.get('cost')
        if not cost:
            return CloudAccountCostResponse(None)

        return CloudAccountCostResponse(
            Converters._parse_datetime(cost.get("last_update")))

    @staticmethod
    def _create_errors(cloud_account: dict) -> List[Error]:
        errors: List[dict] = cloud_account.get('errors', [])
        return [Error(e) for e in errors]

    @staticmethod
    def _create_compute_services_in_account_response(
            cloud_compute_services: List[dict]
    ) -> List[ComputeServiceInAccountResponse]:
        compute_services = [
            ComputeServiceInAccountResponse(
                name=compute_service.get("name", None),
                service_type=compute_service.get("type", None),
                created_date=Converters._parse_datetime(compute_service.get("created_date", None)),
                created_by=compute_service.get("created_by", None),
                user_defined=compute_service.get("user_defined", None),
                status=compute_service.get("status", None),
                spaces=compute_service.get("spaces", [])
            )
            for compute_service in cloud_compute_services
        ]
        return compute_services

    @staticmethod
    def _create_compute_services_in_space_response(
            cloud_compute_services: List[dict]
    ) -> List[ComputeServiceInSpaceResponse]:
        compute_services = [
            ComputeServiceInSpaceResponse(
                name=compute_service.get("name", None),
                service_type=compute_service.get("type", None),
                created_date=Converters._parse_datetime(compute_service.get("created_date", None)),
                created_by=compute_service.get("created_by", None),
                user_defined=compute_service.get("user_defined", None),
                status=compute_service.get("status", None),
                spec=Converters._create_compute_service_space_spec_response(compute_service.get("spec"))
            )
            for compute_service in cloud_compute_services
        ]
        return compute_services

    @staticmethod
    def _create_compute_service_space_spec_response(spec: dict) -> Optional[ComputeServiceSpaceSpecResponse]:
        if spec is None:
            return None
        return ComputeServiceSpaceSpecResponse(
            kubernetes=Converters._create_k8s_compute_service_space_infra_settings_response(spec.get("kubernetes"))
        )

    @staticmethod
    def _create_k8s_compute_service_space_infra_settings_response(kubernetes: dict) \
            -> Optional[K8SComputeServiceSpaceInfraSettingsResponse]:
        if kubernetes is None:
            return None
        return K8SComputeServiceSpaceInfraSettingsResponse(
            namespace=kubernetes.get("namespace"),
            internet_facing=kubernetes.get("internet_facing")
        )

    @staticmethod
    def create_cloud_account_response(cloud: dict) -> CloudAccountResponse:
        """
        Returns CloudAccountResponse based on provided dictionary
        :param cloud: dict
        :return: CloudAccountResponse
        """
        return CloudAccountResponse(
            name=cloud["name"],
            provider=cloud["type"],
            created_date=Converters._parse_datetime(cloud.get("created_date")),
            created_by=cloud["created_by"],
            spaces=cloud["spaces"],
            compute_services=Converters._create_compute_services_in_account_response(
                cloud.get("compute_services", None)
            ),
            cost=Converters._create_cloud_account_cost_response(cloud),
            errors=Converters._create_errors(cloud)
        )

    @staticmethod
    def create_cloud_account_in_space_response(cloud: dict) -> CloudAccountInSpaceResponse:
        """
        Returns CloudAccountResponse based on provided dictionary
        :param cloud: dict
        :return: CloudAccountResponse
        """
        return CloudAccountInSpaceResponse(
            name=cloud["name"],
            provider=cloud["type"],
            created_date=Converters._parse_datetime(cloud.get("created_date")),
            created_by=cloud["created_by"],
            internet_facing=cloud["internet_facing"],
            connectivity=Converters._create_cloud_account_connectivity_response(cloud.get("connectivity")),
            compute_services=Converters._create_compute_services_in_space_response(
                cloud.get("compute_services", None)
            ),
            cost=Converters._create_cloud_account_cost_response(cloud),
            errors=Converters._create_errors(cloud)
        )

    @staticmethod
    def _create_cloud_account_connectivity_response(conn: dict) -> Optional[CloudAccountConnectivityResponse]:
        if not conn:
            return None

        return CloudAccountConnectivityResponse(
            existing_infra=conn.get("existing_infra"),
            existing_infra_sets=[CloudAccountInfraSetResponse(
                region=infra_set["region"],
                virtual_network=infra_set["virtual_network"],
                subnets=CloudAccountSubnetsResponse(
                    gateway_subnet=infra_set["subnets"].get("gateway_subnet"),
                    management_subnet=infra_set["subnets"].get("management_subnet"),
                    application_subnets=infra_set["subnets"].get("application_subnets")
                ) if "subnets" in infra_set else None) for infra_set in conn.get("existing_infra_sets")]
            if "existing_infra_sets" in conn else None)

    @staticmethod
    def _create_blueprint_input_response(
            blueprint_input: dict
    ) -> BlueprintInputResponse:
        return BlueprintInputResponse(
            name=blueprint_input["name"],
            default_value=blueprint_input.get("default_value"),
            display_style=blueprint_input.get("display_style"),
            optional=blueprint_input.get("optional", False),
            description=blueprint_input.get("description"),
        )

    @staticmethod
    def create_sandbox_response(sandbox: dict) -> SandboxResponse:
        """
        Returns SandboxResponse based on provided dictionary
        :param sandbox: dict
        :return: SandboxResponse
        """
        return SandboxResponse(
            sandbox_id=sandbox["id"],
            blueprint=sandbox["blueprint_name"],
            applications=[
                Converters._create_app_response(service)
                for service in sandbox["applications"]
            ]
            if sandbox["applications"]
            else [],
            services=[
                Converters._create_service_response(s)
                for s in sandbox.get("services", [])
            ],
            inputs=Converters._create_sandbox_inputs(sandbox.get("inputs")),
            artifacts=sandbox.get("artifacts"),
            automation=sandbox["automation"],
            start_time=sandbox["deployment_start_time"],
            create_time=sandbox["create_time"],
            status_details=sandbox["status_details"],
            sandbox_status=sandbox["sandbox_status"],
            status_error_description=sandbox["status_error_description"],
            links=[Converters._create_link_response(link) for link in sandbox["links"]]
            if sandbox["links"]
            else [],
            owner=Converters._create_sandbox_owner(sandbox["owner"])
            if sandbox["owner"]
            else [],
            errors=[
                Converters._create_sandbox_error(error)
                for error in sandbox.get("errors", [])
            ],
            scheduled_end_time=dateutil.parser.parse(sandbox["scheduled_end_time"])
            if sandbox.get("scheduled_end_time", None) else None,
            end_time=dateutil.parser.parse(sandbox["end_time"])
            if sandbox.get("end_time", None) else None,
            debugging_service=sandbox.get('debugging_service'),
            launching_progress=Converters._create_launching_progress(sandbox.get('launching_progress')),
            source=Converters._create_source(sandbox.get('source')),
            direct_access=sandbox.get('direct_access', 'off')
        )

    @staticmethod
    def create_production_blue_response(production: dict) -> ProductionBlueResponse:
        """
        Returns ProductionBlueResponse based on provided dictionary
        :param production: dict
        :return: ProductionBlueResponse
        """
        return ProductionBlueResponse(
            production_id=production["id"],
            sandbox_id=production["sandbox_id"],
            name=production["name"],
            owner=Converters._create_sandbox_owner(production["owner"]),
            blueprint_name=production["blueprint_name"],
            blueprint_description=production["blueprint_description"],
            build=production["build"],
            applications=[
                Converters._create_app_response(app)
                for app in production.get("applications", [])
            ],
            services=[
                Converters._create_service_response(s)
                for s in production.get("services", [])
            ],
            inputs=Converters._create_sandbox_inputs(production.get("inputs")),
            artifacts=production.get("artifacts"),
            deployment_start_time=Converters._parse_datetime(
                production.get("deployment_start_time")
            ),
            create_time=Converters._parse_datetime(production.get("create_time")),
            status_details=production["status_details"],
            production_status=production["production_status"],
            update_status=production["update_status"],
            links=[
                Converters._create_link_response(link)
                for link in production.get("links") or []
            ],
            errors=[
                Converters._create_sandbox_error(error)
                for error in production.get("errors") or []
            ],
            status_error_description=production["status_error_description"],
            has_green=production["has_green"],
            debugging_service=production.get('debugging_service'),
            launching_progress=Converters._create_launching_progress(production.get('launching_progress')),
            direct_access=production.get('direct_access', 'off')
        )

    @staticmethod
    def create_production_green_response(production: dict) -> ProductionGreenResponse:
        """
        Returns ProductionGreenResponse based on provided dictionary
        :param production: dict
        :return: ProductionGreenResponse
        """
        return ProductionGreenResponse(
            production_id=production["id"],
            sandbox_id=production["sandbox_id"],
            name=production["name"],
            owner=Converters._create_sandbox_owner(production["owner"]),
            blueprint_name=production["blueprint_name"],
            blueprint_description=production["blueprint_description"],
            build=production["build"],
            applications=[Converters._create_app_response(app) for app in production.get("applications", [])],
            services=[
                Converters._create_service_response(s)
                for s in production.get("services", [])
            ],
            inputs=Converters._create_sandbox_inputs(production.get("inputs")),
            artifacts=production.get("artifacts"),
            deployment_start_time=Converters._parse_datetime(production.get("deployment_start_time")),
            create_time=Converters._parse_datetime(production.get("create_time")),
            status_details=production["status_details"],
            production_status=production["production_status"],
            update_status=production["update_status"],
            links=[Converters._create_link_response(link) for link in production.get("links") or []],
            errors=[Converters._create_sandbox_error(error) for error in production.get("errors") or []],
            status_error_description=production["status_error_description"],
            exposure=production["exposure"],
            debugging_service=production.get('debugging_service'),
            launching_progress=Converters._create_launching_progress(production.get('launching_progress')),
            direct_access=production.get('direct_access', 'off')
        )

    @staticmethod
    def _create_sandbox_owner(user: dict) -> Optional[SandboxOwnerResponse]:
        if not user:
            return None

        return SandboxOwnerResponse(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            join_date=user["join_date"],
        )

    @staticmethod
    def _create_sandbox_error(sandbox_error: dict) -> SandboxError:
        return SandboxError(
            time=sandbox_error["time"],
            code=sandbox_error["code"],
            message=sandbox_error["message"],
        )

    @staticmethod
    def _create_source(source: dict) -> Optional[BlueprintSourceResponse]:
        if not source:
            return None
        return BlueprintSourceResponse(branch=source.get('branch'), commit=source.get('commit'))

    @staticmethod
    def create_sandbox_response_list_item(sandbox: dict) -> SandboxResponseLean:
        """
        Returns SandboxResponseLean based on provided dictionary
        :param sandbox: dict
        :return: SandboxResponseLean
        """
        return SandboxResponseLean(
            sandbox_id=sandbox["id"],
            blueprint=sandbox["blueprint_name"],
            applications=[
                Converters._create_application_response_lean(application)
                for application in sandbox["applications"]
            ]
            if sandbox["applications"]
            else [],
            services=[
                Converters._create_service_response(s)
                for s in sandbox.get("services", [])
            ],
            automation=sandbox["automation"],
            start_time=sandbox["deployment_start_time"],
            create_time=sandbox["create_time"],
            status_details=sandbox["status_details"],
            sandbox_status=sandbox["sandbox_status"],
            status_error_description=sandbox["status_error_description"],
            links=[Converters._create_link_response(link) for link in sandbox["links"]]
            if sandbox["links"]
            else [],
            owner=Converters._create_sandbox_owner(sandbox["owner"])
            if sandbox["owner"]
            else [],
            name=sandbox["name"],
            errors=[
                Converters._create_sandbox_error(error)
                for error in sandbox.get("errors", [])
            ],
            scheduled_end_time=dateutil.parser.parse(sandbox["scheduled_end_time"]) if sandbox.get(
                "scheduled_end_time") else None,
            end_time=dateutil.parser.parse(sandbox["end_time"]) if sandbox.get("end_time") else None,
            debugging_service=sandbox.get("debugging_service"),
            source=Converters._create_source(sandbox.get('source')),
            direct_access=sandbox.get('direct_access', 'off')
        )
 
    @staticmethod
    def create_production_response_list_item(
            production: dict
    ) -> ProductionResponseLean:
        """
        Returns ProductionResponseLean based on provided dictionary
        :param production: dict
        :return: ProductionResponseLean
        """
        return ProductionResponseLean(
            production_id=production["id"],
            name=production["name"],
            blueprint_description=production["blueprint_description"],
            blue_status=production["blue_status"],
            green_status=production["green_status"],
            update_strategy=production["update_strategy"],
            update_status=production["update_status"],
            create_time=Converters._parse_datetime(production.get("create_time")),
            deployment_start_time=Converters._parse_datetime(production.get("deployment_start_time")),
            blue_applications=[Converters._create_application_response_lean(x)
                               for x in production.get("blue_applications") or {}],
            blue_services=[Converters._create_service_response(s) for s in production.get("services", [])],
            direct_access=production.get('direct_access', 'off')
        )

    @staticmethod
    def _create_cloud_response(service: dict) -> CloudResponse:
        cloud_account_name = service.get("cloud_account_name")
        region_id = ""
        region_name = ""
        if "region" in service:
            region_id = service.get("region").get("id")
            region_name = service.get("region").get("name")
        return CloudResponse(
            cloud_account_name=cloud_account_name,
            region_id=region_id,
            region_name=region_name
        )

    @staticmethod
    def _create_app_response(application: dict) -> ApplicationResponse:
        return ApplicationResponse(
            name=application["name"],
            shortcuts=application["shortcuts"],
            status=application["status"],
            instances=[
                Converters._create_instance_response(instance)
                for instance in application["instances"]
            ],
            private_address=application["private_address"],
            public_address=application["public_address"],
            internal_ports=application["internal_ports"],
            external_ports=application["external_ports"],
            internal_dns=application["internal_dns"],
            image_name=application["image_name"],
            cloud=Converters._create_cloud_response(application.get("cloud")),
            icon=application.get("icon")

            if application.get("cloud")
            else None,
            direct_access_protocols=application.get("direct_access_protocols", [])
        )

    @staticmethod
    def _create_application_response_lean(application: dict) -> ApplicationResponseLean:
        return ApplicationResponseLean(
            name=application["name"],
            status=application["status"],
            cloud=Converters._create_cloud_response(application.get("cloud"))
            if application.get("cloud")
            else None,
        )

    @staticmethod
    def _create_instance_response(instance: dict) -> AppInstanceResponse:
        access_links = None
        if "access_links" in instance and instance["access_links"] is not None:
            access_links = [
                Converters._create_access_link(al) for al in instance["access_links"]
            ]

        return AppInstanceResponse(
            private_ip=instance["private_ip"],
            infra_id=instance["infra_id"],
            instance_type=instance["instance_type"],
            memory_limit=instance["memory_limit"],
            cpu_limit=instance["cpu_limit"],
            deployment_status=instance["status"],
            access_links=access_links,
            links=[Converters._create_link_response(link) for link in instance["links"]]
            if instance["links"]
            else [],
        )

    @staticmethod
    def _create_access_link(access_link_json: dict) -> AccessLink:
        return AccessLink(
            protocol=access_link_json["protocol"], link=access_link_json["link"]
        )

    @staticmethod
    def _create_link_response(link: dict) -> HyperlinkResponse:
        return HyperlinkResponse(
            rel=link["rel"], href=link["href"], method=link["method"]
        )

    @staticmethod
    def _create_blueprint_app_response(app: dict) -> BlueprintApplicationResponse:

        return BlueprintApplicationResponse(name=app["name"], version=app["version"])

    @staticmethod
    def _create_blueprint_service_response(service: dict) -> BlueprintServiceResponse:

        return BlueprintServiceResponse(name=service["name"], service_type=service["type"])

    @staticmethod
    def _create_blueprint_cloud_region_response(
            region: dict
    ) -> BlueprintRegionResponse:
        if not region:
            return BlueprintRegionResponse("", "")
        return BlueprintRegionResponse(
            region_id=region.get("id", ""), name=region.get("name", "")
        )

    @staticmethod
    def _create_blueprint_cloud_response(cloud):
        if isinstance(cloud, str):
            return cloud
        return BlueprintCloudResponse(
            cloud_account_name=cloud.get("cloud_account_name"),
            provider=cloud.get("provider"),
            region=Converters._create_blueprint_cloud_region_response(
                cloud.get("region")
            ),
            compute_service=Converters._create_blueprint_compute_service(cloud.get("compute_service"))
        )

    @staticmethod
    def create_token_response(link: dict) -> TokenResponse:
        """
        Returns TokenResponse based on provided dictionary
        :param link: dict
        :return: TokenResponse
        """
        return TokenResponse(
            access_token=link["access_token"],
            refresh_token=link["refresh_token"],
            token_type=link["token_type"],
            expires_in=link["expires_in"],
        )

    @staticmethod
    def _create_catalog_app_response(app: dict) -> CatalogApplicationResponse:
        return CatalogApplicationResponse(name=app["name"], version=app["version"])

    @staticmethod
    def create_user_permitted_to_space_response(
            user: dict
    ) -> UserPermittedToSpaceResponse:
        """
        Returns UserPermittedToSpaceResponse based on provided dictionary
        :param user: dict
        :return: UserPermittedToSpaceResponse
        """
        return UserPermittedToSpaceResponse(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            join_date=user["join_date"],
            space_role=user["space_role"],
            account_role=user["account_role"],
            has_access_to_all_spaces=user["has_access_to_all_spaces"]
        )

    @staticmethod
    def create_user_for_all_users_response(
            user: dict
    ) -> UserForAllUsersResponse:
        """
        Returns UserForAllUsersResponse based on provided dictionary
        :param user: dict
        :return: UserForAllUsersResponse
        """
        return UserForAllUsersResponse(
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            join_date=user["join_date"],
            account_role=user["account_role"],
            has_access_to_all_spaces=user["has_access_to_all_spaces"],
            member_in_spaces=user["member_in_spaces"]
        )

    @staticmethod
    def _create_source_control_details_response(
            source_control: dict
    ) -> SourceControlDetailsResponse:
        return SourceControlDetailsResponse(
            branch_name=source_control["branch_name"],
            latest_commit_id=source_control["latest_commit_id"],
            changed_by=source_control["changed_by"],
            changed_date=dateutil.parser.parse(source_control["change_date"]),
        )

    @staticmethod
    def create_blueprint_file_response(file: dict) -> BlueprintFileResponse:
        """
        Returns BlueprintFileResponse based on provided dictionary
        :param file: dict
        :return: BlueprintFileResponse
        """
        return BlueprintFileResponse(
            url=file["url"],
            kind=file["kind"],
            content=file["content"],
            source_control_details=Converters._create_source_control_details_response(
                file["source_control_details"]
            ),
            icon=file.get("icon"),
        )

    @staticmethod
    def create_user_invitation_response(invite: dict) -> UserInvitationResponse:
        """
        Returns UserInvitationResponse based on provided dictionary
        :param invite: dict
        :return: UserInvitationResponse
        """
        return UserInvitationResponse(
            email=invite["email"],
            send_date=invite["send_date"],
            account_role=invite["account_role"],
            space_name=invite["space_name"],
            space_role=invite["space_role"],
        )

    @staticmethod
    def create_repository_response(repo: dict) -> RepositoryResponse:
        """
        Returns RepositoryResponse based on provided dictionary
        :param repo: dict
        :return: RepositoryResponse
        """
        return RepositoryResponse(
            repository_url=repo["repository_url"],
            errors=[Error(e) for e in repo["errors"]],
        )

    @staticmethod
    def create_role_list_item_response(role: dict) -> RoleListItemResponse:
        return RoleListItemResponse(name=role["name"])

    @staticmethod
    def _create_sandbox_inputs(response_inputs: dict) -> List[InputResponse]:
        inputs = []
        if response_inputs:
            for request_input in response_inputs:
                inputs.append(
                    InputResponse(
                        name=request_input["name"],
                        value=request_input["value"],
                        description=request_input["description"],
                        display_style=request_input["display_style"],
                        optional=request_input.get("optional", False),
                    )
                )
        return inputs

    @staticmethod
    def create_account_status_response(obj: dict):
        return AccountStatusResponse(
            obj["onboarding_status"],
            Converters._parse_datetime(obj["license_expiration_date"]),
            obj["ignore_expiration_date"],
            obj["suspended_reason"],
            obj["salesforce_account_id"],
            obj["plan_id"],
            AccountStatusUserDetails(obj["user_details"]),
        )

    @staticmethod
    def _parse_datetime(value: str) -> datetime:
        if value:
            return dateutil.parser.parse(value)
        return None

    @staticmethod
    def _create_service_response(service: dict) -> ServiceResponse:
        return ServiceResponse(
            name=service["name"],
            status=service["status"],
            service_type=service["type"]
        )

    @staticmethod
    def _create_launching_progress(progress: dict) -> Optional[LaunchingProgress]:
        if not progress:
            return None
        return LaunchingProgress(
            creating_infrastructure=Converters._create_launching_progress_step(progress.get('creating_infrastructure')),
            preparing_artifacts=Converters._create_launching_progress_step(progress.get('preparing_artifacts')),
            deploying_applications=Converters._create_launching_progress_step(progress.get('deploying_applications')),
            verifying_environment=Converters._create_launching_progress_step(progress.get('verifying_environment')))

    @staticmethod
    def _create_launching_progress_step(step: dict) -> LaunchingProgressStep:
        return LaunchingProgressStep(
            total=step['total'],
            succeeded=step['succeeded'],
            failed=step['failed'],
            status=step['status'])

    @staticmethod
    def create_space_cloud_account_regions_response(region: dict) -> RegionResponse:
        return RegionResponse(region["id"], region["name"])

    @staticmethod
    def get_image_response(images: dict):
        return GetImagesResponse(images['image_id'], images['image_name'])

    @staticmethod
    def _create_resources_summary_response(resources_summary: dict) -> List[VerifyCloudProviderResourceResponse]:
        resources = []
        if resources_summary:
            for resource in resources_summary:
                resources.append(
                    VerifyCloudProviderResourceResponse(
                        resource_type=resource["resource_type"],
                        resource_name=resource["resource_name"],
                        resource_id=resource["resource_id"],
                        resource_status=resource["resource_status"],
                        resource_valid=resource["resource_valid"]
                    )
                )
        return resources

    @staticmethod
    def create_verify_response(verify: dict) -> VerifyCloudProviderResponse:
        return VerifyCloudProviderResponse(
            success=verify["success"],
            resources_summary=Converters._create_resources_summary_response(verify["resources_summary"]),
        )

    @staticmethod
    def create_account_repository_response(data: dict) -> AccountRepositoryResponse:
        return AccountRepositoryResponse(name=data['name'],
                                         allow_sharing=data['allow_sharing'],
                                         open_access=data['open_access'],
                                         repository_url=data['repository_url'],
                                         repository_type=data['repository_type'],
                                         errors=[Error(e) for e in data["errors"]])

    @staticmethod
    def create_account_repository_details_branch_response(data: dict) -> AccountRepositoryDetailsBranchResponse:
        return AccountRepositoryDetailsBranchResponse(name=data['name'])

    @staticmethod
    def create_account_repository_details_response(data: dict) -> AccountRepositoryDetailsResponse:
        return AccountRepositoryDetailsResponse(repository_name=data['name'],
                                                repository_full_name=data['full_name'],
                                                default_branch=data['default_branch'],
                                                branches=[AccountRepositoryDetailsBranchResponse(b)
                                                          for b in data["branches"]])

    @staticmethod
    def _create_blueprint_compute_service(compute_service: dict) -> BlueprintComputeServiceResponse:
        return BlueprintComputeServiceResponse(
            name=compute_service.get("name", None),
            service_type=compute_service.get("type", None),
            created_date=Converters._parse_datetime(compute_service.get("created_date", None)),
            created_by=compute_service.get("created_by", None),
            user_defined=compute_service.get("user_defined", None)
        )

    @staticmethod
    def create_space_repository_response(data: dict) -> SpaceRepositoryResponse:
        return SpaceRepositoryResponse(repository_name=data['name'],
                                       repository_type=data['repository_type'],
                                       repository_url=data['repository_url'],
                                       branch=data['branch'])

    @staticmethod
    def create_direct_aws_ssh_response(data: dict) -> DirectAwsSshResponse:
        return DirectAwsSshResponse(
            connection=data["connection"],
            pem_file_url=data["pem_file_url"])

    @staticmethod
    def create_direct_azure_ssh_response(data: dict) -> DirectAzureSshResponse:
        return DirectAzureSshResponse(
            connection=data["connection"],
            password=data["password"])

    @staticmethod
    def create_direct_rdp_response(data: dict) -> DirectRdpResponse:
        return DirectRdpResponse(
            rdp_file_url=data["rdp_file_url"],
            username=data["username"],
            password=data["password"])

    @staticmethod
    def create_parameter_value_response(origin: str, raw_parameter_value: dict) -> ParameterStoreValue:
        if origin == ParameterStoreOrigin.Literal:
            return LiteralValue(content=raw_parameter_value["content"])
        if origin == ParameterStoreOrigin.AwsSsm:
            return AwsSsmValue(path=raw_parameter_value["path"])

        return None

    @staticmethod
    def create_get_all_parameters_response(data: dict) -> List[ParameterStoreItem]:
        parameters = []
        if data:
            for parameter in data:
                parameters.append(
                    ParameterStoreItem(
                        name=parameter["name"],
                        origin=parameter["origin"],
                        value=Converters.create_parameter_value_response(parameter["origin"], parameter["value"]),
                        description=parameter["description"])
                )
        return parameters

    @staticmethod
    def create_get_parameter_response(data: dict) -> Optional[ParameterStoreItem]:
        parameter = None
        if data:
            parameter = ParameterStoreItem(
                name=data["name"],
                origin=data["origin"],
                value=Converters.create_parameter_value_response(data["origin"], data["value"]),
                description=data["description"])
        return parameter

    @staticmethod
    def aws_cloud_provider_settings_model(data: dict) -> AwsCloudProviderSettingsModel:
        return AwsCloudProviderSettingsModel(
            sidecar_image_param_name=data.get("sidecar_image_param_name", None)
        )
