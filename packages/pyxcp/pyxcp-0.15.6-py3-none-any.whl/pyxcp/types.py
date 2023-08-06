#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2020 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from collections import namedtuple
import enum

import construct

from construct import (
    Struct,
    Enum,
    Padding,
    Int8ul,
    GreedyBytes,
    Byte,
    Int16ul,
    Int32ul,
    BitStruct,
    BitsInteger,
    Flag,
    If,
    this,
    Int16ub,
    Int32ub,
    IfThenElse,
    Int16sl,
    Int32sl,
    Int16sb,
    Int32sb,
)


if construct.version < (2, 8):
    print("pyXCP requires at least construct 2.8")
    exit(1)


NumericType = (int, float)
MtaType = namedtuple("MtaType", "address ext")


class FrameSizeError(Exception):
    """
    A frame with an invalid size was received.
    """


class XcpResponseError(Exception):
    """
    Raise an `exception` from an XCP error packet.
    """

    def get_error_code(self):
        return self.args[0]


class XcpTimeoutError(Exception):
    """
    Timeout while waiting for a response occured.
    """


class XcpGetIdType(enum.IntEnum):
    ASCII_TEXT = 0
    FILENAME = 1
    FILE_AND_PATH = 2
    URL = 3
    FILE_TO_UPLOAD = 4


class Command(enum.IntEnum):

    # STD

    # Mandatory Commands
    CONNECT = 0xFF
    DISCONNECT = 0xFE
    GET_STATUS = 0xFD
    SYNCH = 0xFC

    # Optional Commands
    GET_COMM_MODE_INFO = 0xFB
    GET_ID = 0xFA
    SET_REQUEST = 0xF9
    GET_SEED = 0xF8
    UNLOCK = 0xF7
    SET_MTA = 0xF6
    UPLOAD = 0xF5
    SHORT_UPLOAD = 0xF4
    BUILD_CHECKSUM = 0xF3
    TRANSPORT_LAYER_CMD = 0xF2
    USER_CMD = 0xF1
    GET_VERSION = 0xC000

    # CAL

    # Mandatory Commands
    DOWNLOAD = 0xF0

    # Optional Commands
    DOWNLOAD_NEXT = 0xEF
    DOWNLOAD_MAX = 0xEE
    SHORT_DOWNLOAD = 0xED
    MODIFY_BITS = 0xEC

    # PAG

    # Mandatory Commands
    SET_CAL_PAGE = 0xEB
    GET_CAL_PAGE = 0xEA

    # Optional Commands
    GET_PAG_PROCESSOR_INFO = 0xE9
    GET_SEGMENT_INFO = 0xE8
    GET_PAGE_INFO = 0xE7
    SET_SEGMENT_MODE = 0xE6
    GET_SEGMENT_MODE = 0xE5
    COPY_CAL_PAGE = 0xE4

    # DAQ

    # Mandatory Commands
    CLEAR_DAQ_LIST = 0xE3
    SET_DAQ_PTR = 0xE2
    WRITE_DAQ = 0xE1
    WRITE_DAQ_MULTIPLE = 0xC7
    SET_DAQ_LIST_MODE = 0xE0
    GET_DAQ_LIST_MODE = 0xDF
    START_STOP_DAQ_LIST = 0xDE
    START_STOP_SYNCH = 0xDD

    # Optional Commands
    GET_DAQ_CLOCK = 0xDC
    READ_DAQ = 0xDB
    GET_DAQ_PROCESSOR_INFO = 0xDA
    GET_DAQ_RESOLUTION_INFO = 0xD9
    GET_DAQ_LIST_INFO = 0xD8
    GET_DAQ_EVENT_INFO = 0xD7
    DTO_CTR_PROPERTIES = 0xC5
    SET_DAQ_PACKED_MODE = 0xC001
    GET_DAQ_PACKED_MODE = 0xC002
    FREE_DAQ = 0xD6
    ALLOC_DAQ = 0xD5
    ALLOC_ODT = 0xD4
    ALLOC_ODT_ENTRY = 0xD3

    # PGM

    # Mandatory Commands
    PROGRAM_START = 0xD2
    PROGRAM_CLEAR = 0xD1
    PROGRAM = 0xD0
    PROGRAM_RESET = 0xCF

    # Optional Commands
    GET_PGM_PROCESSOR_INFO = 0xCE
    GET_SECTOR_INFO = 0xCD
    PROGRAM_PREPARE = 0xCC
    PROGRAM_FORMAT = 0xCB
    PROGRAM_NEXT = 0xCA
    PROGRAM_MAX = 0xC9
    PROGRAM_VERIFY = 0xC8

    TIME_CORRELATION_PROPERTIES = 0xC6


