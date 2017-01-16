---
title: Basics of Physically-based Rendering
date: 2017-11-26 23:30:10
tags: CG
categories: 数学
---

-------------------------------------

# Photon for Graphics People

```
photon = {energy, wavelength, polarization, time, position, direction}
```

This is not a photon as is meant in physics!

# Radiance

1. stays constant along a line (don't lose enery as they travel).
2. very similar to "colors" see in a direction.
3. radiometric quantites can be derived from rediance.

```
radiance = L(position, direction, wavelength, time)
```

## Incoming Radiance

often called field radiance, is what an insect on the surface sees coming into it, like an environment map.

## Outgoing Radiance

often called surface radiance, is what the viewer seed lokking at a surface.
