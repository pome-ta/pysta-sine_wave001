from objc_util import UIApplication
from objc_util import c, ObjCInstance

import ctypes
import math

from pprint import pprint
import time
import sys
import ui

# --- AudioComponentDescription
OSType = ctypes.c_uint32


class AudioComponentDescription(ctypes.Structure):
  _fields_ = [('componentType', OSType), ('componentSubType', OSType),
              ('componentManufacturer', OSType),
              ('componentFlags', ctypes.c_uint32),
              ('componentFlagsMask', ctypes.c_uint32)]


# --- AudioComponentDescription */

# --- defaultOutputDescription
kAudioUnitType_Output = int.from_bytes(b'auou', byteorder='big')
kAudioUnitSubType_RemoteIO = int.from_bytes(b'rioc', byteorder='big')
kAudioUnitManufacturer_Apple = int.from_bytes(b'appl', byteorder='big')
# --- defaultOutputDescription */

# --- AudioComponentFindNext
AudioComponentFindNext = c.AudioComponentFindNext
AudioComponentFindNext.argtypes = [
  ctypes.c_void_p, ctypes.POINTER(AudioComponentDescription)
]
AudioComponentFindNext.restype = ctypes.c_void_p
# --- AudioComponentFindNext */

# --- AudioComponentInstanceNew
OSStatus = ctypes.c_int32
AudioComponentInstanceNew = c.AudioComponentInstanceNew
AudioComponentInstanceNew.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
AudioComponentInstanceNew.restype = OSStatus
# --- AudioComponentInstanceNew */

# --- AURenderCallbackStruct
AudioUnitRenderActionFlags = ctypes.c_uint32


class AudioTimeStampFlags(ctypes.c_uint32):
  kAudioTimeStampNothingValid = (0)
  kAudioTimeStampSampleTimeValid = (1 << 0)
  kAudioTimeStampHostTimeValid = (1 << 1)
  kAudioTimeStampRateScalarValid = (1 << 2)
  kAudioTimeStampWordClockTimeValid = (1 << 3)
  kAudioTimeStampSMPTETimeValid = (1 << 4)
  kAudioTimeStampSampleHostTimeValid = (kAudioTimeStampSampleTimeValid
                                        | kAudioTimeStampHostTimeValid)


# todo: `from enum import IntFlag` 使える？
class SMPTETimeType(ctypes.c_uint32):
  kSMPTETimeType24 = 0
  kSMPTETimeType25 = 1
  kSMPTETimeType30Drop = 2
  kSMPTETimeType30 = 3
  kSMPTETimeType2997 = 4
  kSMPTETimeType2997Drop = 5
  kSMPTETimeType60 = 6
  kSMPTETimeType5994 = 7
  kSMPTETimeType60Drop = 8
  kSMPTETimeType5994Drop = 9
  kSMPTETimeType50 = 10
  kSMPTETimeType2398 = 11


class SMPTETimeFlags(ctypes.c_uint32):
  kSMPTETimeUnknown = 0
  kSMPTETimeValid = (1 << 0)
  kSMPTETimeRunning = (1 << 1)


class SMPTETime(ctypes.Structure):
  _fields_ = [('mSubframes', ctypes.c_int16),
              ('mSubframeDivisor', ctypes.c_int16),
              ('mCounter', ctypes.c_uint32), ('mType', SMPTETimeType),
              ('mFlags', SMPTETimeFlags), ('mHours', ctypes.c_int16),
              ('mMinutes', ctypes.c_int16), ('mSeconds', ctypes.c_int16),
              ('mFrames', ctypes.c_int16)]


class AudioTimeStamp(ctypes.Structure):
  _fields_ = [('mSampleTime', ctypes.c_double), ('mHostTime', ctypes.c_int64),
              ('mRateScalar', ctypes.c_double),
              ('mWordClockTime', ctypes.c_uint64), ('mSMPTETime', SMPTETime),
              ('mFlags', AudioTimeStampFlags), ('mReserved', ctypes.c_uint32)]


class AudioBuffer(ctypes.Structure):
  _fields_ = [('mNumberChannels', ctypes.c_uint32),
              ('mDataByteSize', ctypes.c_uint32), ('mData', ctypes.c_void_p)]


class AudioBufferList(ctypes.Structure):
  _fields_ = [('mNumberBuffers', ctypes.c_uint32),
              ('mBuffers', AudioBuffer * 1)]


# todo: よくわかってない
def render_callback_prototype(
  inRefCon: ctypes.c_void_p,
  ioActionFlags: ctypes.POINTER(AudioUnitRenderActionFlags),
  inTimeStamp: ctypes.POINTER(AudioTimeStamp), inBusNumber: ctypes.c_uint32,
  inNumberFrames: ctypes.c_uint32, ioData: ctypes.POINTER(AudioBufferList)
) -> ctypes.c_uint32:
  pass


