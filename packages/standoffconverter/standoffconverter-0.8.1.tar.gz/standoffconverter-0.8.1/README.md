# standoffconverter


I intended this package to be used in the following situation:
Given a bunch of XML files (e.g. standard TEI files), I would like to add new annotations (for example with an ML method). The workflow would then be

```
import standoffconverter.Converter as Co

# 1. load the original TEI file and convert it to standoff format
converter = Co(some_xml_tree)

# 2. create new annotations (automatically) and add them to the original
converter.add_inline(
            begin=begin,
            end=end,
            tag="SOMETAG",
            depth=None,
            attrib={}
        )

# 3. store the modified XML
new_tree = converter.tei_tree
```
# Documentation
[https://standoffconverter.readthedocs.io](https://standoffconverter.readthedocs.io/)