class CommandCategory(enum.IntEnum):
    """Values reflect resources (resource protection status / unlock)."""

    STD = 0
    CAL_PAG = 1
    DAQ = 4
    STIM = 8
    PGM = 16


COMMAND_CATEGORIES = {  # Mainly needed to automatically UNLOCK.
    Command.CONNECT: CommandCategory.STD,
    Command.DISCONNECT: CommandCategory.STD,
    Command.GET_STATUS: CommandCategory.STD,
    Command.SYNCH: CommandCategory.STD,
    Command.GET_COMM_MODE_INFO: CommandCategory.STD,
    Command.GET_ID: CommandCategory.STD,
    Command.SET_REQUEST: CommandCategory.STD,
    Command.GET_SEED: CommandCategory.STD,
    Command.UNLOCK: CommandCategory.STD,
    Command.SET_MTA: CommandCategory.STD,
    Command.UPLOAD: CommandCategory.STD,
    Command.SHORT_UPLOAD: CommandCategory.STD,
    Command.BUILD_CHECKSUM: CommandCategory.STD,
    Command.TRANSPORT_LAYER_CMD: CommandCategory.STD,
    Command.USER_CMD: CommandCategory.STD,
    Command.GET_VERSION: CommandCategory.STD,
    Command.DOWNLOAD: CommandCategory.CAL_PAG,
    Command.DOWNLOAD_NEXT: CommandCategory.CAL_PAG,
    Command.DOWNLOAD_MAX: CommandCategory.CAL_PAG,
    Command.SHORT_DOWNLOAD: CommandCategory.CAL_PAG,
    Command.MODIFY_BITS: CommandCategory.CAL_PAG,
    Command.SET_CAL_PAGE: CommandCategory.CAL_PAG,
    Command.GET_CAL_PAGE: CommandCategory.CAL_PAG,
    Command.GET_PAG_PROCESSOR_INFO: CommandCategory.CAL_PAG,
    Command.GET_SEGMENT_INFO: CommandCategory.CAL_PAG,
    Command.GET_PAGE_INFO: CommandCategory.CAL_PAG,
    Command.SET_SEGMENT_MODE: CommandCategory.CAL_PAG,
    Command.GET_SEGMENT_MODE: CommandCategory.CAL_PAG,
    Command.COPY_CAL_PAGE: CommandCategory.CAL_PAG,
    Command.CLEAR_DAQ_LIST: CommandCategory.DAQ,
    Command.CLEAR_DAQ_LIST: CommandCategory.DAQ,
    Command.SET_DAQ_PTR: CommandCategory.DAQ,
    Command.WRITE_DAQ: CommandCategory.DAQ,
    Command.WRITE_DAQ_MULTIPLE: CommandCategory.DAQ,
    Command.SET_DAQ_LIST_MODE: CommandCategory.DAQ,
    Command.GET_DAQ_LIST_MODE: CommandCategory.DAQ,
    Command.START_STOP_DAQ_LIST: CommandCategory.DAQ,
    Command.START_STOP_SYNCH: CommandCategory.DAQ,
    Command.GET_DAQ_CLOCK: CommandCategory.DAQ,
    Command.READ_DAQ: CommandCategory.DAQ,
    Command.GET_DAQ_PROCESSOR_INFO: CommandCategory.DAQ,
    Command.GET_DAQ_RESOLUTION_INFO: CommandCategory.DAQ,
    Command.GET_DAQ_LIST_INFO: CommandCategory.DAQ,
    Command.GET_DAQ_EVENT_INFO: CommandCategory.DAQ,
    Command.DTO_CTR_PROPERTIES: CommandCategory.DAQ,
    Command.SET_DAQ_PACKED_MODE: CommandCategory.DAQ,
    Command.GET_DAQ_PACKED_MODE: CommandCategory.DAQ,
    Command.FREE_DAQ: CommandCategory.DAQ,
    Command.ALLOC_DAQ: CommandCategory.DAQ,
    Command.ALLOC_ODT: CommandCategory.DAQ,
    Command.ALLOC_ODT_ENTRY: CommandCategory.DAQ,
    Command.PROGRAM_START: CommandCategory.PGM,
    Command.PROGRAM_CLEAR: CommandCategory.PGM,
    Command.PROGRAM: CommandCategory.PGM,
    Command.PROGRAM_RESET: CommandCategory.PGM,
    Command.GET_PGM_PROCESSOR_INFO: CommandCategory.PGM,
    Command.GET_SECTOR_INFO: CommandCategory.PGM,
    Command.PROGRAM_PREPARE: CommandCategory.PGM,
    Command.PROGRAM_FORMAT: CommandCategory.PGM,
    Command.PROGRAM_NEXT: CommandCategory.PGM,
    Command.PROGRAM_MAX: CommandCategory.PGM,
    Command.PROGRAM_VERIFY: CommandCategory.PGM,
    # Well... ?
    # TIME_CORRELATION_PROPERTIES
}

