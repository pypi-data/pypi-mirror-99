from enum import Enum

from .command import Command
from .fields import Enum as EnumField, Int, Bool, Str, Time, DateTime, Bitmask
from .utils import parse_enum_bitmask


class DAY_PART(Enum):
    PM = 0x00
    AM = 0x01


class LOCK_STATE(Enum):
    OFF = 0x00
    ON = 0x01


class SERIAL_NUMBER(Command):
    CMD = 0x0B
    GET, SET = True, False
    DATA = [Str('SERIAL_NUMBER')]


class SOFTWARE_VERSION(Command):
    CMD = 0x0E
    GET, SET = True, False
    DATA = [Str('SOFTWARE_VERSION')]


class MODEL_NUMBER(Command):
    CMD = 0x10
    GET, SET = True, False

    class MODEL_SPECIES(Enum):
        PDP = 0x01
        LCD = 0x02
        DLP = 0x03
        LED = 0x04
        CRT = 0x05
        OLED = 0x06

    class TV_SUPPORT(Enum):
        SUPPORTED = 0x00
        NOT_SUPPORTED = 0x01

    # NOTE: Actually there is list of MODEL_NUMBER codes in specification,
    # but it's TOO long
    DATA = [MODEL_SPECIES, Int('MODEL_NUMBER'), TV_SUPPORT]


class POWER(Command):
    CMD = 0x11
    GET, SET = True, True

    class POWER_STATE(Enum):
        OFF = 0x00
        ON = 0x01
        REBOOT = 0x02

    DATA = [POWER_STATE]


class VOLUME(Command):
    CMD = 0x12
    GET, SET = True, True
    VOLUME = Int('VOLUME', range(101))
    DATA = [VOLUME]


class MUTE(Command):
    CMD = 0x13
    GET, SET = True, True

    class MUTE_STATE(Enum):
        OFF = 0x00
        ON = 0x01

    DATA = [MUTE_STATE]


class INPUT_SOURCE(Command):
    CMD = 0x14
    GET, SET = True, True

    class INPUT_SOURCE_STATE(Enum):
        S_VIDEO = 0x04
        COMPONENT = 0x08
        AV = 0x0C
        AV2 = 0x0D
        SCART1 = 0x0E
        DVI = 0x18
        PC = 0x14
        BNC = 0x1E
        DVI_VIDEO = 0x1F
        MAGIC_INFO = 0x20
        HDMI1 = 0x21
        HDMI1_PC = 0x22
        HDMI2 = 0x23
        HDMI2_PC = 0x24
        DISPLAY_PORT_1 = 0x25
        DISPLAY_PORT_2 = 0x26
        DISPLAY_PORT_3 = 0x27
        RF_TV = 0x30
        HDMI3 = 0x31
        HDMI3_PC = 0x32
        HDMI4 = 0x33
        HDMI4_PC = 0x34
        TV_DTV = 0x40
        PLUG_IN_MODE = 0x50
        HD_BASE_T = 0x55
        MEDIA_MAGIC_INFO_S = 0x60
        WIDI_SCREEN_MIRRORING = 0x61
        INTERNAL_USB = 0x62
        URL_LAUNCHER = 0x63
        IWB = 0x64

    DATA = [INPUT_SOURCE_STATE]


class PICTURE_ASPECT(Command):
    CMD = 0x15
    GET, SET = True, True

    class PICTURE_ASPECT_STATE(Enum):
        PC_16_9 = 0x10
        PC_4_3 = 0x18
        PC_ORIGINAL_RATIO = 0x20
        PC_21_9 = 0x21

        VIDEO_AUTO_WIDE = 0x00
        VIDEO_16_9 = 0x01
        VIDEO_ZOOM = 0x04
        VIDEO_ZOOM_1 = 0x05
        VIDEO_ZOOM_2 = 0x06
        VIDEO_SCREEN_FIT = 0x09
        VIDEO_4_3 = 0x0B
        VIDEO_WIDE_FIT = 0x0C
        VIDEO_CUSTOM = 0x0D
        VIDEO_SMART_VIEW_1 = 0x0E
        VIDEO_SMART_VIEW_2 = 0x0F
        VIDEO_WIDE_ZOOM = 0x31
        VIDEO_21_9 = 0x32

    DATA = [PICTURE_ASPECT_STATE]


class MDC_CONNECTION(Command):
    CMD = 0x1D
    GET, SET = True, False
    # NOTE: There is no Set command in documentation,
    # but comment states that this parameter is readonly
    # only for RJ45 connection...

    class MDC_CONNECTION_TYPE(Enum):
        RS232C = 0x00
        RJ45 = 0x01

    DATA = [MDC_CONNECTION_TYPE]


class CONTRAST(Command):
    CMD = 0x24
    GET, SET = True, True
    DATA = [Int('CONTRAST', range(101))]


