# pysta-sine_wave001

> 2020/09/11


[Pythonista3](http://omz-software.com/pythonista/) Script !



ソースをコピペすれば、そのまま動くよ 🥳




## Referenced site

- [Real time audio buffer synth/Real time image smudge tool](https://forum.omz-software.com/topic/5155/real-time-audio-buffer-synth-real-time-image-smudge-tool)
- [An iOS tone generator (an introduction to AudioUnits)](https://www.cocoawithlove.com/2010/10/ios-tone-generator-introduction-to.html)
- [7gano's Weblog カテゴリー: Getting Started With Audio Unit](https://7gano.wordpress.com/category/getting-started-with-audio-unit/page/2/)


## ワイメモ

とりあえず

```
from objc_util import c
```
で呼び出してるやつ



### `Function`


- `&hoge` のやつ

  - 定義時は`POINTER`
	- 呼び出す時は、`byref`
なのかな？



#### Pythonista

`AudioComponent defaultOutput = AudioComponentFindNext(NULL, &defaultOutputDescription);`

```
AudioComponentFindNext = c.AudioComponentFindNext
AudioComponentFindNext.argtypes = (
  ctypes.c_void_p, ctypes.POINTER(AudioComponentDescription)
)
AudioComponentFindNext.restype = ctypes.c_void_p

```


```
defaultOutput = AudioComponentFindNext(None, ctypes.byref(self.cd))
```

`.argtypes` は、`list` の例が多いが`tuple` でもよさそう


もしかしたら、関数化してもよい？



#### Swift

```
func AudioComponentFindNext(_ inComponent: AudioComponent?, 
                          _ inDesc: UnsafePointer<AudioComponentDescription>) -> AudioComponent?

```

#### Objective-C

``` 
AudioComponent AudioComponentFindNext(AudioComponent inComponent, const AudioComponentDescription *inDesc);

```


