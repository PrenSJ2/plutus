from fastapi import APIRouter, Depends

from app.auth.views import get_token
from app.cal._utils import app_logger
from app.cal.tasks import create_cal_for_property, create_trips_from_ics
from app.models import PropertyCal

cal_router = APIRouter()


# Calendar Generation
@cal_router.get('/get_property_cal')
def get_property_cal(property_ref: str, token: str = Depends(get_token)):
    cal_link = create_cal_for_property(property_ref)
    app_logger.info(property_ref)
    # add all cal stuff
    return {'propertyRef': property_ref, 'cal_link': cal_link}


# Sync External Calendar
@cal_router.post('/cal_to_property')
def cal_to_property(data: PropertyCal, token: str = Depends(get_token)):
    app_logger.info(data.property_ref)
    app_logger.info(data.cal_link)
    # add all cal stuff
    if create_trips_from_ics(data.property_ref, data.cal_link):
        return {'propertyRef': data.property_ref, 'message': 'Calendar successfully added to property'}
    else:
        return {'propertyRef': data.property_ref, 'message': 'Calendar could not be added to property'}
