from objc_util import UIApplication
from objc_util import c, ObjCInstance

import ctypes
import math

from pprint import pprint
import time
import sys
import ui, editor

# --- AudioComponentDescription
OSType = ctypes.c_uint32


class AudioComponentDescription(ctypes.Structure):
  _fields_ = [
    ('componentType', OSType),
    ('componentSubType', OSType),
    ('componentManufacturer', OSType),
    ('componentFlags', ctypes.c_uint32),
    ('componentFlagsMask', ctypes.c_uint32),
  ]


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
  kAudioTimeStampSampleHostTimeValid = (kAudioTimeStampSampleTimeValid \
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
  _fields_ = [
    ('mSubframes', ctypes.c_int16),
    ('mSubframeDivisor', ctypes.c_int16),
    ('mCounter', ctypes.c_uint32),
    ('mType', SMPTETimeType),
    ('mFlags', SMPTETimeFlags),
    ('mHours', ctypes.c_int16),
    ('mMinutes', ctypes.c_int16),
    ('mSeconds', ctypes.c_int16),
    ('mFrames', ctypes.c_int16),
  ]


class AudioTimeStamp(ctypes.Structure):
  _fields_ = [
    ('mSampleTime', ctypes.c_double),
    ('mHostTime', ctypes.c_int64),
    ('mRateScalar', ctypes.c_double),
    ('mWordClockTime', ctypes.c_uint64),
    ('mSMPTETime', SMPTETime),
    ('mFlags', AudioTimeStampFlags),
    ('mReserved', ctypes.c_uint32),
  ]


class AudioBuffer(ctypes.Structure):
  _fields_ = [
    ('mNumberChannels', ctypes.c_uint32),
    ('mDataByteSize', ctypes.c_uint32),
    ('mData', ctypes.c_void_p),
  ]


class AudioBufferList(ctypes.Structure):
  _fields_ = [
    ('mNumberBuffers', ctypes.c_uint32),
    ('mBuffers', AudioBuffer * 1),
  ]


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

  instance = ObjCInstance(inRefCon)
  amplitude = 0.9
  sampleRate = 44100
  frequency = instance.frequency
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
  #print(theta)
  return 0


class PyAudio:

  def __init__(self, instance):
    self.instance = instance
    self.cd = AudioComponentDescription()
    self.cd.componentType = kAudioUnitType_Output
    self.cd.componentSubType = kAudioUnitSubType_RemoteIO
    self.cd.componentManufacturer = kAudioUnitManufacturer_Apple
    self.cd.componentFlags = 0
    self.cd.componentFlagsMask = 0

    self.defaultOutput = AudioComponentFindNext(None, ctypes.byref(self.cd))

    self.toneUnit = ctypes.c_void_p(0)

    self.err = AudioComponentInstanceNew(self.defaultOutput,
                                         ctypes.byref(self.toneUnit))

    self.input = AURenderCallbackStruct()
    self.RenderTone = AURenderCallback(render_callback)
    self.input.inputProc = self.RenderTone
    self.input.inputProcRefCon = self.instance.ptr
    self.err = AudioUnitSetProperty(self.toneUnit,
                                    kAudioUnitProperty_SetRenderCallback,
                                    kAudioUnitScope_Input, 0,
                                    ctypes.byref(self.input),
                                    ctypes.sizeof(self.input))
    self.setup()

  def setup(self):
    AudioUnitInitialize(self.toneUnit)
    AudioOutputUnitStart(self.toneUnit)

  def shutdown(self):
    AudioOutputUnitStop(self.toneUnit)
    AudioUnitUninitialize(self.toneUnit)
    AudioComponentInstanceDispose(self.toneUnit)


class View(ui.View):

  def __init__(self):
    self.instance = ObjCInstance(self)
    self.py_audio = PyAudio(self.instance)
    self.instance.theta = 0
    self.instance.frequency = 440
    self.setup_ui()

  def setup_ui(self):
    self.tone_label = ui.Label()
    self.tone_label.font = ('DIN Alternate', 32)
    self.tone_label.alignment = 1

    self.tone_label.text = f'{int(self.instance.frequency):03}'
    self.tone_label.bg_color = 'maroon'
    self.tone_slider = ui.Slider()
    self.tone_slider.value = 0.5
    self.tone_slider.action = self.set_frequency
    self.add_subview(self.tone_label)
    self.add_subview(self.tone_slider)

  def layout(self):
    _x, _y, _w, _h = self.frame

    self.tone_label.x = (_w / 2) - (self.tone_label.width / 2)
    self.tone_label.y = (_h / 3)

    self.tone_slider.width = sw = _w * 0.8
    self.tone_slider.x = (_w / 2) - (sw / 2)
    self.tone_slider.y = _h / 2

  def set_frequency(self, sender):
    self.instance.frequency = sender.value * 880
    self.tone_label.text = f'{int(self.instance.frequency):03}'

  def will_close(self):
    self.py_audio.shutdown()


view = View()
editor.present_themed(
  view,
  theme_name='Theme09_Editorial',
  style='fullscreen',
  #hide_title_bar=True,
  orientations=['portrait'])

