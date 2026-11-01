# Official HYDRA logo extraction

Source: supplied `Brand Kit HYDRA(2).pdf`, page 1, the upper “Logo principal” wordmark. Source SHA-256: `998ecbb07c29b3756a9c9d1097324ace0617d9ae499a524df11ac4056d07d6ab`.

The files use the original PDF vector geometry. The north-star symbol is six filled source paths. HYDRA is an exact 78-segment vector clipping path that masks a gradient in the PDF; its letter outlines and original spacing were extracted directly. The monochrome silkscreen changes color only. There is no AI generation, font substitution, OCR, or raster tracing.

The blue H/trident emblem on the right is an embedded 4096 × 4096 raster image in this PDF, not a vector path. It was excluded because a vector approximation would require tracing. The robot photograph was also excluded. These are compact extracted wordmark/mark elements, not a recreation of the complete photograph-containing principal lockup.

## Available native footprints

| Footprint | Actual graphic size | Smallest finite R–A gap | Use |
| --- | --- | --- | --- |
| `HYDRA_Official_Vector_22mm.kicad_mod` | 22 × 4.3812 mm | 0.06736 mm | Compact exact geometry; gap is below a 0.15 mm silkscreen target. |
| `HYDRA_Official_Vector_50mm.kicad_mod` | 50 × 9.9572 mm | 0.15309 mm | Recommended star + HYDRA size when space permits. |
| `HYDRA_Official_Wordmark_22mm.kicad_mod` | 22 × 4.7622 mm | 0.08570 mm | Compact HYDRA text only; gap is below the target. |
| `HYDRA_Official_Wordmark_40mm.kicad_mod` | 40 × 8.6586 mm | 0.15581 mm | Recommended wordmark size for a 0.15 mm minimum finite gap. |

Every footprint is centered at the center of its graphic bounding box. It contains filled `F.SilkS` polygons only, plus hidden reference/value metadata on `F.Fab`; there are no pads, copper graphics, mask openings, or courtyard geometry. The footprint’s `F.Cu` header identifies the front-side placement and does not place the logo on copper. Each variant also has a same-name SVG and PNG. The SVG preserves source cubic curves; the PNG previews the actual footprint polygons on a green background.

## Scaling and manufacturing limits

Star + wordmark source bounding box: x = 751.000008 to 1152.717773, y = 149.999944 to 229.999998 PDF points. Wordmark-only bounding box: x = 836.952026 to 1152.717773, y = 155.648056 to 224.000061 PDF points. Scale and dimensions for each variant are recorded in `extraction_manifest.json`.

The original R–A spacing is 1.22998047 PDF points at its narrowest. A 0.15 mm finite interletter gap therefore requires at least 48.9908 mm overall for star + wordmark, or 38.5087 mm for the wordmark only. Rounded recommendations are **50 mm** and **40 mm**, respectively. Other main letter strokes are substantially wider; at 22 mm overall lockup width the 8.544-point R crossbar is approximately 0.468 mm.

The star contains pointed tips and point contacts that taper toward zero width. No finite enlargement can make every mathematical tip satisfy a 0.15 mm rule. The supplied geometry retains these exact features without widening, clipping, or changing their spacing. A manufacturer may round or lose the finest tip/center details. Use the wordmark-only 40 mm footprint when preserving a conventional 0.15 mm finite gap matters more than including the star. If using a compact 22 mm variant, inspect the fabrication preview and accept the documented R–A gap risk explicitly.

The native footprint flattens cubic curves with at most 0.004 PDF-point control-to-chord flatness per recursive segment, giving less than 0.00051 mm flattening tolerance at the largest provided scale. Counter shapes in D, R, and A are preserved by decomposing the filled source outline into touching trapezoids; the filled area is checked numerically against the outline’s signed area. No geometry is thickened to improve printability.

Extraction and verification are reproducible with `extract_hydra_logo.py`. `official_main_logo_crop.png` and `source_page_01.png` show the source context; `source_page_01.svg` is the full source page vector export.

## Validation

All four native files parse successfully with Python `sexpdata` and load successfully through `pcbnew.FootprintLoad` using KiCad 9.0.9 from the local tool bundle. Native graphics counts are 1,093 for star + wordmark and 1,087 for wordmark only. All graphic polygons are on `F.SilkS`; no pads are present. The PNG previews of the 22 mm lockup and 40 mm wordmark were inspected visually and preserve the correct letter counters, source spacing, and star shape. Fine geometry and interletter-gap limitations remain as described above.
