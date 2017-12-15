pcm.jack {
  type hw
  card ALSA
}
pcm.array {
  type hw
  card CameraB409241
}
pcm.softvol {
  type softvol
  slave.pcm "jack"
  control {
    name Master
    card 0
  }
}
pcm.cap {
  type plug
  slave.pcm "array"
  slave.channels 4
  ttable {
    0.0 30.0
    1.1 30.0
  }
}
pcm.!default {
    type asym
    playback.pcm "plug:softvol"
    capture.pcm {
      type plug
      slave.pcm "cap"
    }
}
ctl.!default {
  type hw
  card 0
}
ctl.softvol {
  type hw
  card 0
}
