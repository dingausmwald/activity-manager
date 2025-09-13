# activity-manager

Manager recurring tasks from within Home Assistant

Use the companion [Activity Manager Card](https://github.com/dingausmwald/activity-manager-card) for the best experience.

The core idea is that an activity happens on a recurring basis, which is stored in the `frequency` field when adding an activity. By default, the activity is last completed when you first add the activity and then the timer can be reset.

<p align="center">
  <img width="600" src="images/activitymanager.gif">
</p>

## Installation

### Manually

Clone or download this repository and copy the "activity_manager" directory to your "custom_components" directory in your config directory

`<config directory>/custom_components/activity-manager/...`

### HACS

1. Open the HACS section of Home Assistant.
2. Click the "..." button in the top right corner and select "Custom Repositories."
3. In the window that opens paste this Github URL.
4. Select "Integration"
5. In the window that opens when you select it click om "Install This Repository in HACS"

## Usage

Once installed, you can use the link below to add the integration from the UI.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=activity_manager)

If you're using the [Activity Manager Card](https://github.com/dingausmwald/activity-manager-card), then you all you need to do is add the Activity Manager Card to your dashboard. When you're creating the card, you'll have to supply a `category` attribute to the card.

### Notifications

Because entities are exposed for each activity, you can build custom notifications. The example below runs an automation at sunrise to remind the user if they are past due on workout activities:

```
service: notify.mobile_android_phone
data:
  title: >-
    Workout reminder{% if (states.sensor | selectattr('attributes.integration', 'eq', 'activity_manager') |
    selectattr('attributes.category', 'equalto', 'Workout') |
    map(attribute='state') | map('as_datetime') | reject(">", now()) | list |
    count > 1)%}s{% endif %}
  message: >-
    {{ "Remember to stay healthy and go do: " }}
    {%- set new_line = joiner("<br />") %}
    <br />
    {%- for activity in states.sensor | selectattr('attributes.integration', 'eq', 'activity_manager') -%}
    {%- if activity.state|as_datetime < now() and activity.attributes.category=="Workout"  -%}
    {{ new_line() }}{{ " - "}}{{  activity.name }}
    {%- endif -%}
    {%- endfor %}
  data:
    priority: high
    ttl: 0
    importance: high
    notification_icon: "mdi:dumbbell"
```

### More information

-   Activities are stored in .activities_list.json in your `<config>` folder
-   An entity is created for each activity (e.g. `sensor.<category>_<activity>`). The state of the activity shows the current status (scheduled/due/overdue), with the due date available as an attribute.
-   Three services are exposed: `activity_manager.add_activity`, `activity_manager.update_activity`, `activity_manager.remove_activity`. The update activity can be used to reset the timer.

## Configuration Options

After installing the integration, you can configure:

- **Custom State Terms**: Define your own terms for "scheduled", "due", and "overdue" states
- **Update Interval**: Choose how often the states are updated (daily, hourly, 15min, 5min)

Access these options via: Configuration → Integrations → Activity Manager → Configure

## Changelog

### Version 0.1.0 (Fork by dingausmwald)

**New Features:**
- 🎯 **Smart State System**: Sensors now show status ("scheduled", "due", "overdue") instead of dates
- ⚙️ **Custom State Terms**: Configure your own terms via integration options
- ⏰ **Configurable Update Intervals**: Choose from daily to 5-minute updates
- 📅 **Due Date Attribute**: Original due date preserved as sensor attribute
- 📊 **Logbook Integration**: State changes now appear in Home Assistant logbook

**Technical:**
- Added options flow for customization
- Implemented `async_track_time_interval` for regular updates
- Maintained WebSocket API compatibility for existing cards
