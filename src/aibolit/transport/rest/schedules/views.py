from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated
from aibolit.core.dependencies import get_user_service, get_schedule_service
from aibolit.services.users.service import UserService

# from aibolit.schemas.schedules.schemas import (
from aibolit.schemas.openapi_generated.schemas import (
    MedicationScheduleCreateResponse,
    MedicationScheduleCreateRequest,
    MedicationScheduleIdsResponse,
    MedicationSchedule,
    NextTakingsMedicationsResponse,
)
from aibolit.services.schedules.service import ScheduleExpiredError, ScheduleNotFound, ScheduleService

router = APIRouter()


@router.post("/schedule", status_code=201, response_model=MedicationScheduleCreateResponse)
async def create_schedule(
    schedule: MedicationScheduleCreateRequest,
    schedule_service: Annotated[ScheduleService, Depends(get_schedule_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> MedicationScheduleCreateResponse:
    user_exists = await user_service.get_user_by_id(schedule.user_id)
    if not user_exists:
        raise HTTPException(status_code=404, detail=f"User with id={schedule.user_id} not found")
    schedule = await schedule_service.create_schedule(schedule)
    return schedule


@router.get("/schedules", response_model=MedicationScheduleIdsResponse)
async def get_all_schedules(
    user_id: int,
    schedule_service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> MedicationScheduleIdsResponse:
    return await schedule_service.get_all_user_schedules(user_id)


@router.get("/schedule", response_model=MedicationSchedule)
async def get_user_schedule(
    schedule_id: int,
    user_id: int,
    schedule_service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> MedicationSchedule:
    try:
        user_schedule = await schedule_service.get_user_schedule(user_id=user_id, schedule_id=schedule_id)
        return user_schedule
    except (ScheduleExpiredError, ScheduleNotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))


#
@router.get("/next_takings", response_model=NextTakingsMedicationsResponse)
async def get_user_next_takings(
    user_id: int,
    schedule_service: Annotated[ScheduleService, Depends(get_schedule_service)],
) -> NextTakingsMedicationsResponse:
    return await schedule_service.get_user_next_takings(user_id)
