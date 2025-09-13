"""Config flow for ActivityManager."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.core import callback

from .const import (
    DOMAIN,
    DEFAULT_STATE_SCHEDULED,
    DEFAULT_STATE_DUE, 
    DEFAULT_STATE_OVERDUE,
    DEFAULT_UPDATE_INTERVAL,
    UPDATE_INTERVALS
)
import logging

_LOGGER = logging.getLogger(__name__)


class ActivityManagerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a ActivityManager config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        # Check if already configured
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title="Activity Manager", data={'name': "Activity Manager"})

    async_step_import = async_step_user
    
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ActivityManagerOptionsFlowHandler(config_entry)


class ActivityManagerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for the Activity Manager component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize ActivityManager options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_options = self.config_entry.options
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "state_scheduled", 
                    default=current_options.get("state_scheduled", DEFAULT_STATE_SCHEDULED)
                ): str,
                vol.Optional(
                    "state_due", 
                    default=current_options.get("state_due", DEFAULT_STATE_DUE)
                ): str,
                vol.Optional(
                    "state_overdue", 
                    default=current_options.get("state_overdue", DEFAULT_STATE_OVERDUE)
                ): str,
                vol.Optional(
                    "update_interval",
                    default=current_options.get("update_interval", DEFAULT_UPDATE_INTERVAL)
                ): vol.In(list(UPDATE_INTERVALS.keys())),
            })
        )