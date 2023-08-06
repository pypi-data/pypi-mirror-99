# String Output

## Convert to Strings

Colors can be translated to strings by using the `to_string` method. The color class will convert the current color into
one of many of the color's CSS formats.

```color
Color("srgb", [0.5, 0, 1], 0.3).to_string()
```

All color spaces support the following parameters:

- `alpha`: set to `#!py3 None` by default, alpha will only be shown if less than 100%, but if set to `#!py3 True`, alpha
  will always be shown. Setting to `#!py3 False` will cause alpha to be ignored in the output.
- `precision`: precision controls the precision of the output values. The name is a little misleading as it will
  actually adjust the precision and scale of the values. The default is 5. In some cases, like sRGB hex output,
  precision may not really come into play as hex values are rounded to the nearest whole number anyways.

    ```color
    Color("rgb(30.3456% 75% 100%)").to_string(precision=5, percent=True)
    Color("rgb(30.3456% 75% 100%)").to_string(precision=4, percent=True)
    Color("rgb(30.3456% 75% 100%)").to_string(precision=3, percent=True)
    Color("rgb(30.3456% 75% 100%)").to_string(precision=2, percent=True)
    Color("rgb(30.3456% 75% 100%)").to_string(precision=1, percent=True)
    ```

    Providing a precision of `0` will simply enable simple rounding to the nearest whole number.

    ```color
    Color("rgb(30.3456% 75% 100%)").to_string(precision=0, percent=True)
    ```

    Providing a precision of `-1` is a special input that will give the highest precision that can be given. Not
    particularly helpful except to look at the raw decimal number.

    ```color
    Color("rgb(30.3456% 75% 100%)").to_string(precision=-1, percent=True)
    ```

    One note though, format of the value matters. Here we output in the range of 0 - 255. We can see that a precision of
    `1`, in this case, can throw the color out of gamut. So remember to use a sufficient precision for what you are
    doing and the values you are working in.

    ```color
    Color("rgb(30.3456% 75% 100%)").to_string(precision=1)
    ```

- `fit`: set to `#!py3 True` by default, `fit` controls whether colors are fit to their gamut or not. Some color spaces
  are technically unbounded, so no fitting may occur in those color spaces. Additionally, some color formats, like sRGB
  hex, are always fitted (regardless of the this setting) as they must fit into the gamut or they cannot be translated.

      ```color
      Color("rgb(30% 105% 0%)").to_string(),
      Color("rgb(30% 105% 0%)").to_string(fit=False)
      ```

- `color`: for some color spaces, this is the default output, but for others this format can be explicitly requested by
  setting `color` to `#!py3 True`. If set to `#!py3 True`, this will take priority over other format options.

    ```color
    Color("rebeccapurple").to_string(color=True)
    ```

In general, a color in a given color space may share the same options as listed above, but a given color space may also
have options unique to itself.

## sRGB Specific

sRGB can output colors to a hex format which is unique compared to HSL and others. Simply enable `hex`.

```color
Color("rebeccapurple").to_string(hex=True)
```

You can force hex to output in uppercase.

```color
Color("red").to_string(hex=True)
Color("red").to_string(hex=True, upper=True)
```

When converting to the hex color format, a color can be compressed in certain cases. Enabling `compress` will compress a
hex color if possible.

```color
Color("#11223388").to_string(hex=True)
Color("#11223388").to_string(hex=True, compress=True)
```

sRGB also can output colors in an optional percent format. This will output the channels in the range of [0%,100%]
instead of using the range [0,255].

```color
Color("rebeccapurple").to_string(percent=True)
```

sRGB can also output color names. If a color evaluates to a hex code which also evaluates to a color name in the
internal CSS color name mapping, then a color name will be returned. If the color does not match a color name, it will
fallback to whatever the other options dictate. Simply enable `names`.

```color
Color("#663399").to_string(names=True)
```

## Comma Format

In CSS, there are a number of color spaces that allow a comma format: `srgb`, `hsl`, and `hwb`. ColorAide allows these
colors to be output in their legacy comma format. Even though `lch` and `lab` technically do not have a comma format,
they can also have commas enabled. The one format that ColorAide will not allow commas on is `color()`. `color()` is
the common serialization format that ColorAide uses and is strict about its format.

If we want commas, we can force the comma syntax by setting `comma` to `#!py3 True`. This can alter some color space
output in other subtle ways. As the comma format is the old legacy approach, when sRGB has commas enabled, it will use
`rgba` instead of the `rgb`. If using the default space syntax, `rgb` is always used, even when the color has
transparency.

```color
Color("rgb(30 75 100 / 20%)").to_string(comma=True)
```