XcpError = Enum(
    Int8ul,
    ERR_CMD_SYNCH=0x00,  # Command processor synchronization. S0
    ERR_CMD_BUSY=0x10,  # Command was not executed. S2
    ERR_DAQ_ACTIVE=0x11,  # Command rejected because DAQ is running. S2
    ERR_PGM_ACTIVE=0x12,  # Command rejected because PGM is running. S2
    ERR_CMD_UNKNOWN=0x20,  # Unknown command or not implemented optional
    # command. S2
    ERR_CMD_SYNTAX=0x21,  # Command syntax invalid. S2
    ERR_OUT_OF_RANGE=0x22,  # Command syntax valid but command parameter(s)
    # out of range. S2
    ERR_WRITE_PROTECTED=0x23,  # The memory location is write protected. S2
    ERR_ACCESS_DENIED=0x24,  # The memory location is not accessible. S2
    ERR_ACCESS_LOCKED=0x25,  # Access denied, Seed & Key is required. S2
    ERR_PAGE_NOT_VALID=0x26,  # Selected page not available. S2
    ERR_MODE_NOT_VALID=0x27,  # Selected page mode not available. S2
    ERR_SEGMENT_NOT_VALID=0x28,  # Selected segment not valid. S2
    ERR_SEQUENCE=0x29,  # Sequence error. S2
    ERR_DAQ_CONFIG=0x2A,  # DAQ configuration not valid. S2
    ERR_MEMORY_OVERFLOW=0x30,  # Memory overflow error. S2
    ERR_GENERIC=0x31,  # Generic error. S2
    ERR_VERIFY=0x32,  # The slave internal program verify routine detects an
    # error. S3
    # NEW IN 1.1
    ERR_RESOURCE_TEMPORARY_NOT_ACCESSIBLE=0x33,
    # Access to the requested resource is temporary not possible. S3
    ERR_TIMEOUT=0xFF,  # Used by errorhandler; not an offical errorcode.
)

Response = Struct(
    "type"
    / Enum(
        Int8ul,
        OK=0xFF,
        ERR=0xFE,
        EV=0xFD,
        SERV=0xFC,
    )
)

DAQ = Struct(
    "odt" / Byte,
    "daq" / Byte,
    "data" / GreedyBytes,
)

ResourceType = BitStruct(
    Padding(2),
    "dbg" / Flag,
    "pgm" / Flag,
    "stim" / Flag,
    "daq" / Flag,
    Padding(1),
    "calpag" / Flag,
)

RESOURCE_VALUES = {
    "dbg": 32,
    "pgm": 16,
    "stim": 8,
    "daq": 4,
    "calpag": 1,
}

