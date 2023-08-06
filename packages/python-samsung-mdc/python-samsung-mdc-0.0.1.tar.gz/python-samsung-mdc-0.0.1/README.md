# Samsung-MDC

This is implementation of Samsung MDC (Multiple Display Control) protocol on **python3.7+** and **asyncio** with most comprehensive CLI (command line interface).

It allows you to control a variety of different sources (TV, Monitor) through the built-in RS-232C or Ethernet interface.

[MDC Protocol specification - v13.7c 2016-02-23](MDC-Protocol_v13.7c_2016-02-23.pdf)

* Implemented *49* commands
* Easy to extend using simple declarative API - see [samsung_mdc/commmands.py](samsung_mdc/commands.py)
* Detailed [CLI](#usage) help and parameters validation
* Run commands async on numerous targets (using asyncio)
* TCP and SERIAL mode (for RJ45 and RS232C connection types)
* [script](#script) command for advanced usage
* [Python example](#python-example)

Not implemented: some more commands (PRs are welcome)

## Install

```
# global
pip3 install git+https://github.com/vgavro/samsung-mdc
samsung-mdc --help

# local
git clone https://github.com/vgavro/samsung-mdc
cd ./samsung-mdc
python3 -m venv venv
./venv/bin/pip3 install -e ./
./venv/bin/samsung-mdc --help
```

## Usage
```
Usage: samsung-mdc [OPTIONS] TARGET COMMAND [ARGS]...

  Try 'samsung-mdc --help COMMAND' for command info

  For multiple targets commands will be running async, so result order may
  differ.

  TARGET may be:

  DISPLAY_ID@IP[:PORT] (default port: 1515, example: 0@192.168.0.10:1515)
  FILENAME with target list (separated by newline)

  For serial port connection:
  DISPLAY_ID@PORT_NAME for Windows (example: 1@COM1)
  DISPLAY_ID@PORT_PATH (example: 1@/dev/ttyUSB0)

  We're trying to make autodetection of connection mode by port name, but
  you may want to use --mode option.

Options:
  -v, --verbose
  -m, --mode [auto|tcp|serial]  default: auto
  -t, --timeout FLOAT           read/write/connect timeout in seconds
                                (default: 5) (connect can be overrided with
                                separate option)

  --connect-timeout FLOAT
  -h, --help                    Show this message and exit.

```
### Commands:

* [status](#status) `(POWER_STATE VOLUME MUTE_STATE INPUT_SOURCE_STATE PICTURE_ASPECT_STATE N_TIME_NF F_TIME_NF)`
* [serial_number](#serial_number) `(SERIAL_NUMBER)`
* [software_version](#software_version) `(SOFTWARE_VERSION)`
* [model_number](#model_number) `(MODEL_SPECIES MODEL_NUMBER TV_SUPPORT)`
* [power](#power) `[POWER_STATE]`
* [volume](#volume) `[VOLUME]`
* [mute](#mute) `[MUTE_STATE]`
* [input_source](#input_source) `[INPUT_SOURCE_STATE]`
* [picture_aspect](#picture_aspect) `[PICTURE_ASPECT_STATE]`
* [mdc_connection](#mdc_connection) `(MDC_CONNECTION_TYPE)`
* [contrast](#contrast) `[CONTRAST]`
* [brightness](#brightness) `[BRIGHTNESS]`
* [sharpness](#sharpness) `[SHARPNESS]`
* [color](#color) `[COLOR]`
* [tint](#tint) `[TINT]`
* [h_position](#h_position) `H_POSITION_MOVE_TO`
* [v_position](#v_position) `V_POSITION_MOVE_TO`
* [auto_power](#auto_power) `[AUTO_POWER_STATE]`
* [clear_menu](#clear_menu) 
* [ir_state](#ir_state) `[IR_STATE]`
* [rgb_contrast](#rgb_contrast) `[CONTRAST]`
* [rgb_brightness](#rgb_brightness) `[BRIGHTNESS]`
* [auto_adjustment_on](#auto_adjustment_on) 
* [color_tone](#color_tone) `[COLOR_TONE_STATE]`
* [standby](#standby) `[STANDBY_STATE]`
* [auto_lamp](#auto_lamp) `[MAX_TIME MAX_LAMP_VALUE MIN_TIME MIN_LAMP_VALUE]`
* [manual_lamp](#manual_lamp) `[LAMP_VALUE]`
* [inverse](#inverse) `[INVERSE_STATE]`
* [safety_lock](#safety_lock) `[LOCK_STATE]`
* [panel_lock](#panel_lock) `[LOCK_STATE]`
* [device_name](#device_name) `(DEVICE_NAME)`
* [osd](#osd) `[OSD_ENABLED]`
* [all_keys_lock](#all_keys_lock) `[LOCK_STATE]`
* [model_name](#model_name) `(MODEL_NAME)`
* [energy_saving](#energy_saving) `[ENERGY_SAVING_STATE]`
* [reset](#reset) `RESET_TARGET`
* [osd_type](#osd_type) `[OSD_TYPE OSD_ENABLED]`
* [timer_13](#timer_13) `TIMER_ID [ON_TIME ON_ENABLED OFF_TIME OFF_ENABLED VOLUME INPUT_SOURCE_STATE HOLIDAY_APPLY REPEAT MANUAL_WEEKDAY]`
* [timer_15](#timer_15) `TIMER_ID [ON_TIME ON_ENABLED OFF_TIME OFF_ENABLED ON_REPEAT ON_MANUAL_WEEKDAY OFF_REPEAT OFF_MANUAL_WEEKDAY VOLUME INPUT_SOURCE_STATE HOLIDAY_APPLY]`
* [clock_m](#clock_m) `[DATETIME]`
* [virtual_remote](#virtual_remote) `REMOTE_KEY_CODE`
* [network_standby](#network_standby) `[NETWORK_STANDBY_STATE]`
* [auto_id_setting](#auto_id_setting) `[AUTO_ID_SETTING_STATE]`
* [display_id](#display_id) `DISPLAY_ID_STATE`
* [clock_s](#clock_s) `[DATETIME]`
* [launcher_play_via](#launcher_play_via) `[PLAY_VIA_MODE]`
* [launcher_url_address](#launcher_url_address) `[URL_ADDRESS]`
* [panel](#panel) `[PANEL_STATE]`
* [script](#script) `[OPTIONS] SCRIPT_FILE`

#### status
```
Usage: samsung-mdc [OPTIONS] TARGET status

Data:
  POWER_STATE           OFF | ON | REBOOT
  VOLUME                int (0-100)
  MUTE_STATE            OFF | ON
  INPUT_SOURCE_STATE    S_VIDEO | COMPONENT | AV | AV2 | SCART1 | DVI | PC |
                        BNC | DVI_VIDEO | MAGIC_INFO | HDMI1 | HDMI1_PC |
                        HDMI2 | HDMI2_PC | DISPLAY_PORT_1 | DISPLAY_PORT_2 |
                        DISPLAY_PORT_3 | RF_TV | HDMI3 | HDMI3_PC | HDMI4 |
                        HDMI4_PC | TV_DTV | PLUG_IN_MODE | HD_BASE_T |
                        MEDIA_MAGIC_INFO_S | WIDI_SCREEN_MIRRORING |
                        INTERNAL_USB | URL_LAUNCHER | IWB

  PICTURE_ASPECT_STATE  PC_16_9 | PC_4_3 | PC_ORIGINAL_RATIO | PC_21_9 |
                        VIDEO_AUTO_WIDE | VIDEO_16_9 | VIDEO_ZOOM |
                        VIDEO_ZOOM_1 | VIDEO_ZOOM_2 | VIDEO_SCREEN_FIT |
                        VIDEO_4_3 | VIDEO_WIDE_FIT | VIDEO_CUSTOM |
                        VIDEO_SMART_VIEW_1 | VIDEO_SMART_VIEW_2 |
                        VIDEO_WIDE_ZOOM | VIDEO_21_9

  N_TIME_NF             int
  F_TIME_NF             int
```
#### serial_number
```
Usage: samsung-mdc [OPTIONS] TARGET serial_number

Data:
  SERIAL_NUMBER  str
```
#### software_version
```
Usage: samsung-mdc [OPTIONS] TARGET software_version

Data:
  SOFTWARE_VERSION  str
```
#### model_number
```
Usage: samsung-mdc [OPTIONS] TARGET model_number

Data:
  MODEL_SPECIES  PDP | LCD | DLP | LED | CRT | OLED
  MODEL_NUMBER   int
  TV_SUPPORT     SUPPORTED | NOT_SUPPORTED
```
#### power
```
Usage: samsung-mdc [OPTIONS] TARGET power [POWER_STATE]

Data:
  POWER_STATE  OFF | ON | REBOOT
```
#### volume
```
Usage: samsung-mdc [OPTIONS] TARGET volume [VOLUME]

Data:
  VOLUME  int (0-100)
```
#### mute
```
Usage: samsung-mdc [OPTIONS] TARGET mute [MUTE_STATE]

Data:
  MUTE_STATE  OFF | ON
```
#### input_source
```
Usage: samsung-mdc [OPTIONS] TARGET input_source [INPUT_SOURCE_STATE]

Data:
  INPUT_SOURCE_STATE  S_VIDEO | COMPONENT | AV | AV2 | SCART1 | DVI | PC | BNC
                      | DVI_VIDEO | MAGIC_INFO | HDMI1 | HDMI1_PC | HDMI2 |
                      HDMI2_PC | DISPLAY_PORT_1 | DISPLAY_PORT_2 |
                      DISPLAY_PORT_3 | RF_TV | HDMI3 | HDMI3_PC | HDMI4 |
                      HDMI4_PC | TV_DTV | PLUG_IN_MODE | HD_BASE_T |
                      MEDIA_MAGIC_INFO_S | WIDI_SCREEN_MIRRORING |
                      INTERNAL_USB | URL_LAUNCHER | IWB

```
#### picture_aspect
```
Usage: samsung-mdc [OPTIONS] TARGET picture_aspect [PICTURE_ASPECT_STATE]

Data:
  PICTURE_ASPECT_STATE  PC_16_9 | PC_4_3 | PC_ORIGINAL_RATIO | PC_21_9 |
                        VIDEO_AUTO_WIDE | VIDEO_16_9 | VIDEO_ZOOM |
                        VIDEO_ZOOM_1 | VIDEO_ZOOM_2 | VIDEO_SCREEN_FIT |
                        VIDEO_4_3 | VIDEO_WIDE_FIT | VIDEO_CUSTOM |
                        VIDEO_SMART_VIEW_1 | VIDEO_SMART_VIEW_2 |
                        VIDEO_WIDE_ZOOM | VIDEO_21_9

```
#### mdc_connection
```
Usage: samsung-mdc [OPTIONS] TARGET mdc_connection

Data:
  MDC_CONNECTION_TYPE  RS232C | RJ45
```
#### contrast
```
Usage: samsung-mdc [OPTIONS] TARGET contrast [CONTRAST]

Data:
  CONTRAST  int (0-100)
```
#### brightness
```
Usage: samsung-mdc [OPTIONS] TARGET brightness [BRIGHTNESS]

Data:
  BRIGHTNESS  int (0-100)
```
#### sharpness
```
Usage: samsung-mdc [OPTIONS] TARGET sharpness [SHARPNESS]

Data:
  SHARPNESS  int (0-100)
```
#### color
```
Usage: samsung-mdc [OPTIONS] TARGET color [COLOR]

Data:
  COLOR  int (0-100)
```
#### tint
```
Usage: samsung-mdc [OPTIONS] TARGET tint [TINT]

  Tint value code to be set on TV/Monitor. R: Tint Value, G: ( 100 - Tint )
  Value.

  Note: Tint could only be set in 50 Steps (0, 2, 4, 6... 100).

Data:
  TINT  int (0-100)
```
#### h_position
```
Usage: samsung-mdc [OPTIONS] TARGET h_position H_POSITION_MOVE_TO

Data:
  H_POSITION_MOVE_TO  LEFT | RIGHT
```
#### v_position
```
Usage: samsung-mdc [OPTIONS] TARGET v_position V_POSITION_MOVE_TO

Data:
  V_POSITION_MOVE_TO  UP | DOWN
```
#### auto_power
```
Usage: samsung-mdc [OPTIONS] TARGET auto_power [AUTO_POWER_STATE]

Data:
  AUTO_POWER_STATE  OFF | ON
```
#### clear_menu
```
Usage: samsung-mdc [OPTIONS] TARGET clear_menu
```
#### ir_state
```
Usage: samsung-mdc [OPTIONS] TARGET ir_state [IR_STATE]

  Enables/disables IR (Infrared) receiving function (Remote Control).

  Working Condition: * Can operate regardless of whether power is ON/OFF.
  (If DPMS Situation in LFD, it operate Remocon regardless of set value).

Data:
  IR_STATE  DISABLED | ENABLED
```
#### rgb_contrast
```
Usage: samsung-mdc [OPTIONS] TARGET rgb_contrast [CONTRAST]

Data:
  CONTRAST  int (0-100)
```
#### rgb_brightness
```
Usage: samsung-mdc [OPTIONS] TARGET rgb_brightness [BRIGHTNESS]

Data:
  BRIGHTNESS  int (0-100)
```
#### auto_adjustment_on
```
Usage: samsung-mdc [OPTIONS] TARGET auto_adjustment_on
```
#### color_tone
```
Usage: samsung-mdc [OPTIONS] TARGET color_tone [COLOR_TONE_STATE]

Data:
  COLOR_TONE_STATE  COOL_2 | COOL_1 | NORMAL | WARM_1 | WARM_2 | OFF
```
#### standby
```
Usage: samsung-mdc [OPTIONS] TARGET standby [STANDBY_STATE]

Data:
  STANDBY_STATE  OFF | ON | AUTO
```
#### auto_lamp
```
Usage: samsung-mdc [OPTIONS] TARGET auto_lamp [MAX_TIME MAX_LAMP_VALUE
                   MIN_TIME MIN_LAMP_VALUE]

  Auto Lamp function (backlight).

  Note: When Manual Lamp Control is on, Auto Lamp Control will automatically
  turn off.

Data:
  MAX_TIME        time (format: %H:%M:%S)
  MAX_LAMP_VALUE  int (0-100)
  MIN_TIME        time (format: %H:%M:%S)
  MIN_LAMP_VALUE  int (0-100)
```
#### manual_lamp
```
Usage: samsung-mdc [OPTIONS] TARGET manual_lamp [LAMP_VALUE]

  Manual Lamp function (backlight).

  Note: When Auto Lamp Control is on, Manual Lamp Control will automatically
  turn off.

Data:
  LAMP_VALUE  int (0-100)
```
#### inverse
```
Usage: samsung-mdc [OPTIONS] TARGET inverse [INVERSE_STATE]

Data:
  INVERSE_STATE  OFF | ON
```
#### safety_lock
```
Usage: samsung-mdc [OPTIONS] TARGET safety_lock [LOCK_STATE]

Data:
  LOCK_STATE  OFF | ON
```
#### panel_lock
```
Usage: samsung-mdc [OPTIONS] TARGET panel_lock [LOCK_STATE]

Data:
  LOCK_STATE  OFF | ON
```
#### device_name
```
Usage: samsung-mdc [OPTIONS] TARGET device_name

  It reads the device name which user set up in network. Shows the
  information about entered device name.

Data:
  DEVICE_NAME  str
```
#### osd
```
Usage: samsung-mdc [OPTIONS] TARGET osd [OSD_ENABLED]

Data:
  OSD_ENABLED  bool
```
#### all_keys_lock
```
Usage: samsung-mdc [OPTIONS] TARGET all_keys_lock [LOCK_STATE]

  Turns both REMOCON and Panel Key Lock function on/off.

  Note: Can operate regardless of whether power is on/off.

Data:
  LOCK_STATE  OFF | ON
```
#### model_name
```
Usage: samsung-mdc [OPTIONS] TARGET model_name

Data:
  MODEL_NAME  str
```
#### energy_saving
```
Usage: samsung-mdc [OPTIONS] TARGET energy_saving [ENERGY_SAVING_STATE]

Data:
  ENERGY_SAVING_STATE  OFF | LOW | MEDIUM | HIGH | PICTURE_OFF
```
#### reset
```
Usage: samsung-mdc [OPTIONS] TARGET reset RESET_TARGET

Data:
  RESET_TARGET  PICTURE | SOUND | SETUP | ALL | SCREEN_DISPLAY
```
#### osd_type
```
Usage: samsung-mdc [OPTIONS] TARGET osd_type [OSD_TYPE OSD_ENABLED]

Data:
  OSD_TYPE     SOURCE | NOT_OPTIMUM_MODE | NO_SIGNAL | MDC | SCHEDULE_CHANNEL
  OSD_ENABLED  bool
```
#### timer_13
```
Usage: samsung-mdc [OPTIONS] TARGET timer_13 TIMER_ID [ON_TIME ON_ENABLED
                   OFF_TIME OFF_ENABLED VOLUME INPUT_SOURCE_STATE
                   HOLIDAY_APPLY REPEAT MANUAL_WEEKDAY]

  Integrated timer function (13 parameters version).

  Note: This depends on product and will not work on newer versions.

Data:
  TIMER_ID            int (1-7)
  ON_TIME             time (format: %H:%M:%S)
  ON_ENABLED          bool
  OFF_TIME            time (format: %H:%M:%S)
  OFF_ENABLED         bool
  VOLUME              int (0-100)
  INPUT_SOURCE_STATE  S_VIDEO | COMPONENT | AV | AV2 | SCART1 | DVI | PC | BNC
                      | DVI_VIDEO | MAGIC_INFO | HDMI1 | HDMI1_PC | HDMI2 |
                      HDMI2_PC | DISPLAY_PORT_1 | DISPLAY_PORT_2 |
                      DISPLAY_PORT_3 | RF_TV | HDMI3 | HDMI3_PC | HDMI4 |
                      HDMI4_PC | TV_DTV | PLUG_IN_MODE | HD_BASE_T |
                      MEDIA_MAGIC_INFO_S | WIDI_SCREEN_MIRRORING |
                      INTERNAL_USB | URL_LAUNCHER | IWB

  HOLIDAY_APPLY       DONT_APPLY_BOTH | APPLY_BOTH | ON_TIMER_ONLY_APPLY |
                      OFF_TIMER_ONLY_APPLY

  REPEAT              ONCE | EVERYDAY | MON_FRI | MON_SAT | SAT_SUN |
                      MANUAL_WEEKDAY

  MANUAL_WEEKDAY      list(,) SUN | MON | TUE | WED | THU | FRI | SAT
```
#### timer_15
```
Usage: samsung-mdc [OPTIONS] TARGET timer_15 TIMER_ID [ON_TIME ON_ENABLED
                   OFF_TIME OFF_ENABLED ON_REPEAT ON_MANUAL_WEEKDAY OFF_REPEAT
                   OFF_MANUAL_WEEKDAY VOLUME INPUT_SOURCE_STATE HOLIDAY_APPLY]

  Integrated timer function (15 parameters version).

  Note: This depends on product and will not work on older versions.

  ON_TIME/OFF_TIME - Turn ON/OFF display at specific time of day

  ON_ACTIVE/OFF_ACTIVE - If timer is not active, values are ignored, so
  there may be only OFF timer, ON timer, or both.

  REPEAT - On which day timer is enabled (combined with HOLIDAY_APPLY and
  MANUAL_WEEKDAY)

Data:
  TIMER_ID            int (1-7)
  ON_TIME             time (format: %H:%M:%S)
  ON_ENABLED          bool
  OFF_TIME            time (format: %H:%M:%S)
  OFF_ENABLED         bool
  ON_REPEAT           ONCE | EVERYDAY | MON_FRI | MON_SAT | SAT_SUN |
                      MANUAL_WEEKDAY

  ON_MANUAL_WEEKDAY   list(,) SUN | MON | TUE | WED | THU | FRI | SAT
  OFF_REPEAT          ONCE | EVERYDAY | MON_FRI | MON_SAT | SAT_SUN |
                      MANUAL_WEEKDAY

  OFF_MANUAL_WEEKDAY  list(,) SUN | MON | TUE | WED | THU | FRI | SAT
  VOLUME              int (0-100)
  INPUT_SOURCE_STATE  S_VIDEO | COMPONENT | AV | AV2 | SCART1 | DVI | PC | BNC
                      | DVI_VIDEO | MAGIC_INFO | HDMI1 | HDMI1_PC | HDMI2 |
                      HDMI2_PC | DISPLAY_PORT_1 | DISPLAY_PORT_2 |
                      DISPLAY_PORT_3 | RF_TV | HDMI3 | HDMI3_PC | HDMI4 |
                      HDMI4_PC | TV_DTV | PLUG_IN_MODE | HD_BASE_T |
                      MEDIA_MAGIC_INFO_S | WIDI_SCREEN_MIRRORING |
                      INTERNAL_USB | URL_LAUNCHER | IWB

  HOLIDAY_APPLY       DONT_APPLY_BOTH | APPLY_BOTH | ON_TIMER_ONLY_APPLY |
                      OFF_TIMER_ONLY_APPLY

```
#### clock_m
```
Usage: samsung-mdc [OPTIONS] TARGET clock_m [DATETIME]

  Current time function (minute precision).

  Note: This is for models developed until 2013. For newer models see
  CLOCK_S function (seconds precision).

Data:
  DATETIME  datetime (format: %Y-%m-%dT%H:%M:%S / %Y-%m-%d %H:%M:%S /
            %Y-%m-%dT%H:%M / %Y-%m-%d %H:%M)

```
#### virtual_remote
```
Usage: samsung-mdc [OPTIONS] TARGET virtual_remote REMOTE_KEY_CODE

  This function support that MDC command can work same as remote control.

  Note: In a certain model, 0x79 content key works as Home and 0x1f Display
  key works as Info.

Data:
  REMOTE_KEY_CODE  KEY_SOURCE | KEY_POWER | KEY_1 | KEY_2 | KEY_3 |
                   KEY_VOLUME_UP | KEY_4 | KEY_5 | KEY_6 | KEY_VOLUME_DOWN |
                   KEY_7 | KEY_8 | KEY_9 | KEY_MUTE | KEY_CHANNEL_DOWN | KEY_0
                   | KEY_CHANNEL_UP | KEY_GREEN | KEY_YELLOW | KEY_CYAN |
                   KEY_MENU | KEY_DISPLAY | KEY_DIGIT | KEY_PIP_TV_VIDEO |
                   KEY_EXIT | KEY_REW | KEY_STOP | KEY_PLAY | KEY_FF |
                   KEY_PAUSE | KEY_TOOLS | KEY_RETURN | KEY_MAGICINFO_LITE |
                   KEY_CURSOR_UP | KEY_CURSOR_DOWN | KEY_CURSOR_RIGHT |
                   KEY_CURSOR_LEFT | KEY_ENTER | KEY_RED | KEY_LOCK |
                   KEY_CONTENT | DISCRET_POWER_OFF | KEY_3D

```
#### network_standby
```
Usage: samsung-mdc [OPTIONS] TARGET network_standby [NETWORK_STANDBY_STATE]

Data:
  NETWORK_STANDBY_STATE  OFF | ON
```
#### auto_id_setting
```
Usage: samsung-mdc [OPTIONS] TARGET auto_id_setting [AUTO_ID_SETTING_STATE]

Data:
  AUTO_ID_SETTING_STATE  START | END
```
#### display_id
```
Usage: samsung-mdc [OPTIONS] TARGET display_id DISPLAY_ID_STATE

Data:
  DISPLAY_ID_STATE  OFF | ON
```
#### clock_s
```
Usage: samsung-mdc [OPTIONS] TARGET clock_s [DATETIME]

  Current time function (second precision).

  Note: This is for models developed after 2013. For older models see
  CLOCK_M function (minute precision).

Data:
  DATETIME  datetime (format: %Y-%m-%dT%H:%M:%S / %Y-%m-%d %H:%M:%S /
            %Y-%m-%dT%H:%M / %Y-%m-%d %H:%M)

```
#### launcher_play_via
```
Usage: samsung-mdc [OPTIONS] TARGET launcher_play_via [PLAY_VIA_MODE]

Data:
  PLAY_VIA_MODE  MAGIC_INFO | URL_LAUNCHER | MAGIC_IWB
```
#### launcher_url_address
```
Usage: samsung-mdc [OPTIONS] TARGET launcher_url_address [URL_ADDRESS]

Data:
  URL_ADDRESS  str
```
#### panel
```
Usage: samsung-mdc [OPTIONS] TARGET panel [PANEL_STATE]

Data:
  PANEL_STATE  ON | OFF
```
#### script
```
Usage: samsung-mdc [OPTIONS] TARGET script [OPTIONS] SCRIPT_FILE

  Script file with commands to execute.

  Commands for multiple targets will be running async, but commands order is
  preserved for device (and is running on same connection), exit on first
  fail unless retry options provided.

  It's highly recommended to use sleep option for virtual_remote!

  Additional commands:
  sleep SECONDS  (FLOAT, --sleep option for this command is ignored)
  disconnect

  Format:
  command1 [ARGS]...
  command2 [ARGS]...

  Example: samsung-mdc ./targets.txt script -s 3 -r 1 ./commands.txt
  # commands.txt content
  power on
  sleep 5
  clear_menu
  virtual_remote key_menu
  virtual_remote key_down
  virtual_remote enter
  clear_menu

Arguments:
  script_file  Text file with commands, separated by newline.

Options:
  -s, --sleep FLOAT            Pause between commands (seconds)
  --retry-command INTEGER      Retry command if failed (count)
  --retry-command-sleep FLOAT  Sleep before command retry (seconds)
  -r, --retry-script INTEGER   Retry script if failed (count)
  --retry-script-sleep FLOAT   Sleep before script retry (seconds)
  --help                       Show this message and exit.
```

## Python example
```python3
import asyncio
from samsung_mdc import MDC


async def main(ip, display_id):
    async with MDC(ip, verbose=True) as mdc:
        # First argument of command is always display_id
        status = await mdc.status(display_id)
        print(status)  # Result is always tuple

        if status[0] != MDC.power.POWER_STATE.ON:
            # Command arguments are always Sequence (tuple, list)
            await mdc.power(display_id, [MDC.power.POWER_STATE.ON])
            await mdc.close()  # Force reconnect on next command
            await asyncio.sleep(15)

        await mdc.display_id(display_id, [MDC.display_id.DISPLAY_ID_STATE.ON])
        # You may also use names or values instead of enums
        await mdc.display_id(display_id, ['ON'])  # same
        await mdc.display_id(display_id, [1])     # same


# If you see "Connected" and timeout error, try other display_id (0, 1)
asyncio.run(main('192.168.0.10', 1))

```
