from objc_util import UIApplication, ObjCInstance, c

import ctypes
import math

import ui, editor

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
AudioComponentFindNext.argtypes = (ctypes.c_void_p,
                                   ctypes.POINTER(AudioComponentDescription))
AudioComponentFindNext.restype = ctypes.c_void_p
# --- AudioComponentFindNext */

# --- AudioComponentInstanceNew
OSStatus = ctypes.c_int32
AudioComponentInstanceNew = c.AudioComponentInstanceNew
AudioComponentInstanceNew.argtypes = (ctypes.c_void_p, ctypes.c_void_p)
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
  _fields_ = (('mSubframes', ctypes.c_int16), ('mSubframeDivisor',
                                               ctypes.c_int16),
              ('mCounter', ctypes.c_uint32), ('mType', SMPTETimeType),
              ('mFlags', SMPTETimeFlags), ('mHours', ctypes.c_int16),
              ('mMinutes', ctypes.c_int16), ('mSeconds', ctypes.c_int16),
              ('mFrames', ctypes.c_int16))


class AudioTimeStamp(ctypes.Structure):
  _fields_ = (('mSampleTime', ctypes.c_double), ('mHostTime', ctypes.c_int64),
              ('mRateScalar', ctypes.c_double),
              ('mWordClockTime', ctypes.c_uint64), ('mSMPTETime', SMPTETime),
              ('mFlags', AudioTimeStampFlags), ('mReserved', ctypes.c_uint32))


class AudioBuffer(ctypes.Structure):
  _fields_ = (('mNumberChannels', ctypes.c_uint32),
              ('mDataByteSize', ctypes.c_uint32), ('mData', ctypes.c_void_p))


class AudioBufferList(ctypes.Structure):
  _fields_ = (('mNumberBuffers', ctypes.c_uint32), ('mBuffers',
                                                    AudioBuffer * 1))


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
  _fields_ = (('inputProc', AURenderCallback), ('inputProcRefCon',
                                                ctypes.c_void_p))


# --- AURenderCallbackStruct */

# --- AudioUnitSetProperty
AudioUnitSetProperty = c.AudioUnitSetProperty
AudioUnitSetProperty.argtypes = (ctypes.c_void_p, ctypes.c_uint32,
                                 ctypes.c_uint32, ctypes.c_uint32,
                                 ctypes.c_void_p, ctypes.c_uint32)
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
  instance.buffer = buffer
  instance.theta = theta
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
    self.instance.buffer = []
    self.time_div = 120
    self.update_interval = 1 / self.time_div

    self.setup_ui()

  def draw(self):
    ui.set_color('lime')
    line = ui.Path()
    line.line_width = 2
    self.segment = len(self.instance.buffer)
    amp = self.height / 8
    for n, b in enumerate(self.instance.buffer):
      x = (n / (self.segment - 1)) * self.width
      y = amp * b + self.height / 2
      if n: line.line_to(x, y)
      else: line.move_to(x, y)
    line.stroke()

  def update(self):
    self.set_needs_display()

  def setup_ui(self):
    self.frequency_label = ui.Label()
    self.frequency_label.font = ('DIN Alternate', 64)
    self.frequency_label.alignment = 1
    self.frequency_label.text = f'{int(self.instance.frequency):03}'
    self.frequency_label.bg_color = 'maroon'
    self.frequency_slider = ui.Slider()
    self.frequency_slider.value = 0.5
    self.frequency_slider.action = self.set_frequency
    self.add_subview(self.frequency_label)
    self.add_subview(self.frequency_slider)

  def layout(self):
    _x, _y, _w, _h = self.frame
    self.frequency_label.x = (_w / 2) - (self.frequency_label.width / 2)
    self.frequency_label.y = (_h / 3)

    self.frequency_slider.width = sw = _w * 0.92
    self.frequency_slider.x = (_w / 2) - (sw / 2)
    self.frequency_slider.y = (_h / 2) - (self.frequency_slider.height / 2)

  def set_frequency(self, sender):
    self.instance.frequency = sender.value * 880
    self.frequency_label.text = f'{int(self.instance.frequency):03}'

  @ui.in_background
  def will_close(self):
    self.instance.buffer = [-1] * self.segment
    self.py_audio.shutdown()


view = View()
editor.present_themed(view,
                      theme_name='Theme09_Editorial',
                      style='fullscreen',
                      orientations=['portrait'])