AddressGranularity = Enum(BitsInteger(2), BYTE=0b00, WORD=0b01, DWORD=0b10, RESERVED=0b11)

ByteOrder = Enum(BitsInteger(1), INTEL=0, MOTOROLA=1)

# byte-order dependent types
Int16u = IfThenElse(this._.byteOrder == ByteOrder.INTEL, Int16ul, Int16ub)
Int16s = IfThenElse(this._.byteOrder == ByteOrder.INTEL, Int16sl, Int16sb)
Int32u = IfThenElse(this._.byteOrder == ByteOrder.INTEL, Int32ul, Int32ub)
Int32s = IfThenElse(this._.byteOrder == ByteOrder.INTEL, Int32sl, Int32sb)

CommModeBasic = BitStruct(
    "optional" / Flag,  # The OPTIONAL flag indicates whether additional
    # information on supported types of Communication mode
    # is available. The master can get that additional
    # information with GET_COMM_MODE_INFO
    "slaveBlockMode" / Flag,
    Padding(3),
    "addressGranularity" / AddressGranularity,
    "byteOrder" / ByteOrder,
)

ConnectResponsePartial = Struct("resource" / ResourceType, "commModeBasic" / CommModeBasic)

ConnectResponse = Struct(
    "resource" / ResourceType,
    "commModeBasic" / CommModeBasic,
    "maxCto" / Int8ul,
    "maxDto" / Int16u,
    "protocolLayerVersion" / Int8ul,
    "transportLayerVersion" / Int8ul,
)

GetVersionResponse = Struct(
    Padding(1),
    "protocolMajor" / Int8ul,
    "protocolMinor" / Int8ul,
    "transportMajor" / Int8ul,
    "transportMinor" / Int8ul,
)

SessionStatus = BitStruct(
    "resume" / Flag,
    "daqRunning" / Flag,
    Padding(2),
    "clearDaqRequest" / Flag,
    "storeDaqRequest" / Flag,
    Padding(1),
    "storeCalRequest" / Flag,
)

GetStatusResponse = Struct(
    "sessionStatus" / SessionStatus,
    "resourceProtectionStatus" / ResourceType,
    Padding(1),
    "sessionConfiguration" / Int16u,
)

CommModeOptional = BitStruct(
    Padding(6),
    "interleavedMode" / Flag,
    "masterBlockMode" / Flag,
)

GetCommModeInfoResponse = Struct(
    Padding(1),
    "commModeOptional" / CommModeOptional,
    Padding(1),
    "maxBs" / Int8ul,
    "minSt" / Int8ul,
    "queueSize" / Int8ul,
    "xcpDriverVersionNumber" / Int8ul,
)

GetIDResponse = Struct(
    "mode" / Int8ul, Padding(2), "length" / Int32u, "identification" / If(this.mode == 1, Byte[this.length])
)

GetSeedResponse = Struct("length" / Int8ul, "seed" / If(this.length > 0, Byte[this.length]))

SetRequestMode = BitStruct(
    Padding(4),
    "clearDaqReq" / Flag,
    "storeDaqReq" / Flag,
    Padding(1),
    "storeCalReq" / Flag,
)

BuildChecksumResponse = Struct(
    "checksumType"
    / Enum(
        Int8ul,
        XCP_NONE=0x00,
        XCP_ADD_11=0x01,
        XCP_ADD_12=0x02,
        XCP_ADD_14=0x03,
        XCP_ADD_22=0x04,
        XCP_ADD_24=0x05,
        XCP_ADD_44=0x06,
        XCP_CRC_16=0x07,
        XCP_CRC_16_CITT=0x08,
        XCP_CRC_32=0x09,
        XCP_USER_DEFINED=0xFF,
    ),
    Padding(2),
    "checksum" / Int32u,
)

SetCalPageMode = BitStruct(
    "all" / Flag,
    Padding(5),
    "xcp" / Flag,
    "ecu" / Flag,
)

GetPagProcessorInfoResponse = Struct(
    "maxSegments" / Int8ul,
    "pagProperties" / Int8ul,
)

GetSegmentInfoMode0Response = Struct(
    Padding(3),
    "basicInfo" / Int32u,
)