class BRIGHTNESS(Command):
    CMD = 0x25
    GET, SET = True, True
    DATA = [Int('BRIGHTNESS', range(101))]


class SHARPNESS(Command):
    CMD = 0x26
    GET, SET = True, True
    DATA = [Int('SHARPNESS', range(101))]


class COLOR(Command):
    CMD = 0x27
    GET, SET = True, True
    DATA = [Int('COLOR', range(101))]


class TINT(Command):
    """
    Tint value code to be set on TV/Monitor.
    R: Tint Value, G: ( 100 - Tint ) Value.

    Note: Tint could only be set in 50 Steps (0, 2, 4, 6... 100).
    """
    CMD = 0x28
    GET, SET = True, True
    DATA = [Int('TINT', range(101))]


class H_POSITION(Command):
    CMD = 0x31
    GET, SET = False, True

    class H_POSITION_MOVE_TO(Enum):
        LEFT = 0x00
        RIGHT = 0x01

    DATA = [H_POSITION_MOVE_TO]


class V_POSITION(Command):
    CMD = 0x32
    GET, SET = False, True

    class V_POSITION_MOVE_TO(Enum):
        UP = 0x00
        DOWN = 0x01

    DATA = [V_POSITION_MOVE_TO]


class AUTO_POWER(Command):
    CMD = 0x33
    GET, SET = True, True

    class AUTO_POWER_STATE(Enum):
        OFF = 0x00
        ON = 0x01

    DATA = [AUTO_POWER_STATE]


class CLEAR_MENU(Command):
    CMD = 0x34
    SUBCMD = 0x00
    GET, SET = False, True

    DATA = []


class IR_STATE(Command):
    """
    Enables/disables IR (Infrared) receiving function (Remote Control).

    Working Condition:
    * Can operate regardless of whether power is ON/OFF.
    (If DPMS Situation in LFD, it operate Remocon regardless of set value).
    """
    CMD = 0x36
    GET, SET = True, True

    class IR_STATE(Enum):
        DISABLED = 0x00
        ENABLED = 0x01

    DATA = [IR_STATE]


class RGB_CONTRAST(Command):
    CMD = 0x37
    GET, SET = True, True
    DATA = [Int('CONTRAST', range(101))]


class RGB_BRIGHTNESS(Command):
    CMD = 0x38
    GET, SET = True, True
    DATA = [Int('BRIGHTNESS', range(101))]


class AUTO_ADJUSTMENT_ON(Command):
    CMD = 0x3D
    SUBCMD = 0x00
    GET, SET = False, True
    DATA = []


class COLOR_TONE(Command):
    CMD = 0x3E
    GET, SET = True, True

    class COLOR_TONE_STATE(Enum):
        COOL_2 = 0x00
        COOL_1 = 0x01
        NORMAL = 0x02
        WARM_1 = 0x03
        WARM_2 = 0x04
        OFF = 0x50

    DATA = [COLOR_TONE_STATE]


class STANDBY(Command):
    CMD = 0x4A
    GET, SET = True, True

    class STANDBY_STATE(Enum):
        OFF = 0x00
        ON = 0x01
        AUTO = 0x02

    DATA = [STANDBY_STATE]


class AUTO_LAMP(Command):
    """
    Auto Lamp function (backlight).

    Note: When Manual Lamp Control is on,
    Auto Lamp Control will automatically turn off.
    """
    CMD = 0x57
    GET, SET = True, True

    DATA = [
        Time('MAX_TIME'),
        Int('MAX_LAMP_VALUE', range(101)),
        Time('MIN_TIME'),
        Int('MIN_LAMP_VALUE', range(101)),
    ]


class MANUAL_LAMP(Command):
    """
    Manual Lamp function (backlight).

    Note: When Auto Lamp Control is on,
    Manual Lamp Control will automatically turn off.
    """
    CMD = 0x58
    GET, SET = True, True
    DATA = [Int('LAMP_VALUE', range(101))]


class INVERSE(Command):
    CMD = 0x5A
    GET, SET = True, True

    class INVERSE_STATE(Enum):
        OFF = 0x00
        ON = 0x01

    DATA = [INVERSE_STATE]


class SAFETY_LOCK(Command):
    CMD = 0x5D
    GET, SET = True, True
    DATA = [LOCK_STATE]


class PANEL_LOCK(Command):
    CMD = 0x5F
    GET, SET = True, True
    DATA = [LOCK_STATE]


class DEVICE_NAME(Command):
    """
    It reads the device name which user set up in network.
    Shows the information about entered device name.
    """
    CMD = 0x67
    GET, SET = True, False
    DATA = [Str('DEVICE_NAME')]


