---
authors: yihong
tags: [feelsbad]
title: What happens when RPI Imager crashes in the middle of flashing?
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

My experience with the M1 Chip has been awesome, seeing how much more efficient the battery is and how much faster my builds are. But it is these rare (debatable) incompatiblity issues that sometimes I wish I have stucked with a PC.

<!--truncate-->

I was flashing a SD card with a RPI OS image on my mac when the imager reported a _write error_ without any error code or additional hints. What followed immediately was that my SD card became **uninitialized**. This meant that my SD was no longer readable and the file system/partitions (in fact everything) was gone. At this point I thought it was a freak event, so I went to reformat it.

In the case where you faced the same thing, you can reformat the SD card with the following configs:

- File System Type: **MS-DOS(FAT-32)**
- Partition Scheme: **Master Boot Record(MBR)**

<Tabs>
  <TabItem value="win" label="Windows" default>
  <ol>
    <li>Right click your SD-card</li>
    <li>Reformat</li>
    <li>Choose <b>exFAT</b> as File System</li>
  </ol> 
  </TabItem>
  <TabItem value="mac" label="Mac">
  <ol>
    <li>Open <i>Disk Utility</i></li>
    <li>Select the uninitialized disk corresponding to your SD-card</li>
    <li>Choose <b>MS-DOS(FAT)</b> as File System Type</li>
    <li>Choose <b>Master Boot Record</b> as Partition Scheme</li>
  </ol> 
  </TabItem>
</Tabs>

I fired up the Imager again and gave it another shot. It didn't work so like every programmer I reformatted it again and tried to flash it again with the Imager. This time the progress bar went to up around `17%` (previously it failed at `3%`), so I was rather hopeful, but after a celebratory trip to the water cooler, the same error popped up when I came back.

Perhaps it was a problem with the Imager so I tried to flash it manually. (you can get a comprehensive guide on how to do that [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-images-on-mac-os)) The process ended up with no errors and after doing a sanity check to see if I have actually got data onto the disk (SD-card), I thought it worked.

```
kernel panic-not syncing: VFS: unable to mount root fs on unknown-block(179,2)
```

While booting up, the kernel panicked and so did I. To put it simply, the error had something to do with the kernel not being able to pick up the right partition of the file system. Followed some fixes but after rounds of reformatting and flashing, it still didn't seem to work.

At this point you are probably expecting I found a fix... well technically I did but it was more of avoiding this specific problem. I went back to my old `win` PC and did the whole process again. 

**It worked.**

I will probably find some time in the future to look more this but I guess the journey that a RPI Imager crashing in the middle of flashing took me on made me appreciate `win` more for its convenience and got me disappointed at engineers' lack of effort to support M1 hardware even after more than a year since its launch.