GetSegmentInfoMode1Response = Struct(
    "maxPages" / Int8ul,
    "addressExtension" / Int8ul,
    "maxMapping" / Int8ul,
    "compressionMethod" / Int8ul,
    "encryptionMethod" / Int8ul,
)

GetSegmentInfoMode2Response = Struct(
    Padding(3),
    "mappingInfo" / Int32u,
)

PageProperties = BitStruct(
    Padding(2),
    "xcpWriteAccessWithEcu" / Flag,
    "xcpWriteAccessWithoutEcu" / Flag,
    "xcpReadAccessWithEcu" / Flag,
    "xcpReadAccessWithoutEcu" / Flag,
    "ecuAccessWithXcp" / Flag,
    "ecuAccessWithoutXcp" / Flag,
)

DaqProperties = BitStruct(
    "overloadEvent" / Flag,
    "overloadMsb" / Flag,
    "pidOffSupported" / Flag,
    "timestampSupported" / Flag,
    "bitStimSupported" / Flag,
    "resumeSupported" / Flag,
    "prescalerSupported" / Flag,
    "daqConfigType" / Enum(BitsInteger(1), STATIC=0b0, DYNAMIC=0b1),
)

GetDaqProcessorInfoResponse = Struct(
    "daqProperties" / DaqProperties,
    "maxDaq" / Int16u,
    "maxEventChannel" / Int16u,
    "minDaq" / Int8ul,
    "daqKeyByte"
    / BitStruct(
        "Identification_Field"
        / Enum(
            BitsInteger(2),
            IDF_ABS_ODT_NUMBER=0b00,
            IDF_REL_ODT_NUMBER_ABS_DAQ_LIST_NUMBER_BYTE=0b01,
            IDF_REL_ODT_NUMBER_ABS_DAQ_LIST_NUMBER_WORD=0b10,
            IDF_REL_ODT_NUMBER_ABS_DAQ_LIST_NUMBER_WORD_ALIGNED=0b11,
        ),
        "Address_Extension"
        / Enum(
            BitsInteger(2),
            AE_DIFFERENT_WITHIN_ODT=0b00,
            AE_SAME_FOR_ALL_ODT=0b01,
            _NOT_ALLOWED=0b10,
            AE_SAME_FOR_ALL_DAQ=0b11,
        ),
        "Optimisation_Type"
        / Enum(
            BitsInteger(4),
            OM_DEFAULT=0b0000,
            OM_ODT_TYPE_16=0b0001,
            OM_ODT_TYPE_32=0b0010,
            OM_ODT_TYPE_64=0b0011,
            OM_ODT_TYPE_ALIGNMENT=0b0100,
            OM_MAX_ENTRY_SIZE=0b0101,
        ),
    ),
)

DAQ_DIRECTION = Enum(BitsInteger(1), DAQ=0, STIM=1)

PID_OFF = Enum(BitsInteger(1), DTO_WITH_ID_FIELD=0, DTO_WITHOUT_ID_FIELD=1)

CurrentMode = BitStruct(
    "resume" / Flag,
    "running" / Flag,
    "pid_off" / PID_OFF,
    "timestamp" / Flag,
    Padding(2),
    "direction" / DAQ_DIRECTION,
    "selected" / Flag,
)

GetDaqListModeResponse = Struct(
    "currentMode" / CurrentMode,
    Padding(2),
    "currentEventChannel" / Int16u,
    "currentPrescaler" / Int8ul,
    "currentPriority" / Int8ul,
)

SetDaqListMode = BitStruct(
    Padding(2), "pid_off" / PID_OFF, "enable_timestamp" / Flag, Padding(2), "direction" / DAQ_DIRECTION, Padding(1)
)

DaqElement = Struct("bitOffset" / Int8ul, "size" / Int8ul, "address" / Int32u, "addressExt" / Int8ul, Padding(1))

GetDaqClockResponse = Struct(
    Padding(3),
    "timestamp" / Int32u,
)

DaqPackedMode = Enum(Int8ul, NONE=0, ELEMENT_GROUPED=1, EVENT_GROUPED=2)