class OSD(Command):
    CMD = 0x70
    GET, SET = True, True

    DATA = [Bool('OSD_ENABLED')]


class ALL_KEYS_LOCK(Command):
    """
    Turns both REMOCON and Panel Key Lock function on/off.

    Note: Can operate regardless of whether power is on/off.
    """

    # TODO: REMOCON? Remote Control?
    CMD = 0x77
    GET, SET = True, True

    class LOCK_STATE(Enum):
        OFF = 0x00
        ON = 0x01

    DATA = [LOCK_STATE]


class MODEL_NAME(Command):
    CMD = 0x8A
    GET, SET = True, False
    DATA = [Str('MODEL_NAME')]


class ENERGY_SAVING(Command):
    CMD = 0x92
    GET, SET = True, True

    class ENERGY_SAVING_STATE(Enum):
        OFF = 0x00
        LOW = 0x01
        MEDIUM = 0x02
        HIGH = 0x03
        PICTURE_OFF = 0x04

    DATA = [ENERGY_SAVING_STATE]


class RESET(Command):
    CMD = 0x9F
    GET, SET = False, True

    class RESET_TARGET(Enum):
        PICTURE = 0x00
        SOUND = 0x01
        SETUP = 0x02  # (System reset)
        ALL = 0x03
        SCREEN_DISPLAY = 0x04

    DATA = [RESET_TARGET]


class OSD_TYPE(Command):
    CMD = 0xA3
    GET, SET = True, True

    class OSD_TYPE(Enum):
        SOURCE = 0x00
        NOT_OPTIMUM_MODE = 0x01
        NO_SIGNAL = 0x02
        MDC = 0x03
        SCHEDULE_CHANNEL = 0x04

    DATA = [OSD_TYPE, Bool('OSD_ENABLED')]

    @classmethod
    def parse_response_data(cls, data):
        return parse_enum_bitmask(cls.OSD_TYPE, data[0])


class TIMER_15(Command):
    """
    Integrated timer function (15 parameters version).

    Note: This depends on product and will not work on older versions.

    ON_TIME/OFF_TIME - Turn ON/OFF display at specific time of day

    ON_ACTIVE/OFF_ACTIVE - If timer is not active, values are ignored,
    so there may be only OFF timer, ON timer, or both.

    REPEAT - On which day timer is enabled
    (combined with HOLIDAY_APPLY and MANUAL_WEEKDAY)
    """
    CMD = Int('TIMER_ID', range(1, 8))
    _TIMER_ID_CMD = [0xA4, 0xA5, 0xA6, 0xAB, 0xAC, 0xAD, 0xAE]
    GET, SET = True, True

    class TIMER_REPEAT(Enum):
        ONCE = 0x00
        EVERYDAY = 0x01
        MON_FRI = 0x02
        MON_SAT = 0x03
        SAT_SUN = 0x04
        MANUAL_WEEKDAY = 0x05

    class WEEKDAY(Enum):
        SUN = 0
        MON = 1
        TUE = 2
        WED = 3
        THU = 4
        FRI = 5
        SAT = 6
        # ignore_bit_7 = 7

    class HOLIDAY_APPLY(Enum):
        DONT_APPLY_BOTH = 0x00
        APPLY_BOTH = 0x01
        ON_TIMER_ONLY_APPLY = 0x02
        OFF_TIMER_ONLY_APPLY = 0x03

    DATA = [
        Time('ON_TIME'),
        Bool('ON_ENABLED'),

        Time('OFF_TIME'),
        Bool('OFF_ENABLED'),

        EnumField(TIMER_REPEAT, 'ON_REPEAT'),
        # TODO: implement bitmask field
        Bitmask(WEEKDAY, 'ON_MANUAL_WEEKDAY'),

        EnumField(TIMER_REPEAT, 'OFF_REPEAT'),
        Bitmask(WEEKDAY, 'OFF_MANUAL_WEEKDAY'),

        VOLUME.VOLUME,
        INPUT_SOURCE.INPUT_SOURCE_STATE,
        HOLIDAY_APPLY,
    ]

    async def __call__(self, connection, display_id, timer_id, data):
        cmd = self._TIMER_ID_CMD[timer_id - 1]
        data = self.parse_response(
            await connection.send(
                cmd, display_id,
                self.pack_payload_data(data) if data else []
            ),
        )
        return self.parse_response_data(data)

    @classmethod
    def get_order(cls):
        return (0xA4, cls.name)


class TIMER_13(TIMER_15):
    """
    Integrated timer function (13 parameters version).

    Note: This depends on product and will not work on newer versions.
    """
    DATA = ([
        f for f in TIMER_15.DATA
        if not f.name.endswith('_REPEAT')
        and not f.name.endswith('_MANUAL_WEEKDAY')
    ] + [
        EnumField(TIMER_15.TIMER_REPEAT, 'REPEAT'),
        Bitmask(TIMER_15.WEEKDAY, 'MANUAL_WEEKDAY'),
    ])


