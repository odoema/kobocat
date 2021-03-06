# -*- coding: utf-8 -*-
import logging
import requests

from django.conf import settings
from onadata.apps.restservice.RestServiceInterface import RestServiceInterface
from onadata.apps.logger.models import Instance


class ServiceDefinition(RestServiceInterface):
    id = u"kpi_hook"
    verbose_name = u"KPI Hook POST"

    def send(self, endpoint, data):

        post_data = {
            "instance_id": data.get("instance_id")  # Will be used internally by KPI to fetch data with KoboCatBackend
        }
        headers = {"Content-Type": "application/json"}

        # Verify if endpoint starts with `/assets/` before sending the request to`kpi`
        if endpoint.startswith(settings.KPI_HOOK_ENDPOINT_PATTERN[:8]):
            # Build the url in the service to avoid saving hardcoded domain name in the DB
            url = "{}{}".format(
                settings.KPI_INTERNAL_URL,
                endpoint
            )
            response = requests.post(url, headers=headers, json=post_data)
            response.raise_for_status()

            # Save successful
            Instance.objects.filter(pk=data.get("instance_id")).update(posted_to_kpi=True)
        else:
            logging.warning('This endpoint: `{}` is not valid for `KPI Hook`')