GetDaqPackedModeResponse = Struct(
    Padding(1),
    "daqPackedMode" / DaqPackedMode,
    "dpmTimestampMode"
    / If((this.daqPackedMode == "ELEMENT_GROUPED") | (this.daqPackedMode == "EVENT_GROUPED"), Int8ul),
    "dpmSampleCount" / If((this.daqPackedMode == "ELEMENT_GROUPED") | (this.daqPackedMode == "EVENT_GROUPED"), Int16u),
)

ReadDaqResponse = Struct(
    "bitOffset" / Int8ul,
    "sizeofDaqElement" / Int8ul,
    "adressExtension" / Int8ul,
    "address" / Int32u,
)

DaqTimestampUnit = Enum(
    BitsInteger(4),
    DAQ_TIMESTAMP_UNIT_1NS=0b0000,
    DAQ_TIMESTAMP_UNIT_10NS=0b0001,
    DAQ_TIMESTAMP_UNIT_100NS=0b0010,
    DAQ_TIMESTAMP_UNIT_1US=0b0011,
    DAQ_TIMESTAMP_UNIT_10US=0b0100,
    DAQ_TIMESTAMP_UNIT_100US=0b0101,
    DAQ_TIMESTAMP_UNIT_1MS=0b0110,
    DAQ_TIMESTAMP_UNIT_10MS=0b0111,
    DAQ_TIMESTAMP_UNIT_100MS=0b1000,
    DAQ_TIMESTAMP_UNIT_1S=0b1001,
    DAQ_TIMESTAMP_UNIT_1PS=0b1010,
    DAQ_TIMESTAMP_UNIT_10PS=0b1011,
    DAQ_TIMESTAMP_UNIT_100PS=0b1100,
)

GetDaqResolutionInfoResponse = Struct(
    "granularityOdtEntrySizeDaq" / Int8ul,
    "maxOdtEntrySizeDaq" / Int8ul,
    "granularityOdtEntrySizeStim" / Int8ul,
    "maxOdtEntrySizeStim" / Int8ul,
    "timestampMode"
    / BitStruct(  # Int8ul,
        "unit" / DaqTimestampUnit,
        "fixed" / Flag,
        "size"
        / Enum(
            BitsInteger(3),
            NO_TIME_STAMP=0b000,
            S1=0b001,
            S2=0b010,
            NOT_ALLOWED=0b011,
            S4=0b100,
        ),
    ),
    "timestampTicks" / Int16u,
)

DaqListProperties = BitStruct(
    Padding(3),
    "packed" / Flag,
    "stim" / Flag,
    "daq" / Flag,
    "eventFixed" / Flag,
    "predefined" / Flag,
)

GetDaqListInfoResponse = Struct(
    "daqListProperties" / DaqListProperties,
    "maxOdt" / Int8ul,
    "maxOdtEntries" / Int8ul,
    "fixedEvent" / Int16u,
)

StartStopDaqListResponse = Struct("firstPid" / Int8ul)

DaqEventProperties = BitStruct(
    "consistency"
    / Enum(
        BitsInteger(2),
        CONSISTENCY_ODT=0b00,
        CONSISTENCY_DAQ=0b01,
        CONSISTENCY_EVENTCHANNEL=0b10,
        CONSISTENCY_NONE=0b11,
    ),
    Padding(1),
    "packed" / Flag,
    "stim" / Flag,
    "daq" / Flag,
    Padding(2),
)

GetEventChannelInfoResponse = Struct(
    "daqEventProperties" / DaqEventProperties,
    "maxDaqList" / Int8ul,
    "eventChannelNameLength" / Int8ul,
    "eventChannelTimeCycle" / Int8ul,
    "eventChannelTimeUnit"
    / Enum(
        Int8ul,
        EVENT_CHANNEL_TIME_UNIT_1NS=0,
        EVENT_CHANNEL_TIME_UNIT_10NS=1,
        EVENT_CHANNEL_TIME_UNIT_100NS=2,
        EVENT_CHANNEL_TIME_UNIT_1US=3,
        EVENT_CHANNEL_TIME_UNIT_10US=4,
        EVENT_CHANNEL_TIME_UNIT_100US=5,
        EVENT_CHANNEL_TIME_UNIT_1MS=6,
        EVENT_CHANNEL_TIME_UNIT_10MS=7,
        EVENT_CHANNEL_TIME_UNIT_100MS=8,
        EVENT_CHANNEL_TIME_UNIT_1S=9,
        EVENT_CHANNEL_TIME_UNIT_1PS=10,
        EVENT_CHANNEL_TIME_UNIT_10PS=11,
        EVENT_CHANNEL_TIME_UNIT_100PS=12,
    ),
    "eventChannelPriority" / Int8ul,
)

