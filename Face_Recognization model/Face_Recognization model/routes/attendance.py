"""Attendance API endpoints."""

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from datetime import datetime

import services.attendance_service as attendance_svc

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("/mark")
async def mark_attendance(image: UploadFile = File(...)):
    """
    Mark attendance by recognizing face from uploaded image.
    One attendance per person per day.
    """
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    image_bytes = await image.read()
    result = await attendance_svc.mark_attendance(image_bytes)
    return result


@router.get("/records")
async def get_attendance(
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=500),
):
    """Get attendance records."""
    records = await attendance_svc.get_attendance(date=date, limit=limit)
    return {"records": records, "count": len(records)}


@router.get("/export")
async def export_attendance(
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
):
    """Download attendance as Excel file."""
    buffer = await attendance_svc.export_attendance_to_excel(date=date)
    filename = f"attendance_{date or datetime.utcnow().strftime('%Y-%m-%d')}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
