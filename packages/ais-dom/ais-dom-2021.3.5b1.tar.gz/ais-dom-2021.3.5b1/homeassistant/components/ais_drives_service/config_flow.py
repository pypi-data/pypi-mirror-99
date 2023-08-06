"""Config flow to configure the AIS Drive Service component."""

import asyncio
import logging
import time

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_EMAIL,
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_TYPE,
    CONF_USERNAME,
)
from homeassistant.core import callback
from homeassistant.util import slugify

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
DRIVE_NAME_INPUT = None
DRIVE_TYPE_INPUT = None
AUTH_URL = None
G_DRIVE_CREATION_TIME_CALL = None


@callback
def configured_drivers(hass):
    """Return a set of configured Drives instances."""
    return {
        entry.data.get(CONF_NAME) for entry in hass.config_entries.async_entries(DOMAIN)
    }


class DriveFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Drive config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize zone configuration flow."""
        pass

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        return await self.async_step_confirm(user_input)

    async def async_step_confirm(self, user_input=None):
        """Handle a flow start."""
        errors = {}
        if user_input is not None:
            return await self.async_step_drive_name(user_input=None)
        return self.async_show_form(step_id="confirm", errors=errors)

    async def async_step_drive_name(self, user_input=None):
        """Handle a flow start."""
        from homeassistant.components.ais_drives_service import (
            TYPE_DRIVE,
            TYPE_FTP,
            TYPE_MEGA,
            get_remotes_types_by_name,
        )

        global DRIVE_NAME_INPUT, DRIVE_TYPE_INPUT, AUTH_URL
        errors = {}

        names = get_remotes_types_by_name(None)
        data_schema = vol.Schema(
            {vol.Required(CONF_TYPE): vol.In(list(names)), vol.Required(CONF_NAME): str}
        )
        if user_input is not None:
            DRIVE_NAME_INPUT = user_input.get(CONF_NAME)
            DRIVE_TYPE_INPUT = get_remotes_types_by_name(user_input.get(CONF_TYPE))

            ent_registry = await self.hass.helpers.entity_registry.async_get_registry()
            if ent_registry.async_is_registered(
                "sensor.ais_drives_service_" + slugify(DRIVE_NAME_INPUT)
            ):
                errors = {CONF_NAME: "identifier_exists"}

            if slugify(DRIVE_NAME_INPUT) != DRIVE_NAME_INPUT:
                errors = {CONF_NAME: "drive_name_error"}

            if errors == {}:
                if DRIVE_TYPE_INPUT == TYPE_DRIVE:
                    # get url from rclone
                    from homeassistant.components.ais_drives_service import (
                        rclone_get_auth_url,
                    )

                    AUTH_URL = rclone_get_auth_url(DRIVE_NAME_INPUT, DRIVE_TYPE_INPUT)
                    return await self.async_step_token(user_input=None)
                elif DRIVE_TYPE_INPUT == TYPE_MEGA:
                    return await self.async_step_passwd(user_input=None)
                elif DRIVE_TYPE_INPUT == TYPE_FTP:
                    return await self.async_step_ftp(user_input=None)

        return self.async_show_form(
            step_id="drive_name", errors=errors, data_schema=data_schema
        )

    async def async_step_token(self, user_input=None):
        """Handle a flow start."""
        from homeassistant.components.ais_drives_service import rclone_set_auth_gdrive

        errors = {}
        global G_DRIVE_CREATION_TIME_CALL
        data_schema = vol.Schema({vol.Required("token_key"): str})
        ret = ""
        if user_input is not None and "token_key" in user_input:
            # add new one
            user_input[CONF_NAME] = DRIVE_NAME_INPUT
            user_input[CONF_TYPE] = DRIVE_TYPE_INPUT
            ret = rclone_set_auth_gdrive(DRIVE_NAME_INPUT, user_input["token_key"])
            if ret == "ok":
                # remove if exists
                G_DRIVE_CREATION_TIME_CALL = time.time()
                exists_entries = [
                    entry.entry_id for entry in self._async_current_entries()
                ]
                if exists_entries:
                    await asyncio.wait(
                        [
                            self.hass.config_entries.async_remove(entry_id)
                            for entry_id in exists_entries
                        ]
                    )
                return self.async_create_entry(title="Zdalne dyski", data=user_input)
            else:
                errors = {"token_key": "token_error"}

        return self.async_show_form(
            step_id="token",
            errors=errors,
            description_placeholders={"auth_url": AUTH_URL},
            data_schema=data_schema,
        )

    async def async_step_passwd(self, user_input=None):
        """Handle a flow start."""
        from homeassistant.components.ais_drives_service import rclone_set_auth_mega

        errors = {}
        global G_DRIVE_CREATION_TIME_CALL
        data_schema = vol.Schema(
            {vol.Required(CONF_EMAIL): str, vol.Required(CONF_PASSWORD): str}
        )
        if user_input is not None and CONF_EMAIL in user_input:
            # add new one or update
            user_input[CONF_NAME] = DRIVE_NAME_INPUT
            user_input[CONF_TYPE] = DRIVE_TYPE_INPUT
            ret = rclone_set_auth_mega(
                DRIVE_NAME_INPUT, user_input[CONF_EMAIL], user_input[CONF_PASSWORD]
            )
            if ret == "ok":
                # if exists
                G_DRIVE_CREATION_TIME_CALL = time.time()
                exists_entries = [
                    entry.entry_id for entry in self._async_current_entries()
                ]
                if exists_entries:
                    await asyncio.wait(
                        [
                            self.hass.config_entries.async_remove(entry_id)
                            for entry_id in exists_entries
                        ]
                    )
                return self.async_create_entry(title="Zdalne dyski", data=user_input)
            else:
                errors = {"email": "rclone_error"}

        return self.async_show_form(
            step_id="passwd", errors=errors, data_schema=data_schema
        )

    async def async_step_ftp(self, user_input=None):
        """Handle a flow start."""
        from homeassistant.components.ais_drives_service import rclone_set_auth_ftp

        errors = {}
        global G_DRIVE_CREATION_TIME_CALL
        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=21): int,
                vol.Required(CONF_USERNAME, default="anonymous"): str,
                vol.Optional(CONF_PASSWORD, default=""): str,
            }
        )
        if user_input is not None and CONF_HOST in user_input:
            # add new one or update
            user_input[CONF_NAME] = DRIVE_NAME_INPUT
            user_input[CONF_TYPE] = DRIVE_TYPE_INPUT
            ret = rclone_set_auth_ftp(
                DRIVE_NAME_INPUT,
                user_input[CONF_HOST],
                user_input[CONF_PORT],
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )
            if ret == "ok":
                # if exists
                G_DRIVE_CREATION_TIME_CALL = time.time()
                exists_entries = [
                    entry.entry_id for entry in self._async_current_entries()
                ]
                if exists_entries:
                    await asyncio.wait(
                        [
                            self.hass.config_entries.async_remove(entry_id)
                            for entry_id in exists_entries
                        ]
                    )
                return self.async_create_entry(title="Zdalne dyski", data=user_input)
            else:
                errors = {"email": "rclone_error"}

        return self.async_show_form(
            step_id="ftp", errors=errors, data_schema=data_schema
        )
