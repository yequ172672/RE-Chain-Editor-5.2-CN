# RE Chain Editor localization

The add-on keeps Chinese translations in the root [`translations.py`](translations.py) module. It registers two equivalent language tables, `zh_CN` and `zh_HANS`, through Blender 5.2's `bpy.app.translations` API. Interface labels and RNA property text use the default `*` context; operator labels, popups, and reports use the `Operator` context.

Registering the add-on calls `translations.register()` and unloading it calls `translations.unregister()`. The `interface()`, `tip()`, and `report()` helpers are for dynamic text, so formatting happens after Blender resolves the translated template. When Blender runs in English, the same helpers return the original source strings. File extensions, format identifiers, enum values used by the binary readers, and game IDs remain unchanged.

To validate the table without changing a live Blender profile, run a factory-startup Blender 5.2 background script that sets the in-memory locale to `zh_HANS`, imports the add-on, calls `register()` and `unregister()`, and checks representative `pgettext_iface()`/`pgettext_tip()` results. Do not save preferences from that script.