DtoCtrProperties = BitStruct(
    "evtCtrPresent" / Flag,
    "stimCtrCpyPresent" / Flag,
    "stimModePresent" / Flag,
    "daqModePresent" / Flag,
    "relatedEventPresent" / Flag,
    "stimModeFixed" / Flag,
    "daqModeFixed" / Flag,
    "relatedEventFixed" / Flag,
)

DtoCtrMode = BitStruct(Padding(6), "stimMode" / Flag, "daqMode" / Flag)

DtoCtrPropertiesResponse = Struct("properties" / DtoCtrProperties, "relatedEventChannel" / Int16u, "mode" / DtoCtrMode)

CommModePgm = BitStruct(
    Padding(1),
    "slaveBlockMode" / Flag,
    Padding(4),
    "interleavedMode" / Flag,
    "masterBlockMode" / Flag,
)

ProgramStartResponse = Struct(
    Padding(1),
    "commModePgm" / CommModePgm,
    "maxCtoPgm" / Int8ul,
    "maxBsPgm" / Int8ul,
    "minStPgm" / Int8ul,
    "queueSizePgm" / Int8ul,
)

PgmProperties = BitStruct(
    "nonSeqPgmRequired" / Flag,
    "nonSeqPgmSupported" / Flag,
    "encryptionRequired" / Flag,
    "encryptionSupported" / Flag,
    "compressionRequired" / Flag,
    "compressionSupported" / Flag,
    "functionalMode" / Flag,
    "absoluteMode" / Flag,
)

GetPgmProcessorInfoResponse = Struct("pgmProperties" / PgmProperties, "maxSector" / Int8ul)

GetSectorInfoResponseMode01 = Struct(
    "clearSequenceNumber" / Int8ul,
    "programSequenceNumber" / Int8ul,
    "programmingMethod" / Int8ul,
    "sectorInfo" / Int32u,
)

GetSectorInfoResponseMode2 = Struct("sectorNameLength" / Int8ul)

TimeCorrelationPropertiesResponse = Struct(
    "slaveConfig" / Int8ul,
    "observableClocks" / Int8ul,
    "syncState" / Int8ul,
    "clockInfo" / Int8ul,
    Padding(1),
    "clusterId" / Int16u,
)

DaqPtr = namedtuple("DaqPtr", "daqListNumber odtNumber odtEntryNumber")

DAQ_TIMESTAMP_UNIT_TO_EXP = {
    "DAQ_TIMESTAMP_UNIT_1PS": -12,
    "DAQ_TIMESTAMP_UNIT_10PS": -11,
    "DAQ_TIMESTAMP_UNIT_100PS": -10,
    "DAQ_TIMESTAMP_UNIT_1NS": -9,
    "DAQ_TIMESTAMP_UNIT_10NS": -8,
    "DAQ_TIMESTAMP_UNIT_100NS": -7,
    "DAQ_TIMESTAMP_UNIT_1US": -6,
    "DAQ_TIMESTAMP_UNIT_10US": -5,
    "DAQ_TIMESTAMP_UNIT_100US": -4,
    "DAQ_TIMESTAMP_UNIT_1MS": -3,
    "DAQ_TIMESTAMP_UNIT_10MS": -2,
    "DAQ_TIMESTAMP_UNIT_100MS": -1,
    "DAQ_TIMESTAMP_UNIT_1S": 0,
}


class XcpGetSeedMode(enum.IntEnum):
    FIRST_PART = 0
    REMAINING = 1