class CLOCK_S(Command):
    """
    Current time function (second precision).

    Note: This is for models developed after 2013.
    For older models see CLOCK_M function (minute precision).
    """
    GET, SET = True, True
    CMD = 0xC5

    DATA = [DateTime()]


class CLOCK_M(CLOCK_S):
    """
    Current time function (minute precision).

    Note: This is for models developed until 2013.
    For newer models see CLOCK_S function (seconds precision).
    """
    CMD = 0xA7

    DATA = [DateTime(seconds=False)]


class VIRTUAL_REMOTE(Command):
    """
    This function support that MDC command can work same as remote control.

    Note: In a certain model, 0x79 content key works as Home
    and 0x1f Display key works as Info.
    """
    CMD = 0xB0
    GET, SET = False, True

    class REMOTE_KEY_CODE(Enum):
        KEY_SOURCE = 0x01
        KEY_POWER = 0x02
        KEY_1 = 0x04
        KEY_2 = 0x05
        KEY_3 = 0x06
        KEY_VOLUME_UP = 0x07
        KEY_4 = 0x08
        KEY_5 = 0x09
        KEY_6 = 0x0A
        KEY_VOLUME_DOWN = 0x0B
        KEY_7 = 0x0C
        KEY_8 = 0x0D
        KEY_9 = 0x0E
        KEY_MUTE = 0x0F
        KEY_CHANNEL_DOWN = 0x10
        KEY_0 = 0x11
        KEY_CHANNEL_UP = 0x12
        KEY_GREEN = 0x14
        KEY_YELLOW = 0x15
        KEY_CYAN = 0x16
        KEY_MENU = 0x1A
        KEY_DISPLAY = 0x1F
        KEY_DIGIT = 0x23
        KEY_PIP_TV_VIDEO = 0x24
        KEY_EXIT = 0x2D
        KEY_REW = 0x45
        KEY_STOP = 0x46
        KEY_PLAY = 0x47
        KEY_FF = 0x48
        KEY_PAUSE = 0x4A
        KEY_TOOLS = 0x4B
        KEY_RETURN = 0x58
        KEY_MAGICINFO_LITE = 0x5B
        KEY_CURSOR_UP = 0x60
        KEY_CURSOR_DOWN = 0x61
        KEY_CURSOR_RIGHT = 0x62
        KEY_CURSOR_LEFT = 0x65
        KEY_ENTER = 0x68
        KEY_RED = 0x6C
        KEY_LOCK = 0x77
        KEY_CONTENT = 0x79  # HOME
        DISCRET_POWER_OFF = 0x98
        KEY_3D = 0x9F

    DATA = [REMOTE_KEY_CODE]


class NETWORK_STANDBY(Command):
    CMD = 0xB5
    GET, SET = True, True

    class NETWORK_STANDBY_STATE(Enum):
        OFF = 0x00
        ON = 0x01

    DATA = [NETWORK_STANDBY_STATE]


class AUTO_ID_SETTING(Command):
    CMD = 0xB8
    GET, SET = True, True

    class AUTO_ID_SETTING_STATE(Enum):
        START = 0x00
        END = 0x01

    DATA = [AUTO_ID_SETTING_STATE]


class DISPLAY_ID(Command):
    CMD = 0xB9
    GET, SET = False, True

    class DISPLAY_ID_STATE(Enum):
        OFF = 0x00
        ON = 0x01

    DATA = [DISPLAY_ID_STATE]


class LAUNCHER_PLAY_VIA(Command):
    CMD = 0xC7
    SUBCMD = 0x81
    GET, SET = True, True

    class PLAY_VIA_MODE(Enum):
        MAGIC_INFO = 0x00
        URL_LAUNCHER = 0x01
        MAGIC_IWB = 0x02

    DATA = [PLAY_VIA_MODE]


class LAUNCHER_URL_ADDRESS(Command):
    CMD = 0xC7
    SUBCMD = 0x82
    GET, SET = True, True
    DATA = [Str('URL_ADDRESS')]


class PANEL(Command):
    CMD = 0xF9
    GET, SET = True, True

    class PANEL_STATE(Enum):
        ON = 0x00
        OFF = 0x01

    DATA = [PANEL_STATE]


class STATUS(Command):
    CMD = 0x00
    GET, SET = True, False
    DATA = [
        POWER.POWER_STATE, VOLUME.VOLUME, MUTE.MUTE_STATE,
        INPUT_SOURCE.INPUT_SOURCE_STATE, PICTURE_ASPECT.PICTURE_ASPECT_STATE,
        Int('N_TIME_NF'), Int('F_TIME_NF')
    ]