AURenderCallbackargs = list(render_callback_prototype.__annotations__.values())
AURenderCallback = ctypes.CFUNCTYPE(AURenderCallbackargs[-1],
                                    *AURenderCallbackargs[0:-1])


class AURenderCallbackStruct(ctypes.Structure):
  _fields_ = [('inputProc', AURenderCallback),
              ('inputProcRefCon', ctypes.c_void_p)]


# --- AURenderCallbackStruct */

# --- AudioUnitSetProperty
AudioUnitSetProperty = c.AudioUnitSetProperty
AudioUnitSetProperty.argtypes = [
  ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32,
  ctypes.c_void_p, ctypes.c_uint32
]
AudioUnitSetProperty.restype = OSStatus
kAudioUnitProperty_SetRenderCallback = 23
kAudioUnitScope_Input = 1
# --- AudioUnitSetProperty */

# --- AudioUnitInitialize
AudioUnitInitialize = c.AudioUnitInitialize
AudioUnitInitialize.argtypes = [ctypes.c_void_p]
AudioUnitInitialize.restype = OSStatus
# --- AudioUnitInitialize */

# --- AudioOutputUnitStart
AudioOutputUnitStart = c.AudioOutputUnitStart
AudioOutputUnitStart.argtypes = [ctypes.c_void_p]
AudioOutputUnitStart.restype = OSStatus
# --- AudioOutputUnitStart */

# --- AudioOutputUnitStop
AudioOutputUnitStop = c.AudioOutputUnitStop
AudioOutputUnitStop.argtypes = [ctypes.c_void_p]
AudioOutputUnitStop.restype = OSStatus
# --- AudioOutputUnitStop */

# --- AudioUnitUninitialize
AudioUnitUninitialize = c.AudioUnitUninitialize
AudioUnitUninitialize.argtypes = [ctypes.c_void_p]
AudioUnitUninitialize.restype = OSStatus
# --- AudioUnitUninitialize */

# --- AudioComponentInstanceDispose
AudioComponentInstanceDispose = c.AudioComponentInstanceDispose
AudioComponentInstanceDispose.argtypes = [ctypes.c_void_p]
AudioComponentInstanceDispose.restype = OSStatus
# --- AudioComponentInstanceDispose */

pi = math.pi


def render_callback(
  inRefCon: ctypes.c_void_p,
  ioActionFlags: ctypes.POINTER(AudioUnitRenderActionFlags),
  inTimeStamp: ctypes.POINTER(AudioTimeStamp), inBusNumber: ctypes.c_uint32,
  inNumberFrames: ctypes.c_uint32, ioData: ctypes.POINTER(AudioBufferList)
) -> ctypes.c_uint32:

  amplitude = 0.5
  sampleRate = 44100
  frequency = 440
  instance = ObjCInstance(inRefCon)
  theta = instance.theta
  theta_increment = 2.0 * pi * frequency / sampleRate

  buffer = ctypes.cast(ioData[0].mBuffers[0].mData,
                       ctypes.POINTER(ctypes.c_float *
                                      inNumberFrames)).contents

  for frame in range(inNumberFrames):
    buffer[frame] = math.sin(theta) * amplitude
    theta += theta_increment
    if theta > 2.0 * pi:
      theta -= 2.0 * pi

  instance.theta = theta
  print(theta)
  return 0


# --- Start
defaultOutputDescription = AudioComponentDescription()

defaultOutputDescription.componentType = kAudioUnitType_Output
defaultOutputDescription.componentSubType = kAudioUnitSubType_RemoteIO
defaultOutputDescription.componentManufacturer = kAudioUnitManufacturer_Apple
defaultOutputDescription.componentFlags = 0
defaultOutputDescription.componentFlagsMask = 0

defaultOutput = AudioComponentFindNext(None,
                                       ctypes.byref(defaultOutputDescription))

toneUnit = ctypes.c_void_p(0)
err = AudioComponentInstanceNew(defaultOutput, ctypes.byref(toneUnit))

input = AURenderCallbackStruct()


class View(ui.View):

  def __init__(self):
    self.instance = ObjCInstance(self)
    self.instance.theta = 0


v = View()
v.present()

RenderTone = AURenderCallback(render_callback)
input.inputProc = RenderTone
input.inputProcRefCon = v.instance.ptr
err = AudioUnitSetProperty(toneUnit, kAudioUnitProperty_SetRenderCallback,
                           kAudioUnitScope_Input, 0, ctypes.byref(input),
                           ctypes.sizeof(input))

print('---')
AudioUnitInitialize(toneUnit)
AudioOutputUnitStart(toneUnit)

# n秒後に終了
time.sleep(1.0)

AudioOutputUnitStop(toneUnit)
AudioUnitUninitialize(toneUnit)
AudioComponentInstanceDispose(toneUnit)
# --- exit
toneUnit = None
# todo: 他のscript に影響出る
del input
sys.exit()
# --- exit */

