# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

import cv2
from rapidocr_onnxruntime import RapidOCR, VisRes

from rapid_table import RapidTable, RapidTableInput, VisTable

# Init
ocr_engine = RapidOCR()
vis_ocr = VisRes()

input_args = RapidTableInput(model_type="unitable")
table_engine = RapidTable(input_args)
viser = VisTable()

img_path = "tests/test_files/table.jpg"

# OCR
ocr_result, _ = ocr_engine(img_path)
boxes, txts, scores = list(zip(*ocr_result))

# Table Rec
table_results = table_engine(img_path, ocr_result)
table_html_str, table_cell_bboxes = table_results.pred_html, table_results.cell_bboxes

# Save
save_dir = Path("outputs")
save_dir.mkdir(parents=True, exist_ok=True)

save_html_path = save_dir / f"{Path(img_path).stem}.html"
save_drawed_path = save_dir / f"{Path(img_path).stem}_table_vis{Path(img_path).suffix}"

# Visualize table rec result
vis_imged = viser(img_path, table_results, save_html_path, save_drawed_path)

# Visualize OCR result
save_ocr_path = save_dir / f"{Path(img_path).stem}_ocr_vis{Path(img_path).suffix}"
res = vis_ocr(vis_imged, boxes)
cv2.imwrite(save_ocr_path, res)
print(table_html_str)

print(f"The results has been saved {save_dir}")
