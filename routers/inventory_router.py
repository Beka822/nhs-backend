from io import BytesIO
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from core.db import get_db
from models.user import User
from core.dependencies import get_user_object
from models.pharmacy import Drug
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Font
router=APIRouter(prefix="/export",tags=["Export"])
@router.get("/inventory")
def export_inventory(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    drugs=db.query(Drug).filter(Drug.hospital_id==current_user.hospital_id).all()
    wb=Workbook()
    ws=wb.active
    ws.title="Inventory"
    ws.append(["PHARMACY INVENTORY EXPORT"])
    ws["A1"].font=Font(bold=True,size=14)
    ws.append([])
    headers=[
        "Drug ID",
        "Drug Name",
        "Category",
        "Unit",
        "Buying Price",
        "Selling Price",
        "Stock Quantity",
        "Reorder Level",
        "Expiry Date",
        "Created At"
    ]
    ws.append(headers)
    for cell in ws[3]:
        cell.font=Font(bold=True)
    for drug in drugs:
        ws.append([
            drug.drug_id,
            drug.name,
            drug.category,
            drug.unit,
            float(drug.buying_price or 0),
            float(drug.selling_price or 0),
            drug.quantity_in_stock,
            drug.reorder_level,
            str(drug.expiry_date or ""),
            str(drug.created_at)
        ])
    for column in ws.columns:
        max_length=0
        column_letter=column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value))>max_length:
                    max_length=len(str(cell.value))
            except:
                pass
        adjusted_width=max_length + 4
        ws.column_dimensions[column_letter].width=adjusted_width
    stream=BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocuments.spreadsheetml.sheet",
        headers={
            "Content-Disposition":"attachment; filename=inventory_export.xlsx"
        }
    )
