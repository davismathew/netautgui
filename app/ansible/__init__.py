from flask import Blueprint

ansible = Blueprint('ansible', __name__)

from . import views
from ..models import Permission
